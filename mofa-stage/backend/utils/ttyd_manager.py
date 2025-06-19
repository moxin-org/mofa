import os
import sys
import platform
import subprocess
import signal
import json
import time
import logging
import tempfile
import shutil
import atexit
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ttyd_manager')

# Global variables
ttyd_process = None
pid_file = os.path.join(tempfile.gettempdir(), 'mofa_ttyd.pid')
log_file = os.path.join(tempfile.gettempdir(), 'mofa_ttyd.log')

def is_ttyd_installed():
    """Check if ttyd is installed and available in PATH"""
    try:
        # Run ttyd --version to check if it's available
        result = subprocess.run(['ttyd', '--version'], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ttyd():
    """Install ttyd based on the current platform"""
    system = platform.system().lower()
    
    if system == 'linux':
        # Detect package manager
        if os.path.exists('/usr/bin/apt-get') or os.path.exists('/usr/bin/apt'):
            logger.info("Detected Debian/Ubuntu, installing ttyd using apt...")
            try:
                # Install dependencies
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run([
                    'sudo', 'apt-get', 'install', '-y', 
                    'build-essential', 'cmake', 'git', 
                    'libjson-c-dev', 'libwebsockets-dev'
                ], check=True)
                
                # Create temporary directory for build
                with tempfile.TemporaryDirectory() as tmpdir:
                    # Clone ttyd repository
                    subprocess.run([
                        'git', 'clone', 'https://github.com/tsl0922/ttyd.git', tmpdir
                    ], check=True)
                    
                    # Build and install ttyd
                    build_dir = os.path.join(tmpdir, 'build')
                    os.makedirs(build_dir, exist_ok=True)
                    
                    subprocess.run(['cmake', '..'], cwd=build_dir, check=True)
                    subprocess.run(['make'], cwd=build_dir, check=True)
                    subprocess.run(['sudo', 'make', 'install'], cwd=build_dir, check=True)
                
                logger.info("ttyd installed successfully!")
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install ttyd: {e}")
                return False
        else:
            logger.error("Unsupported Linux distribution. Please install ttyd manually.")
            return False
    
    elif system == 'darwin':  # macOS
        try:
            logger.info("Detected macOS, installing ttyd using brew...")
            # Check if Homebrew is installed
            try:
                subprocess.run(['brew', '--version'], check=True, stdout=subprocess.PIPE)
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.error("Homebrew not found. Please install Homebrew first: https://brew.sh/")
                return False
            
            # Install ttyd using Homebrew
            subprocess.run(['brew', 'install', 'ttyd'], check=True)
            logger.info("ttyd installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install ttyd: {e}")
            return False
    
    else:
        logger.error(f"Unsupported operating system: {system}. Please install ttyd manually.")
        return False

def get_settings():
    """Load settings from settings.json"""
    try:
        settings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'settings.json')
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        return settings
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        # Return default settings
        return {
            "ttyd_port": 7681,
            "mofa_dir": os.path.expanduser("~"),
        }

def get_pid_from_file():
    """Get the ttyd process ID from the PID file, if it exists"""
    try:
        if os.path.exists(pid_file):
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            return pid
        return None
    except Exception as e:
        logger.error(f"Error reading PID file: {e}")
        return None

def is_process_running(pid):
    """Check if a process with the given PID is running"""
    if pid is None:
        return False
    
    try:
        os.kill(pid, 0)  # Send signal 0 to check if process exists
        return True
    except OSError:
        return False

def stop_ttyd():
    """Stop the ttyd process if it's running"""
    global ttyd_process
    
    pid = get_pid_from_file()
    
    if pid and is_process_running(pid):
        logger.info(f"Stopping ttyd process (PID: {pid})...")
        try:
            os.kill(pid, signal.SIGTERM)
            # Wait for the process to terminate
            for _ in range(10):  # Wait up to 5 seconds
                if not is_process_running(pid):
                    break
                time.sleep(0.5)
            else:
                # Force kill if it didn't terminate
                os.kill(pid, signal.SIGKILL)
            
            logger.info("ttyd process stopped.")
        except OSError as e:
            logger.error(f"Failed to stop ttyd process: {e}")
    
    # Also terminate the process started by this script if it exists
    if ttyd_process and ttyd_process.poll() is None:
        ttyd_process.terminate()
        ttyd_process = None
    
    # Remove PID file if it exists
    if os.path.exists(pid_file):
        os.remove(pid_file)

