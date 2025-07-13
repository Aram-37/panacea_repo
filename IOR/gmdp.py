import os
import re
import glob
import hashlib
import signal
import time
import docx
import PyPDF2
from multiprocessing import Pool, cpu_count
from functools import partial
from datetime import datetime
import json

try:
    from tqdm import tqdm
except ImportError:
    print("⚠️ 'tqdm' library not found. Progress bars will not be displayed.")
    print("   Install it with: pip install tqdm")
    def tqdm(iterable, *args, **kwargs):
        return iterable

# --- Centralized Configuration ---
CONFIG = {
    "supported_extensions": ('.txt', '.docx', '.pdf', '.json'),
    "patterns": {
        # Patterns to identify HUMAN dialogue - these are PRESERVED
        "human_dialogue": [
            r'^(User|Human|britkenko|성협|Cor|You)\s*[:：]\s*.+',
            r'^\s*\[(User|Human|britkenko)\]\s*[:：]?\s*.+',
            r'^[^A-Z]*[:：]\s*.{10,}',  # Casual human speech patterns
            r'.*\?\s*$',  # Questions (often human)
            r'.*\!\s*$',  # Exclamations (often human)
            r'.*\.\.\.\s*$',  # Trailing thoughts (often human)
        ],
        # Patterns to identify AI responses - these are KEPT but with lower priority
        "ai_dialogue": [
            r'^(ChatGPT|GPT|Assistant|AI|Claude|Gemini|GitHub Copilot|Copilot)\s*[:：]\s*.+',
            r'^\s*\[(ChatGPT|Assistant|AI|Claude|Gemini)\]\s*[:：]?\s*.+',
        ],
        # Patterns to SKIP entirely
        "skip_patterns": [
            r'^(import|from|def|class|if|else|elif|for|while|try|except|return|print)\s',
            r'^\s*[#//]\s*',
            r'\b(doi:|arxiv:|isbn:|issn:)\b',
            r'\b[\w\.-]+@[\w\.-]+\.\w+\b',  # emails
            r'\b\d{3}-\d{3}-\d{4}\b',  # phone numbers
            r'\b(password|pwd|token|key|secret)\s*[:：=]',
        ],
        # Patterns that indicate non-dialogue structure
        "non_dialogue_starters": [
            r'^\d+[\.\)]\s*',
            r'^[-\*\+]\s*',
            r'^#+\s*',  # headers
        ],
    }
}

def extract_embedded_timestamps(text):
    """Extract timestamps embedded in dialogue text and return standardized format."""
    # 타임스탬프 추출 비활성화
    return None

def clean_text_of_timestamps(text):
    """Remove embedded timestamps from text."""
    # 타임스탬프 정리 비활성화 - 원본 텍스트를 그대로 반환
    return text

def should_skip_line(line, patterns):
    """Checks if a line should be completely skipped."""
    return any(re.search(p, line, re.IGNORECASE) for p in patterns['skip_patterns'])

def is_human_dialogue(line, patterns):
    """Checks if a line is human dialogue (highest priority)."""
    return any(re.match(p, line, re.IGNORECASE) for p in patterns['human_dialogue'])

def is_ai_dialogue(line, patterns):
    """Checks if a line is AI dialogue (kept but lower priority)."""
    return any(re.match(p, line, re.IGNORECASE) for p in patterns['ai_dialogue'])

def is_likely_dialogue(line):
    """Heuristic check for dialogue-like content."""
    stripped = line.strip()
    if len(stripped) < 5:
        return False
    
    # Check for dialogue markers
    dialogue_indicators = [
        '"' in stripped,  # Quoted speech
        "'" in stripped and len(stripped) > 20,  # Quoted speech
        stripped.count('?') > 0,  # Questions
        stripped.count('!') > 0,  # Exclamations
        any(word in stripped.lower() for word in ['you', 'i', 'me', 'my', 'your', 'we', 'us']),  # Personal pronouns
    ]
    
    return any(dialogue_indicators)

