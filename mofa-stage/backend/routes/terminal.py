"""
Terminal related API routes with embedded terminal session support
"""
from flask import Blueprint, request, jsonify
import os
import sys
import platform
import subprocess
import uuid
import shlex
import threading
import time
import json
import psutil
from datetime import datetime
from pathlib import Path

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.file_ops import read_file, write_file
from config import DEFAULT_MOFA_ENV, DEFAULT_MOFA_DIR, USE_SYSTEM_MOFA

terminal_bp = Blueprint('terminal', __name__, url_prefix='/api/terminal')

# Store active terminal sessions
# Format: {session_id: {process: subprocess.Popen, cwd: str, env: dict, use_system_mofa: bool, mofa_env_path: str, mofa_dir: str, running_process: subprocess.Popen, websocket: object}}
active_sessions = {}

# Session cleanup thread
def cleanup_inactive_sessions():
    while True:
        time.sleep(300)  # Check every 5 minutes
        sessions_to_remove = []
        
        for session_id, session_data in active_sessions.items():
            # Check if process exists and is still alive
            if 'process' in session_data and session_data['process'] is not None:
                if session_data['process'].poll() is not None:
                    sessions_to_remove.append(session_id)
            else:
                # If process is None or doesn't exist, mark for removal
                sessions_to_remove.append(session_id)
        
        # Remove dead sessions
        for session_id in sessions_to_remove:
            try:
                if session_id in active_sessions and 'process' in active_sessions[session_id] and active_sessions[session_id]['process']:
                    active_sessions[session_id]['process'].terminate()
            except:
                pass
            if session_id in active_sessions:
                del active_sessions[session_id]
                print(f"Cleaned up inactive session: {session_id}")

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_inactive_sessions, daemon=True)
cleanup_thread.start()

# Function to get system information
def get_system_info():
    """Get system information for display in terminal"""
    try:
        # Get basic system info
        uptime = time.time() - psutil.boot_time()
        uptime_str = f"{int(uptime // 86400)}d {int((uptime % 86400) // 3600)}h {int((uptime % 3600) // 60)}m"
        
        # Get load average
        load_avg = psutil.getloadavg()
        load_avg_str = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
        
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_used_percent = memory.percent
        memory_str = f"{memory_used_percent}% ({memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB)"
        
        return {
            "uptime": uptime_str,
            "loadAverage": load_avg_str,
            "memoryUsage": memory_str,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"Error getting system info: {e}")
        return {
            "uptime": "Error",
            "loadAverage": "Error",
            "memoryUsage": "Error",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

# Function to periodically send system info to connected websockets
def send_system_info():
    while True:
        time.sleep(5)  # Update every 5 seconds
        system_info = get_system_info()
        
        # Send to all active sessions with websockets
        for session_id, session_data in active_sessions.items():
            if 'websocket' in session_data and session_data['websocket']:
                try:
                    message = json.dumps({
                        "type": "system_info",
                        "data": system_info
                    })
                    session_data['websocket'].send(message)
                except Exception as e:
                    print(f"Error sending system info to session {session_id}: {e}")

# # Start system info thread
# system_info_thread = threading.Thread(target=send_system_info, daemon=True)
# system_info_thread.start()

@terminal_bp.route('/platform', methods=['GET'])
def get_platform_info():
    """Get platform information"""
    system = platform.system()
    release = platform.release()
    
    platform_info = f"{system} {release}"
    
    # Get username and hostname
    try:
        import getpass
        import socket
        username = getpass.getuser()
        hostname = socket.gethostname()
    except Exception as e:
        print(f"Error getting username/hostname: {e}")
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

@terminal_bp.route('/session', methods=['GET', 'POST'])
def create_terminal_session():
    """Create a new terminal session with the configured MoFA environment"""
    if request.method == 'GET':
        # Return active sessions info
        sessions_info = {}
        for session_id, session in active_sessions.items():
            sessions_info[session_id] = {
                "cwd": session.get('cwd', ''),
                "use_system_mofa": session.get('use_system_mofa', USE_SYSTEM_MOFA),
                "mofa_dir": session.get('mofa_dir', DEFAULT_MOFA_DIR),
                "active": session.get('process') and session.get('process').poll() is None
            }
        return jsonify({"success": True, "sessions": sessions_info})
    
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400
    
    data = request.json
    use_system_mofa = data.get('use_system_mofa', USE_SYSTEM_MOFA)
    mofa_env_path = data.get('mofa_env_path', DEFAULT_MOFA_ENV)
    mofa_dir = data.get('mofa_dir', DEFAULT_MOFA_DIR)
    
    # Check if the required directories exist
    if not os.path.exists(mofa_dir):
        return jsonify({
            "success": False,
            "message": f"MoFA directory does not exist: {mofa_dir}"
        }), 400
    
    if not use_system_mofa and not os.path.exists(mofa_env_path):
        return jsonify({
            "success": False,
            "message": f"MoFA environment path does not exist: {mofa_env_path}"
        }), 400
    
    try:
        # Create a unique session ID
        session_id = str(uuid.uuid4())
        
        # Set up environment variables
        env = os.environ.copy()
        
        # Create a shell process that will handle commands
        if use_system_mofa:
            # Using system MOFA
            shell_cmd = 'bash'
        else:
            # Using virtual environment
            # We'll activate the virtual environment in the first command
            shell_cmd = 'bash'
        
        # Start the shell process
        process = subprocess.Popen(
            shell_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            cwd=mofa_dir,
            env=env
        )
        
        # Store session data
        active_sessions[session_id] = {
            'process': process,
            'cwd': mofa_dir,
            'env': env,
            'use_system_mofa': use_system_mofa,
            'mofa_env_path': mofa_env_path,
            'mofa_dir': mofa_dir
        }
        
        # Prepare welcome message
        welcome_message = "Terminal session initialized. "
        if use_system_mofa:
            welcome_message += "Using system installed MOFA."
        else:
            welcome_message += f"Using virtual environment at {mofa_env_path}."
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": welcome_message,
            "cwd": mofa_dir
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to create terminal session: {str(e)}"
        }), 500