def start_ttyd():
    """Start the ttyd service with configured settings"""
    global ttyd_process
    
    # First, ensure ttyd is installed
    if not is_ttyd_installed():
        logger.info("ttyd is not installed. Attempting to install it...")
        if not install_ttyd():
            logger.error("Failed to install ttyd. Please install it manually.")
            return False
    
    # Stop any existing ttyd process
    stop_ttyd()
    
    # Get settings
    settings = get_settings()
    ttyd_port = settings.get('ttyd_port', 7681)
    mofa_dir = settings.get('mofa_dir', os.path.expanduser("~"))
    
    # Determine working directory priority:
    # 1. mofa_dir/python if exists
    # 2. mofa_dir if exists  
    # 3. parent directory of current stage project
    # 4. home directory as fallback
    working_dir = None
    
    if mofa_dir and os.path.exists(mofa_dir):
        # Check if mofa_dir/python exists
        mofa_python_dir = os.path.join(mofa_dir, 'python')
        if os.path.exists(mofa_python_dir):
            working_dir = mofa_python_dir
            logger.info(f"Using mofa/python directory: {working_dir}")
        else:
            working_dir = mofa_dir
            logger.info(f"Using mofa directory: {working_dir}")
    else:
        # Fallback to parent of current stage directory
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend parent
        stage_parent = os.path.dirname(current_dir)  # stage parent
        if os.path.exists(stage_parent):
            working_dir = stage_parent
            logger.info(f"Using stage parent directory: {working_dir}")
        else:
            working_dir = os.path.expanduser("~")
            logger.warning(f"All preferred directories not found, using home directory: {working_dir}")
    
    # Final check
    if not os.path.exists(working_dir):
        logger.warning(f"Determined working directory '{working_dir}' doesn't exist. Using home directory instead.")
        working_dir = os.path.expanduser("~")
    
    # Get shell command from settings, fallback to zsh
    shell_cmd = settings.get('ttyd_command', 'zsh')
    
    # Prepare ttyd command with proper settings
    cmd = [
        'ttyd',
        '-p', str(ttyd_port),
        '-W',  # Allow write access
        '-w', working_dir,  # Set working directory
        # '-t', 'fontSize=14',
        # '-t', "fontFamily='Courier New',monospace",
        # '-t', 'theme={"background":"#1e1e1e","foreground":"#d4d4d4"}',
        shell_cmd
    ]
    
    logger.info(f"Starting ttyd with command: {' '.join(cmd)}")
    logger.info(f"Working directory: {working_dir}")
    
    try:
        # Open log file
        log_fd = open(log_file, 'w')
        
        # Start ttyd process
        ttyd_process = subprocess.Popen(
            cmd,
            cwd=working_dir,  # Use the determined working directory
            stdout=log_fd,
            stderr=log_fd,
            start_new_session=True  # Detach from parent process
        )
        
        # Write PID to file
        with open(pid_file, 'w') as f:
            f.write(str(ttyd_process.pid))
        
        logger.info(f"ttyd started with PID {ttyd_process.pid} on port {ttyd_port}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to start ttyd: {e}")
        return False

def restart_ttyd():
    """Restart the ttyd service"""
    stop_ttyd()
    return start_ttyd()

def get_ttyd_status():
    """Get the current status of the ttyd service"""
    pid = get_pid_from_file()
    
    if pid and is_process_running(pid):
        settings = get_settings()
        port = settings.get('ttyd_port', 7681)
        return {
            'status': 'running',
            'pid': pid,
            'port': port,
            'log_file': log_file
        }
    else:
        return {
            'status': 'stopped',
            'pid': None,
            'port': None,
            'log_file': log_file
        }

# Register cleanup function to stop ttyd when the script exits
atexit.register(stop_ttyd)

# Command-line interface for manual testing/control
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage ttyd service')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status', 'install'],
                        help='Action to perform')
    
    args = parser.parse_args()
    
    if args.action == 'start':
        start_ttyd()
    elif args.action == 'stop':
        stop_ttyd()
    elif args.action == 'restart':
        restart_ttyd()
    elif args.action == 'status':
        status = get_ttyd_status()
        print(f"ttyd status: {status['status']}")
        if status['pid']:
            print(f"PID: {status['pid']}")
            print(f"Port: {status['port']}")
    elif args.action == 'install':
        if is_ttyd_installed():
            print("ttyd is already installed.")
        else:
            print("Installing ttyd...")
            if install_ttyd():
                print("ttyd installed successfully!")
            else:
                print("Failed to install ttyd.") 