"""
WebSSH related API routes with SSH terminal support via WebSocket
"""
from flask import Blueprint, render_template, request, jsonify
from flask_sock import Sock
import os
import json
import logging
import paramiko
import threading
import uuid

# Import active_sessions from terminal.py
from routes.terminal import active_sessions

# Add project root directory to Python path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create blueprint
webssh_bp = Blueprint('webssh', __name__, url_prefix='/api/webssh')

# Initialize Sock for WebSocket support
sock = None

# Buffer size for SSH data
BUFFER_SIZE = 1024 * 16  # 16KB buffer

# Configure logging
logging.basicConfig(level=logging.INFO)

def init_websocket(app):
    """Initialize WebSocket for the app"""
    global sock
    sock = Sock(app)
    
    @sock.route('/ssh')
    def ssh_websocket(ws):
        """Handles WebSocket connections for the SSH terminal"""
        logging.info("WebSocket connection received for SSH terminal")
        
        try:
            # Get connection parameters from the first message
            config_data = ws.receive()
            logging.info(f"Received config data: {config_data[:50]}...")
            config = json.loads(config_data)
            
            # Start SSH interaction
            ssh_interaction(ws, config)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in SSH WebSocket: {e}")
            try:
                ws.send(json.dumps({"type": "error", "data": "Invalid connection parameters. Please check your input."})) 
            except:
                pass
        except Exception as e:
            logging.error(f"Error in SSH WebSocket: {e}")
            try:
                ws.send(json.dumps({"type": "error", "data": f"Connection error: {str(e)}"}))
            except:
                pass
        
        logging.info("WebSocket connection closed")