@terminal_bp.route('/execute', methods=['POST'])
def execute_command():
    """Execute a command in an existing terminal session"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400
    
    data = request.json
    session_id = data.get('session_id', '')
    command = data.get('command', '').strip()
    
    if not session_id or session_id not in active_sessions:
        return jsonify({
            "success": False,
            "message": "Invalid or expired session ID"
        }), 400
    
    if not command:
        return jsonify({
            "success": False,
            "message": "No command provided"
        }), 400
    
    session = active_sessions[session_id]
    
    try:
        # Handle special commands
        if command == 'clear':
            return jsonify({
                "success": True,
                "output": "",
                "cwd": session['cwd']
            })
        
        # Handle cd commands specially to track current directory
        if command.startswith('cd '):
            path = command[3:].strip()
            
            # Handle relative paths
            if not os.path.isabs(path):
                path = os.path.normpath(os.path.join(session['cwd'], path))
            
            # Check if directory exists
            if not os.path.isdir(path):
                return jsonify({
                    "success": False,
                    "message": f"Directory not found: {path}"
                })
            
            # Update current working directory
            old_cwd = session['cwd']
            session['cwd'] = path
            
            return jsonify({
                "success": True,
                "output": "",
                "cwd": path,
                "old_cwd": old_cwd  # Send the old working directory for reference
            })
        
        # For activating virtual environment
        if command == 'activate' and not session['use_system_mofa']:
            activate_cmd = f"source {session['mofa_env_path']}/bin/activate"
            result = execute_shell_command(session, activate_cmd)
            return jsonify({
                "success": True,
                "output": "Virtual environment activated",
                "cwd": session['cwd']
            })
        
        # Execute the command
        result = execute_shell_command(session, command)
        
        return jsonify({
            "success": True,
            "output": result,
            "cwd": session['cwd']
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to execute command: {str(e)}"
        }), 500

def execute_shell_command(session, command):
    """Execute a shell command and return the output"""
    try:
        # Special handling for interactive commands
        if command.strip() == 'python' or command.strip() == 'python3' or 'shell' in command:
            return f"Interactive shells like '{command}' are not supported in the web terminal. \nPlease use specific commands or scripts instead."
        
        # Create a temporary script to execute the command
        script_content = f"cd {session['cwd']} && {command} 2>&1"
        
        # Execute the command and store the process reference
        process = subprocess.Popen(
            ['bash', '-c', script_content],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=session['cwd'],
            env=session['env']
        )
        
        # Store the running process in the session
        session['running_process'] = process
        
        try:
            # Wait for the process to complete with a timeout
            stdout, stderr = process.communicate(timeout=60)
            
            # Clear the running process reference
            session['running_process'] = None
            
            # Return combined stdout and stderr
            return stdout + stderr
        except subprocess.TimeoutExpired:
            # If the process is taking too long, don't terminate it but return what we have
            session['running_process'] = process
            return "Command is still running..."
        
    except Exception as e:
        # Make sure to clear the running process reference
        session['running_process'] = None
        return f"Error executing command: {str(e)}"

@terminal_bp.route('/interrupt', methods=['POST'])
def interrupt_command():
    """Interrupt a running command (Ctrl+C)"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400
    
    data = request.json
    session_id = data.get('session_id', '')
    
    if not session_id or session_id not in active_sessions:
        return jsonify({
            "success": False,
            "message": "Invalid or expired session ID"
        }), 400
    
    session = active_sessions[session_id]
    
    try:
        # Check if there's a running process to interrupt
        if 'running_process' in session and session['running_process'] is not None:
            # Send SIGINT (Ctrl+C) to the process
            session['running_process'].send_signal(subprocess.signal.SIGINT)
            
            # Wait a short time for the process to handle the signal
            try:
                session['running_process'].wait(timeout=2)
            except subprocess.TimeoutExpired:
                # If it's still running after timeout, force terminate
                session['running_process'].terminate()
            
            # Clear the running process reference
            session['running_process'] = None
            
            return jsonify({
                "success": True,
                "message": "Command interrupted"
            })
        else:
            return jsonify({
                "success": False,
                "message": "No running command to interrupt"
            })
    except Exception as e:
        # Ensure running_process is cleared even if an exception occurs
        if 'running_process' in session:
            session['running_process'] = None
        return jsonify({
            "success": False,
            "message": f"Failed to interrupt command: {str(e)}"
        }), 500

@terminal_bp.route('/close', methods=['POST'])
def close_session():
    """Close a terminal session"""
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400
    
    data = request.json
    session_id = data.get('session_id', '')
    
    if not session_id or session_id not in active_sessions:
        return jsonify({
            "success": False,
            "message": "Invalid or expired session ID"
        }), 400
    
    try:
        # Terminate any running process
        if 'running_process' in active_sessions[session_id] and active_sessions[session_id]['running_process'] is not None:
            active_sessions[session_id]['running_process'].terminate()
        
        # Terminate the shell process
        if 'process' in active_sessions[session_id] and active_sessions[session_id]['process'] is not None:
            active_sessions[session_id]['process'].terminate()
        
        # Remove the session
        del active_sessions[session_id]
        
        return jsonify({
            "success": True,
            "message": "Terminal session closed"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to close terminal session: {str(e)}"
        }), 500