def extract_dialogues_from_json(content):
    """Extract dialogues from JSON conversation format maintaining sequence."""
    dialogues = []
    
    try:
        data = json.loads(content)
        
        # Handle different JSON structures
        if isinstance(data, dict) and 'mapping' in data:
            # ChatGPT conversation format
            mapping = data['mapping']
            
            # Create a list of messages with timestamps
            messages = []
            for msg_id, msg_data in mapping.items():
                if 'message' in msg_data and msg_data['message']:
                    message = msg_data['message']
                    if 'content' in message and message['content']:
                        content_parts = message['content'].get('parts', [])
                        if content_parts:
                            text = ' '.join(str(part) for part in content_parts if part)
                            author = message.get('author', {}).get('role', 'unknown')
                            create_time = message.get('create_time', 0)
                            
                            messages.append({
                                'text': text,
                                'author': author,
                                'timestamp': create_time,
                                'msg_id': msg_id
                            })
            
            # Sort by timestamp to maintain sequence
            messages.sort(key=lambda x: x['timestamp'])
            
            # Convert to dialogue format
            for msg in messages:
                if msg['author'] != 'system' and msg['text'].strip():
                    dialogues.append({
                        'text': msg['text'],
                        'author': msg['author'],
                        'timestamp': msg['timestamp'],
                        'sequence_id': len(dialogues)
                    })
        
        elif isinstance(data, list):
            # List of dialogue objects
            for i, item in enumerate(data):
                if isinstance(item, dict) and 'text' in item:
                    dialogues.append({
                        'text': item['text'],
                        'author': item.get('author', 'unknown'),
                        'timestamp': item.get('timestamp', i),
                        'sequence_id': i
                    })
    
    except json.JSONDecodeError:
        # If it's not valid JSON, treat as plain text
        return extract_dialogues_from_text(content)
    
    return dialogues

def extract_dialogues_from_text(content):
    """Extract dialogues from plain text maintaining chronological sequence."""
    lines = content.splitlines()
    dialogues = []
    
    for line_num, line in enumerate(lines):
        stripped_line = line.strip()
        if not stripped_line:
            continue
        
        # Skip unwanted content
        if should_skip_line(stripped_line, CONFIG['patterns']):
            continue
        
        # Extract timestamp if present
        timestamp = extract_embedded_timestamps(stripped_line)
        cleaned_text = clean_text_of_timestamps(stripped_line)
        
        # Check if it's dialogue
        is_dialogue = (
            is_human_dialogue(stripped_line, CONFIG['patterns']) or
            is_ai_dialogue(stripped_line, CONFIG['patterns']) or
            is_likely_dialogue(stripped_line)
        )
        
        if is_dialogue and cleaned_text:
            # Determine author
            author = 'human'
            if is_ai_dialogue(stripped_line, CONFIG['patterns']):
                author = 'ai'
            elif is_human_dialogue(stripped_line, CONFIG['patterns']):
                author = 'human'
            else:
                author = 'unknown'
            
            dialogues.append({
                'text': cleaned_text,
                'author': author,
                'timestamp': timestamp,
                'line_number': line_num,
                'sequence_id': len(dialogues)
            })
    
    # Sort by timestamp if available, otherwise by line number
    def sort_key(dialogue):
        if dialogue['timestamp']:
            return dialogue['timestamp']
        else:
            return datetime.fromtimestamp(dialogue['line_number'])
    
    dialogues.sort(key=sort_key)
    
    # Update sequence IDs after sorting
    for i, dialogue in enumerate(dialogues):
        dialogue['sequence_id'] = i
    
    return dialogues

def filter_dialogue_content(content, patterns):
    """Extracts dialogue maintaining chronological sequence."""
    # First check if content is JSON
    content_stripped = content.strip()
    if content_stripped.startswith('{') or content_stripped.startswith('['):
        dialogues = extract_dialogues_from_json(content)
    else:
        dialogues = extract_dialogues_from_text(content)
    
    # Convert back to text format maintaining sequence
    dialogue_lines = []
    for dialogue in dialogues:
        timestamp_str = ""
        if dialogue['timestamp']:
            if isinstance(dialogue['timestamp'], datetime):
                timestamp_str = f"[{dialogue['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}] "
            elif isinstance(dialogue['timestamp'], (int, float)):
                timestamp_str = f"[{datetime.fromtimestamp(dialogue['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}] "
        
        author_str = f"{dialogue['author'].title()}: " if dialogue['author'] != 'unknown' else ""
        dialogue_lines.append(f"{timestamp_str}{author_str}{dialogue['text']}")
    
    return '\n'.join(dialogue_lines)

