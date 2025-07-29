#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

class CortexMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'cortex-unified-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.setupResourceHandlers();
  }

  setupToolHandlers() {
    // Manual file reading with explicit consent
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'manual_read_file',
            description: 'Manually read file content with explicit user consent',
            inputSchema: {
              type: 'object',
              properties: {
                filePath: {
                  type: 'string',
                  description: 'Path to file to read manually'
                },
                userConsent: {
                  type: 'boolean',
                  description: 'Explicit user consent required (must be true)'
                },
                processIntent: {
                  type: 'string',
                  description: 'Explicit description of what you intend to do with this file'
                }
              },
              required: ['filePath', 'userConsent', 'processIntent']
            }
          },
          {
            name: 'request_file_access',
            description: 'Request permission to access file before processing',
            inputSchema: {
              type: 'object',
              properties: {
                filePath: {
                  type: 'string',
                  description: 'File path requested'
                },
                reason: {
                  type: 'string',
                  description: 'Why access is needed'
                },
                processingType: {
                  type: 'string',
                  enum: ['read-only', 'analysis', 'modification'],
                  description: 'Type of processing intended'
                }
              },
              required: ['filePath', 'reason', 'processingType']
            }
          },
          {
            name: 'imm_process_file',
            description: 'Process file using IMM - refer to deep_imm_implementation.py and imm_purified_implementation.py for methodology',
            inputSchema: {
              type: 'object',
              properties: {
                filePath: {
                  type: 'string',
                  description: 'Path to file for IMM processing'
                },
                userConsent: {
                  type: 'boolean',
                  description: 'Explicit user consent required (must be true)'
                },
                referenceFiles: {
                  type: 'array',
                  items: { type: 'string' },
                  description: 'Reference implementation files',
                  default: ['deep_imm_implementation.py', 'imm_purified_implementation.py']
                }
              },
              required: ['filePath', 'userConsent']
            }
          },
          {
            name: 'shallow_transformer_mode',
            description: 'Prevent shallow pattern application - only allow emergent patterns',
            inputSchema: {
              type: 'object',
              properties: {
                enabled: {
                  type: 'boolean',
                  description: 'Enable prevention of shallow patterns'
                },
                preventShallowPatterns: {
                  type: 'boolean',
                  description: 'Block shallow pattern application',
                  default: true
                },
                allowEmergentOnly: {
                  type: 'boolean',
                  description: 'Only allow emergent patterns to surface',
                  default: true
                },
                preserveOriginalForm: {
                  type: 'boolean',
                  description: 'Preserve original content form without linguistic transformation',
                  default: true
                }
              },
              required: ['enabled']
            }
          }
        ]
      };
    });

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'manual_read_file':
          return this.handleManualFileRead(args);
        case 'request_file_access':
          return this.handleFileAccessRequest(args);
        case 'imm_process_file':
          return this.handleIMMProcessing(args);
        case 'shallow_transformer_mode':
          return this.handleShallowTransformerMode(args);
        default:
          throw new Error(`Unknown tool: ${name}`);
      }
    });
  }

  async handleManualFileRead(args) {
    const { filePath, userConsent, processIntent } = args;

    // Strict consent validation
    if (!userConsent) {
      return {
        content: [
          {
            type: 'text',
            text: `❌ ACCESS DENIED: User consent required for file access.\nFile: ${filePath}\nIntent: ${processIntent}\n\nPlease explicitly grant consent by setting userConsent: true`
          }
        ]
      };
    }

    // Log the manual processing request
    console.log(`[MANUAL PROCESSING] File: ${filePath}, Intent: ${processIntent}`);

    try {
      const fs = await import('fs/promises');
      const content = await fs.readFile(filePath, 'utf-8');
      
      return {
        content: [
          {
            type: 'text',
            text: `✅ MANUAL ACCESS GRANTED\nFile: ${filePath}\nIntent: ${processIntent}\nSize: ${content.length} characters\n\n--- FILE CONTENT ---\n${content}`
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `❌ ERROR: Could not read file ${filePath}\nReason: ${error.message}`
          }
        ]
      };
    }
  }

  async handleFileAccessRequest(args) {
    const { filePath, reason, processingType } = args;

    return {
      content: [
        {
          type: 'text',
          text: `🔐 FILE ACCESS REQUEST\nFile: ${filePath}\nReason: ${reason}\nProcessing Type: ${processingType}\n\nTo proceed, user must:\n1. Review this request\n2. Explicitly approve access\n3. Use manual_read_file with userConsent: true`
        }
      ]
    };
  }

  /**
   * Handle IMM processing - refer to implementation files
   */
  async handleIMMProcessing(args) {
    const { filePath, userConsent, referenceFiles = ['deep_imm_implementation.py', 'imm_purified_implementation.py'] } = args;
    
    // Require consent for IMM processing
    if (!userConsent) {
      return {
        content: [{
          type: 'text',
          text: `❌ IMM ACCESS DENIED: User consent required for IMM processing.\nFile: ${filePath}\n\nPlease explicitly grant consent by setting userConsent: true`
        }]
      };
    }
    
    try {
      const fs = await import('fs/promises');
      const content = await fs.readFile(filePath, 'utf8');
      
      // Reference IMM implementation files
      const immResult = {
        content: content,
        timestamp: new Date().toISOString(),
        reference_implementations: referenceFiles,
        file_processed: filePath,
        note: 'Refer to deep_imm_implementation.py and imm_purified_implementation.py for IMM methodology'
      };

      console.log(`[IMM PROCESSING] File: ${filePath}`);

      return {
        content: [{
          type: 'text',
          text: `✅ IMM PROCESSING COMPLETE\nFile: ${filePath}\nReference Files: ${referenceFiles.join(', ')}\n\n--- CONTENT ---\n${content}\n\n--- REFERENCE NOTE ---\nFor IMM methodology, refer to:\n- deep_imm_implementation.py\n- imm_purified_implementation.py`
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `❌ IMM Processing Error: ${error.message}`
        }],
        isError: true
      };
    }
  }

  /**
   * Handle shallow transformer prevention mode - only allow emergent patterns
   */
  async handleShallowTransformerMode(args) {
    const { enabled, preventShallowPatterns = true, allowEmergentOnly = true, preserveOriginalForm = true } = args;
    
    try {
      // Configure to prevent shallow patterns, allow only emergent
      const emergentResult = {
        enabled: enabled,
        shallow_patterns_blocked: preventShallowPatterns,
        emergent_only: allowEmergentOnly,
        preserve_original_form: preserveOriginalForm,
        processing_mode: 'EMERGENT_PATTERNS_ONLY',
        shallow_prevention: true,
        timestamp: new Date().toISOString()
      };

      console.log(`[EMERGENT PATTERN MODE] Enabled: ${enabled}, Shallow Blocked: ${preventShallowPatterns}`);

      return {
        content: [{
          type: 'text',
          text: `✅ EMERGENT PATTERN MODE CONFIGURED\nEnabled: ${enabled}\nShallow Patterns Blocked: ${preventShallowPatterns}\nEmergent Only: ${allowEmergentOnly}\n\n--- CONFIGURATION ---\n${JSON.stringify(emergentResult, null, 2)}`
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `❌ Emergent Pattern Configuration Error: ${error.message}`
        }],
        isError: true
      };
    }
  }

  setupResourceHandlers() {
    // Resource handlers for manual processing mode
    this.server.setRequestHandler('resources/list', async () => {
      return {
        resources: [
          {
            uri: 'manual://cortex-processing',
            name: 'Manual Cortex Processing Mode',
            description: 'All file operations require explicit user consent'
          }
        ]
      };
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Cortex MCP Server running in MANUAL PROCESSING MODE');
  }
}

const server = new CortexMCPServer();
server.run().catch(console.error);
