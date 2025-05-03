"""
MoFA_Stage Flask 后端应用
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 引入路由
from routes.agents import agents_bp
from routes.settings import settings_bp
from routes.dataflows import dataflows_bp
from routes.terminal import terminal_bp

def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)
    
    # 配置应用
    app.config.from_pyfile('config.py')
    
    # 启用 CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 注册蓝图
    app.register_blueprint(agents_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(dataflows_bp)
    app.register_blueprint(terminal_bp)
    
    # 主页路由
    @app.route('/')
    def index():
        return jsonify({"message": "MoFA_Stage API", "status": "running"})
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "message": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"success": False, "message": "Internal server error"}), 500
    
    return app

if __name__ == '__main__':
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='MoFA_Stage Backend Server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    
    app = create_app()
    app.run(host='0.0.0.0', port=args.port, debug=True)