def clean_paragraph(paragraph_text):
    """Removes duplicate sentences from a paragraph."""
    sentences = re.split(r'(?<=[.?!])\s+', paragraph_text)
    seen_sentences = set()
    unique_sentences = []
    
    for sent in sentences:
        normalized_sent = sent.strip().lower()
        if normalized_sent and normalized_sent not in seen_sentences:
            seen_sentences.add(normalized_sent)
            unique_sentences.append(sent.strip())
    
    return ' '.join(unique_sentences)

def get_content_from_file(file_path):
    """Extracts text content from supported file types."""
    lower_path = file_path.lower()
    content = ""
    
    try:
        if lower_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        elif lower_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        elif lower_path.endswith('.docx'):
            doc = docx.Document(file_path)
            content = '\n'.join([para.text for para in doc.paragraphs])
        elif lower_path.endswith('.pdf'):
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                content = '\n'.join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        print(f"❌ Failed to read {os.path.relpath(file_path)}: {e}")
        return None
    
    return content

def get_file_hash(file_path):
    """Calculates the SHA256 hash of a file."""
    h = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def discover_unique_files(settings):
    """Finds all files, excluding duplicates based on content hash."""
    print(f"\n🔍 Searching for {', '.join(CONFIG['supported_extensions'])} files...")
    
    seen_hashes = set()
    unique_files = []
    output_pattern = re.compile(rf"^{re.escape(settings['base_name'])}_part\d+\.txt$", re.I)
    
    walk_path = os.getcwd()
    file_list = []
    
    if settings['include_subs']:
        for root, _, files in os.walk(walk_path):
            for f in files:
                file_list.append(os.path.join(root, f))
    else:
        file_list = [f for f in os.listdir(walk_path) if os.path.isfile(f)]
    
    file_list = [os.path.abspath(p) for p in file_list 
                 if p.lower().endswith(CONFIG['supported_extensions']) 
                 and not output_pattern.match(os.path.basename(p))]
    
    print(f"Found {len(file_list)} potential files. Calculating hashes to find uniques...")
    
    for path in tqdm(file_list, desc="Deduplicating files"):
        file_hash = get_file_hash(path)
        if file_hash and file_hash not in seen_hashes:
            seen_hashes.add(file_hash)
            unique_files.append(path)
    
    print(f"📂 Found {len(unique_files)} unique files to process.")
    unique_files.sort()
    return unique_files

def process_file_content(file_path, settings):
    """Worker function: reads, filters, and cleans a single file."""
    content = get_content_from_file(file_path)
    if not content:
        return (file_path, None)
    
    if settings['dialogue_only']:
        content = filter_dialogue_content(content, CONFIG['patterns'])
        if not content or not content.strip():
            return (file_path, "")
    
    if settings['perform_cleaning']:
        paragraphs = re.split(r'\n\s*\n', content)
        cleaned_paragraphs = [clean_paragraph(p.strip()) for p in paragraphs if p.strip()]
        content = "\n\n".join(cleaned_paragraphs)
    
    return (file_path, content)

def get_user_settings():
    """Prompts the user for all required settings."""
    settings = {}
    
    while True:
        base = input("Enter a base name for the output file(s): ").strip()
        if base:
            settings['base_name'] = re.sub(r'[^\w-]', '', base).lower()
            break
        print("An output name is required.")
    
    while True:
        size_input = input("Enter chunk size in MB (press Enter or 0 for a single file): ").strip()
        if not size_input or size_input == "0":
            settings['chunk_size_bytes'] = float('inf')
            break
        try:
            settings['chunk_size_bytes'] = int(float(size_input) * 1048576)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    settings['include_subs'] = input("Include subdirectories? (y/n): ").lower().strip() == 'y'
    settings['perform_cleaning'] = input("Perform redundancy cleaning? (y/n): ").lower().strip() == 'y'
    settings['dialogue_only'] = input("Filter for dialogues (maintaining chronological sequence)? (y/n): ").lower().strip() == 'y'
    
    return settings

