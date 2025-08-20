from flask import Blueprint, jsonify, request
import os
import sys
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ttyd_manager import (
    start_ttyd, stop_ttyd, restart_ttyd, get_ttyd_status, is_ttyd_installed, install_ttyd
)

# Configure logging
logger = logging.getLogger('ttyd_routes')

ttyd_bp = Blueprint('ttyd', __name__)

@ttyd_bp.route('/status', methods=['GET'])
def status():
    """Get the current status of the ttyd service"""
    status = get_ttyd_status()
    
    # Add installation status
    status['installed'] = is_ttyd_installed()
    
    return jsonify(status)

@ttyd_bp.route('/start', methods=['POST'])
def start():
    """Start the ttyd service"""
    result = start_ttyd()
    
    if result:
        status = get_ttyd_status()
        return jsonify({
            'success': True,
            'message': 'ttyd service started successfully',
            'status': status
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to start ttyd service'
        }), 500

@ttyd_bp.route('/stop', methods=['POST'])
def stop():
    """Stop the ttyd service"""
    stop_ttyd()
    
    status = get_ttyd_status()
    return jsonify({
        'success': True,
        'message': 'ttyd service stopped successfully',
        'status': status
    })

@ttyd_bp.route('/restart', methods=['POST'])
def restart():
    """Restart the ttyd service"""
    result = restart_ttyd()
    
    if result:
        status = get_ttyd_status()
        return jsonify({
            'success': True,
            'message': 'ttyd service restarted successfully',
            'status': status
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to restart ttyd service'
        }), 500

@ttyd_bp.route('/install', methods=['POST'])
def install():
    """Install ttyd if not already installed"""
    if is_ttyd_installed():
        return jsonify({
            'success': True,
            'message': 'ttyd is already installed',
            'installed': True
        })
    
    result = install_ttyd()
    
    if result:
        return jsonify({
            'success': True,
            'message': 'ttyd installed successfully',
            'installed': True
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to install ttyd',
            'installed': False
        }), 500 