<template>
    <div class="terminal-instance">
      <div :id="terminalId" ref="terminalElement" class="terminal-element"></div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, onBeforeUnmount, nextTick, watch, onActivated } from 'vue'
  import { ElMessage } from 'element-plus'
  // Dynamically load Terminal and FitAddon if not already loaded
  // Remove reliance on global window objects
  // let Terminal = window.Terminal
  // let FitAddon = window.FitAddon
  import { Terminal } from 'xterm';
  import { FitAddon } from 'xterm-addon-fit';
  import 'xterm/css/xterm.css'; // Import xterm CSS
  
  // TODO: Implement a more robust way to ensure libraries are loaded,
  // maybe load them globally in main.js or index.html
  // Removed the TODO as we now import directly
  
  export default {
    name: 'XtermTerminalTab',
    props: {
      sessionId: {
        type: [String, Number],
        required: true
      },
      sshConfig: {
        type: Object,
        required: true,
        validator: (value) => {
          return value && value.hostname && value.username
        }
      },
      autoConnect: {
        type: Boolean,
        default: true
      }
    },
    emits: ['connected', 'disconnected', 'error', 'status-change'],
    setup(props, { emit }) {
      const terminalId = `terminal-${props.sessionId}`
      const terminalElement = ref(null)
      const isConnected = ref(false)
      
      let term = null
      let fitAddon = null
      let ws = null
  
      // Initialize terminal
      const initTerminal = async () => {
        if (!terminalElement.value) {
           console.error('Cannot initialize terminal - element missing.');
           emit('error', 'Terminal DOM element not found');
           return false;
        }
        
        // Dispose previous instance if exists
        if (term) {
          term.dispose()
          term = null
          fitAddon = null // Reset addon as well
        }
        
        // Explicitly set background color in terminal options
        term = new Terminal({
          cursorBlink: true,
          rows: 24,
          cols: 80,
          theme: {
            background: '#1e1e1e',
            foreground: '#d4d4d4',
            cursor: '#ffffff',
            selection: 'rgba(255, 255, 255, 0.3)',
            black: '#000000',
            white: '#ffffff'
          },
          fontFamily: 'Courier New, monospace',
          fontSize: 14,
          convertEol: true,
          rendererType: 'canvas' // Try forcing canvas renderer
        })
        
        fitAddon = new FitAddon()
        term.loadAddon(fitAddon)
        
        // Log before opening
        console.log('Opening terminal on element:', terminalElement.value, 'ID:', terminalId);
        
        // Ensure element is visible before attaching terminal
        terminalElement.value.style.display = 'block';
        terminalElement.value.style.height = '100%';
        terminalElement.value.style.width = '100%';
        
        term.open(terminalElement.value)
        
        // Force a proper size after opening
        term.resize(80, 24);
        
        // Handle data input from terminal -> WebSocket
        term.onData(data => {
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'input', data: data }))
          }
        })
        
        // Initial fit after a brief timeout to ensure DOM is fully ready
        setTimeout(() => {
          resizeTerminal();
          console.log('Initial terminal resize completed');
        }, 100);
        
        return true
      }
  
      // Connect to SSH server via WebSocket
      const connect = async () => {
        if (isConnected.value) {
          console.warn('Already connected or connecting.');
          return;
        }
        if (!props.sshConfig || !props.sshConfig.hostname || !props.sshConfig.username) {
          ElMessage.error('SSH configuration is incomplete.');
          emit('error', 'Incomplete SSH config');
          return;
        }
        
        // Make sure element is actually visible
        if (terminalElement.value) {
          // Force display mode
          terminalElement.value.style.display = 'block';
          terminalElement.value.style.height = '100%';
          terminalElement.value.style.minHeight = '300px';
        }
        
        // Initialize terminal first
        const terminalInitialized = await initTerminal();
        if (!terminalInitialized) {
            // Display a fallback message in the container if terminal fails to initialize
            if (terminalElement.value) {
              terminalElement.value.innerHTML = `
                <div style="color: white; background: #1e1e1e; padding: 20px; height: 100%; font-family: monospace;">
                  <h3 style="color: red">Failed to initialize terminal</h3>
                  <p>Could not create terminal instance. Please check your browser console for errors.</p>
                </div>
              `;
            }
            emit('error', 'Failed to initialize terminal');
            return;
        }
        
        term.clear()
        term.writeln('Attempting WebSocket connection...')
        emit('status-change', 'connecting')
  
        try {
          // Determine WebSocket URL (use port 5001 for WebSSH)
          const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://'
          const wsHost = window.location.hostname
          // TODO: Make port configurable? Currently hardcoded to 5001
          // const wsUrl = `${wsProtocol}${wsHost}:5001/api/webssh/ssh` // Correct backend endpoint path
          const wsUrl = `${wsProtocol}${wsHost}:5001/ssh` // Corrected endpoint path for dedicated server
          
          ws = new WebSocket(wsUrl)
          
          ws.onopen = () => {
            term.writeln('WebSocket connected. Sending SSH config...')
            // Create a sanitized config with proper field names expected by backend
            const configToSend = {
              hostname: props.sshConfig.hostname,
              port: props.sshConfig.port || 22,
              username: props.sshConfig.username,
              password: props.sshConfig.password || ''
            };
            
            // Log config (without password) for debugging
            console.log('Sending SSH config:', {...configToSend, password: configToSend.password ? '********' : ''});
            
            // Send SSH configuration as the first message
            ws.send(JSON.stringify(configToSend))
            
            // Send initial terminal size after config is sent
            resizeTerminal() // Ensure size is sent after connection established
          }
          
          ws.onmessage = (event) => {
            try {
               // First check if it's our JSON control messages
               if (typeof event.data === 'string') {
                  try {
                      const message = JSON.parse(event.data);
                      if (message.type === 'error') {
                          term.writeln(`\r\n\x1b[31mError: ${message.data}\x1b[0m`);
                          emit('error', message.data);
                          disconnect(); // Close on backend error message
                      } else if (message.type === 'status') {
                          term.writeln(`\r\n\x1b[33mStatus: ${message.data}\x1b[0m`);
                          if (message.data.includes('SSH Connected')) {
                              isConnected.value = true;
                              emit('connected');
                              emit('status-change', 'connected');
                          }
                      } else {
                           // Unknown JSON message type? Log it.
                           console.warn('Received unknown JSON message type:', message);
                           term.write(event.data); // Write raw if unknown
                      }
                      return; // Handled as JSON
                  } catch(e) {
                      // Not JSON, treat as terminal data
                      term.write(event.data);
                  }
               } else {
                   // Handle Blob data if necessary (though backend sends strings)
                   // Example: Convert blob to string or handle binary data
                   console.warn('Received non-string data:', event.data);
                   // term.write(await event.data.text()); // Example for Blob
               }
            } catch(e) {
              // If parsing fails or writing fails, log error
              console.error('Error processing WebSocket message:', e, event.data)
              term.writeln(`\r\n\x1b[31mInternal Error processing message.\x1b[0m`)
            }
          }
          
          ws.onerror = (event) => {
            term.writeln('\r\n\x1b[31mWebSocket Error.\x1b[0m')
            console.error("WebSocket Error:", event)
            emit('error', 'WebSocket connection error')
            disconnect() // Disconnect on error
          }
          
          ws.onclose = (event) => {
            if (isConnected.value) { // Only show message if we were previously connected
               term.writeln(`\r\n\x1b[31mConnection Closed. Code: ${event.code}, Reason: ${event.reason || '-'}\x1b[0m`)
            } else if (term) { // If not connected, maybe connection failed
                term.writeln(`\r\n\x1b[31mConnection attempt failed or closed prematurely.\x1b[0m`);
            }
            isConnected.value = false
            emit('disconnected')
            emit('status-change', 'disconnected')
            ws = null // Clear WebSocket reference
          }
        } catch (error) {
          console.error('Failed to establish WebSocket connection:', error)
          if(term) term.writeln(`\r\n\x1b[31mError setting up connection: ${error.message}\x1b[0m`)
          emit('error', `Connection setup error: ${error.message}`)
          disconnect() // Ensure cleanup on error
        }
      }
  
      // Disconnect WebSocket
      const disconnect = () => {
        if (ws) {
          ws.close()
          // ws = null // ws will be set to null in onclose handler
        }
        // Don't dispose terminal here, just mark as disconnected
        // The parent component might want to show the last state
        if (isConnected.value) {
            isConnected.value = false;
            // emit('disconnected') // Emitted by onclose handler
            // emit('status-change', 'disconnected') // Emitted by onclose handler
        }
         if (term) {
            term.writeln('\r\n\x1b[33mDisconnecting...\x1b[0m');
        }
      }
  
      // Resize terminal and notify backend
      const resizeTerminal = () => {
         // Debounce or throttle this if it gets called too frequently
         nextTick(() => { // Ensure the DOM element dimensions are updated
             // Check if the terminal element is actually visible and has dimensions
             if (fitAddon && term && terminalElement.value && terminalElement.value.clientHeight > 0) {
                  try {
                      fitAddon.fit()
                      // Corrected method call: fitAddon.proposeDimensions()
                      // const dimensions = term.proposeGeometry()
                      const dimensions = fitAddon.proposeDimensions()
                      if (ws && ws.readyState === WebSocket.OPEN && dimensions) {
                          ws.send(JSON.stringify({
                              type: 'resize',
                              cols: dimensions.cols || 80,
                              rows: dimensions.rows || 24
                          }))
                      } else if (!dimensions) {
                          console.warn('fitAddon.proposeDimensions() returned undefined');
                      }
                  } catch (e) {
                      console.error('Error during terminal resize:', e);
                  }
             }
         });
      }
  
      // Lifecycle hooks
      onMounted(() => {
         // Directly try to connect if autoConnect is true
         if (props.autoConnect) {
             connect();
         }
         // Add window resize listener
         window.addEventListener('resize', resizeTerminal)
      })
      
      // Handle component activation (when parent is re-shown)
      onActivated(() => {
        console.log(`Terminal ${props.sessionId} activated`);
        // When the component is re-activated, make sure to resize it
        nextTick(() => {
          resizeTerminal();
        });
      })
  
      onBeforeUnmount(() => {
        disconnect() // Ensure connection is closed
        if (term) {
          term.dispose() // Dispose terminal instance
          term = null
          fitAddon = null
        }
         window.removeEventListener('resize', resizeTerminal)
      })
      
      // Watch for config changes (optional, might not be needed if config is fixed per tab)
      // watch(() => props.sshConfig, (newConfig, oldConfig) => {
      //   if (JSON.stringify(newConfig) !== JSON.stringify(oldConfig)) {
      //     console.log('SSH config changed, consider reconnecting.');
      //     // Optionally disconnect and reconnect, or just update internal state
      //     // disconnect();
      //     // nextTick(connect);
      //   }
      // }, { deep: true });
  
      // Expose methods to parent component if needed via template refs
      // (Not standard setup script way, use defineExpose)
      
      // Using defineExpose to make methods callable from parent ref
      // No need for defineExpose in Vue 3 <script setup> if using standard <script>
      // If using <script setup>, use: defineExpose({ connect, disconnect, resizeTerminal });
  
      return {
        terminalId,
        terminalElement,
        isConnected,
        // Expose methods for parent component via ref
        connect,
        disconnect,
        resizeTerminal,
      }
    }
  }
  </script>
  
  <style scoped>
  .terminal-instance {
    width: 100%;
    height: 100%; /* Ensure terminal takes full height of its container */
    background-color: #1e1e1e; /* Match terminal theme */
    display: flex;
    flex-direction: column;
    padding: 0;
    margin: 0;
    border-radius: 4px;
    overflow: hidden;
  }
  
  /* Style for the div xterm attaches to */
  .terminal-element {
    flex-grow: 1;
    min-height: 300px; /* Ensure a minimum height */
    background-color: #1e1e1e; /* Match terminal theme */
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
  
  /* Deeper styling for xterm elements */
  :deep(.xterm) {
    height: 100%;
  }
  
  :deep(.xterm-viewport) {
    background-color: #1e1e1e !important; /* Force background color */
    overflow: auto;
  }
  
  :deep(.xterm-screen) {
    height: 100% !important;
  }
  
  /* Scroll styling for terminal */
  :deep(.xterm-viewport::-webkit-scrollbar) {
    width: 8px;
  }
  
  :deep(.xterm-viewport::-webkit-scrollbar-track) {
    background: #1e1e1e;
  }
  
  :deep(.xterm-viewport::-webkit-scrollbar-thumb) {
    background-color: #555;
    border-radius: 4px;
  }
  </style> 