def manage_existing_files(base_name):
    """Checks for existing files and returns the starting part number."""
    pattern = re.compile(rf"^{re.escape(base_name)}_part\d+\.txt$", re.I)
    
    try:
        existing = [f for f in glob.glob(f"{base_name}_part*.txt") if pattern.match(os.path.basename(f))]
    except Exception as e:
        print(f"Error checking existing files: {e}")
        return 1
    
    if not existing:
        return 1
    
    print(f"\nFound {len(existing)} existing output file(s) for base '{base_name}'.")
    choice = input("[D]elete all, [C]ontinue numbering, or [A]bort? (d/c/a): ").lower().strip()
    
    if choice == 'd':
        print("Deleting existing files...")
        for f in existing:
            os.remove(f)
        return 1
    elif choice == 'c':
        next_num = max(int(re.search(r'_part(\d+)', f, re.I).group(1)) for f in existing) + 1
        print(f"Continuing, new files will start from part {next_num}.")
        return next_num
    else:
        print("Operation cancelled.")
        exit()

def main():
    """Main function to orchestrate the entire process."""
    interrupted = False
    
    def signal_handler(sig, frame):
        nonlocal interrupted
        print("\n\n⚠️ Process interrupted by user! Exiting...")
        interrupted = True
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        print("🔧 Chronological Dialogue Processor with Sequence Preservation")
        print("   (Maintains proper dialogue sequence using timestamps and context)")
        
        settings = get_user_settings()
        start_part_num = manage_existing_files(settings['base_name'])
        unique_files = discover_unique_files(settings)
        
        if not unique_files:
            print("❌ No new files to process. Exiting.")
            return
        
        print(f"\n⚙️ Processing {len(unique_files)} files using up to {cpu_count()} CPU cores...")
        
        worker_func = partial(process_file_content, settings=settings)
        all_content = []
        
        with Pool(processes=cpu_count()) as pool:
            results_iterator = pool.imap(worker_func, unique_files)
            
            for file_path, result in tqdm(results_iterator, total=len(unique_files), desc="Processing files"):
                if interrupted:
                    pool.terminate()
                    break
                
                if result:
                    header = f"\n--- Start of {os.path.relpath(file_path)} ---\n"
                    footer = f"\n--- End of {os.path.relpath(file_path)} ---\n"
                    all_content.append(header + result + footer)
                elif result == "":
                    print(f"⏭️ Skipping {os.path.relpath(file_path)} (no dialogue content found)")
        
        if interrupted:
            raise SystemExit("Process was interrupted during file processing.")
        
        print("\n✍️ Writing content to output file(s) (chronological sequence preserved)...")
        
        current_part_file = None
        current_size = 0
        part_num = start_part_num
        output_file_count = 0
        
        final_payload = "\n".join(all_content).encode('utf-8')
        payload_written = 0
        
        while payload_written < len(final_payload):
            if not current_part_file or (settings['chunk_size_bytes'] != float('inf') and current_size >= settings['chunk_size_bytes']):
                if current_part_file:
                    current_part_file.close()
                
                output_path = f"{settings['base_name']}_part{part_num}.txt"
                current_part_file = open(output_path, 'wb')
                print(f"📁 Creating/writing to: {os.path.relpath(output_path)}")
                part_num += 1
                current_size = 0
                
                if output_file_count == 0:
                    output_file_count = 1
                else:
                    output_file_count += 1
            
            if settings['chunk_size_bytes'] == float('inf'):
                bytes_to_write = len(final_payload) - payload_written
            else:
                bytes_to_write = min(len(final_payload) - payload_written, int(settings['chunk_size_bytes'] - current_size))
            
            current_part_file.write(final_payload[payload_written:payload_written + bytes_to_write])
            payload_written += bytes_to_write
            current_size += bytes_to_write
        
        if current_part_file:
            current_part_file.close()
        
        print(f"\n✅ Success! Dialogue sequence preservation completed.")
        if output_file_count > 0:
            print(f"Created {output_file_count} output file(s) with chronological dialogue sequence preserved.")
        else:
            print("No output files created.")
    
    except (SystemExit, KeyboardInterrupt) as e:
        print(f"\n{e or 'Exiting.'}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds.")
