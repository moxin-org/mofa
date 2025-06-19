import asyncio
import websockets
import logging
import sys
import os

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_client(websocket, path):
    logger.info(f"新客户端连接: {websocket.remote_address}")
    try:
        async for message in websocket:
            logger.info(f"收到消息: {message}")
            # 回显消息
            await websocket.send(f"收到: {message}")
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"客户端断开连接: {websocket.remote_address}")

async def main():
    # 启动WebSocket服务器
    host = "0.0.0.0"
    port = 8765
    logger.info(f"启动WebSocket服务器 {host}:{port}")
    async with websockets.serve(handle_client, host, port):
        await asyncio.Future()  # 运行直到被取消

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("WebSocket服务器已停止")
        sys.exit(0)
