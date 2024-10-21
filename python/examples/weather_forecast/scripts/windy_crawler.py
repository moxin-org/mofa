import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import io
import sys
import base64
import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output, load_node_result
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path, make_dir
from mofa.utils.log.agent import record_agent_result_log

import os
from typing import Optional

from langchain_community.utilities import SearchApiAPIWrapper
from pydantic import Field

# 映射要素名称到URL片段
ELEMENT_URL_MAP = {
    '气象雷达': ('%E6%B0%94%E8%B1%A1%E9%9B%B7%E8%BE%BE-radar', 'radar'),
    '卫星云图': ('%E5%8D%AB%E6%98%9F云图-satellite', 'satellite'),
    'Radar+': ('Radar+-radarPlus', 'radarPlus'),
    '雨、雷暴': ('%E9%9B%AA%E3%80%81%E9%9B%B7暴-rain', 'rain'),
    '温度': ('%E6%B8%A9度-temp', 'temp'),
    '云': ('%E4%BA%91-clouds', 'clouds'),
    '海浪': ('%E6%B5%B7%E6%B5%AA-waves', 'waves'),
    '降雨量': ('%E9%99%8D%E9%9B%A8%E9%87%8F-rainAccu?rainAccu,next3d', 'rainAccu,next3d'),
    '风': ('', ''),
    # 添加更多要素名称和对应的URL片段
}


class WindyImageDownloader():
    """从Windy.com自动下载气象图的脚本
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 自动下载和安装匹配的ChromeDriver
        chromedriver_autoinstaller.install()

    def execute(self, url: str, output_path: Optional[str] = "windy_image.png"):
        # 创建一个新的浏览器实例

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 无头模式
        options.add_argument('--disable-gpu')  # 禁用GPU
        options.add_argument('--start-maximized')  # 设置窗口大小

        # 创建一个Service实例（不需要指定路径，chromedriver_autoinstaller已处理）
        service = Service()

        driver = webdriver.Chrome(service=service, options=options)

        try:
            # 打开Windy.com的页面
            driver.get(url)

            # 处理可能出现的警报弹窗
            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print("Alert accepted.")
            except:
                print("No alert present.")

            # 等待页面加载完成
            wait = WebDriverWait(driver, 20)  # 增加等待时间
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "leaflet-pane")))

            # 给一点额外的时间让地图完全加载
            time.sleep(5)

            # 截取屏幕快照
            screenshot = driver.get_screenshot_as_png()

            # 保存图片到本地
            with open(output_path, "wb") as f:
                f.write(screenshot)

            # 使用io.BytesIO处理截图
            buffered = io.BytesIO()
            buffered.write(screenshot)

            # 将图像转换为Base64编码
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # 返回Base64编码的图像字符串
            return img_str

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            # 关闭浏览器
            driver.quit()



class Operator:
    @property
    def now_date(self,):
        from datetime import datetime

        # 获取当前日期和时间
        now = datetime.now()

        # 格式化为字符串
        current_time_str = now.strftime('%Y%m%d_%H%M%S')

        return current_time_str
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event["id"] == 'geolocation_response':
                geolocation_response = load_node_result(dora_event["value"][0].as_py())
                geolocation_response = geolocation_response.replace("Answer:","").replace(" ","").replace("°","").replace("'","").replace(" ","").replace("N","").replace("E","")
                image_dir_path = './data/output/weather/'
                make_dir(image_dir_path)
                images_file_path = f"{image_dir_path}{self.now_date}.jpg"
                downloader = WindyImageDownloader()
                url = f"https://www.Windy.com/zh/-气象雷达-radar?radar,{geolocation_response},5\n"
                print('--------: ',url)
                downloader.execute(url=url,output_path=images_file_path)
                send_output("windy_crawler_response", pa.array([create_agent_output(step_name='windy_crawler_response',
                                                                                  output_data=images_file_path,
                                                                                  dataflow_status=os.getenv(
                                                                                      'IS_DATAFLOW_END', False))]),
                            dora_event['metadata'])
                print('windy_crawler_response:', images_file_path)
        return DoraStatus.CONTINUE

# if __name__ == "__main__":
#     downloader = WindyImageDownloader()
#     # 假设这里的URL是你要截图的Windy.com的页面
#     url = "https://www.Windy.com/zh/-气象雷达-radar?radar,39.9042,116.4074,5\n"
#     base64_image = downloader.execute(url)