def ssh_interaction(ws, config):
    """Handles the SSH connection and data transfer"""
    ssh = None
    channel = None
    session_id = str(uuid.uuid4())
    try:
        # 1. Check Config
        if not all([config.get('hostname'), config.get('username')]):
            ws.send(json.dumps({"type": "error", "data": "Hostname and Username are required."}))
            logging.warning("SSH connection aborted: Missing hostname or username in config.")
            return
        
        hostname = config['hostname']
        port = int(config.get('port', 22))
        username = config['username']
        password = config.get('password', '')
        
        # 2. Establish SSH Connection
        logging.info(f"Attempting SSH connection to {username}@{hostname}:{port}")
        ws.send(json.dumps({"type": "status", "data": f"Connecting to {username}@{hostname}:{port}..."}))
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            ssh.connect(hostname, port=port, username=username, password=password, look_for_keys=True)
        except paramiko.AuthenticationException:
            logging.warning(f"Authentication failed for {username}@{hostname}")
            ws.send(json.dumps({"type": "error", "data": "Authentication failed (Incorrect password or key?)."}))
            return
        except Exception as e:
            logging.error(f"SSH connection error to {hostname}:{port}: {e}")
            ws.send(json.dumps({"type": "error", "data": f"Connection Error: {e}"}))
            return
        
        logging.info(f"SSH connection established to {username}@{hostname}")
        ws.send(json.dumps({"type": "status", "data": "SSH Connected."}))
        
        # Store websocket in active_sessions for system info updates
        active_sessions[session_id] = {
            'process': None,  # No actual process for SSH sessions
            'cwd': '/',
            'env': {},
            'use_system_mofa': False,
            'mofa_env_path': '',
            'mofa_dir': '',
            'running_process': None,
            'websocket': ws,
            'ssh_client': ssh,
            'ssh_channel': None,  # Will be set below
            'hostname': hostname,
            'username': username
        }
        
        # 3. Open SSH Shell Channel
        channel = ssh.invoke_shell(term='xterm-256color', width=80, height=24)
        channel.settimeout(0.0)  # Non-blocking
        
        # Store channel in active_sessions
        if session_id in active_sessions:
            active_sessions[session_id]['ssh_channel'] = channel
        
        # 4. Bridge WebSocket and SSH Channel
        while True:
            try:
                # Read from SSH -> Send to WS
                if channel.recv_ready():
                    ssh_data = channel.recv(BUFFER_SIZE)
                    if not ssh_data:  # Channel closed
                        logging.info("SSH channel closed by remote end.")
                        break
                    # Send raw data to the client
                    try:
                        ws.send(ssh_data.decode('utf-8', errors='replace'))
                    except Exception as e:
                        logging.error(f"Error sending data to WebSocket: {e}")
                        break
                
                # Read from WS -> Send to SSH
                try:
                    ws_data_str = ws.receive(timeout=0.01)  # Small timeout
                    if ws_data_str:
                        try:
                            ws_data = json.loads(ws_data_str)
                            if ws_data.get('type') == 'input':
                                channel.send(ws_data['data'])
                            elif ws_data.get('type') == 'resize':
                                cols = ws_data.get('cols', 80)
                                rows = ws_data.get('rows', 24)
                                channel.resize_pty(width=cols, height=rows)
                                logging.debug(f"Resized PTY to {cols}x{rows}")
                        except json.JSONDecodeError:
                            logging.warning(f"Received non-JSON data on WebSocket: {ws_data_str[:50]}...")
                        except Exception as e:
                            logging.error(f"Error processing WebSocket message: {e}")
                except TimeoutError:  # From ws.receive(timeout=...)
                    pass  # No data received, continue
                except Exception as e:
                    if 'Connection closed' in str(e):
                        logging.info("WebSocket connection closed by client")
                        break
                    logging.error(f"Error receiving data from WebSocket: {e}")
                    break
                
                if not channel.active:
                    logging.info("SSH channel became inactive.")
                    break
                
            except Exception as e:
                logging.error(f"Error during SSH/WS bridge: {e}", exc_info=True)
                try:
                    ws.send(json.dumps({"type": "error", "data": f"Runtime Error: {e}"}))
                except:
                    pass  # Ignore if we can't send the error
                break
    
    except Exception as e:
        logging.error(f"Unexpected error in ssh_interaction: {e}", exc_info=True)
        try:
            ws.send(json.dumps({"type": "error", "data": f"Internal Server Error: {e}"}))
        except Exception:
            pass  # Ignore if we can't even send the error
    finally:
        logging.info("Closing SSH connection and channel.")
        if channel:
            channel.close()
        if ssh:
            ssh.close()
            
        # Remove session from active_sessions
        if session_id in active_sessions:
            del active_sessions[session_id]
            logging.info(f"Removed WebSSH session {session_id} from active_sessions")

@webssh_bp.route('/config', methods=['GET', 'POST'])
def ssh_config():
    """Handle SSH configuration"""
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"success": False, "message": "Request must be JSON"}), 400
        
        config_data = request.json
        return jsonify({
            "success": True,
            "message": "SSH configuration received"
        })
    else:
        # Return default configuration
        return jsonify({
            "success": True,
            "config": {
                "hostname": "",
                "port": 22,
                "username": "",
                "password": ""
            }
        })

@webssh_bp.route('/platform', methods=['GET'])
def get_platform_info():
    """Get platform information for WebSSH"""
    import platform
    import getpass
    import socket
    
    system = platform.system()
    release = platform.release()
    
    platform_info = f"{system} {release}"
    
    # Get username and hostname
    try:
        username = getpass.getuser()
        hostname = socket.gethostname()
    except Exception as e:
        logging.error(f"Error getting username/hostname: {e}")
        username = "user"
        hostname = "localhost"
    
    # Add more detailed information for different platforms
    if system == "Windows":
        platform_info += " (For Windows users, we recommend using WSL for better compatibility)"
    elif system == "Linux":
        # Check if running in WSL
        if os.path.exists('/proc/version'):
            with open('/proc/version', 'r') as f:
                if 'microsoft' in f.read().lower():
                    platform_info += " (Running in Windows Subsystem for Linux)"
    
    return jsonify({
        "success": True,
        "platform": platform_info,
        "system_info": {
            "username": username,
            "hostname": hostname,
            "platform": system
        }
    })
