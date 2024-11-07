import io
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import ray
import base64
from typing import Optional
from openai import OpenAI
# 设置 OpenAI API 密钥
api_key = ""
client = OpenAI(api_key=api_key)
chromedriver_autoinstaller.install()
def encode_image(image_path:str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def generate_prompt(image_type: str) -> str:
    """根据图像类型生成适合的 prompt"""
    if "radar" in image_type:
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Precipitation Pattern Identification**\n"
            "**C - 上下文 (Context)：**\n"
            "这是一张雷达天气图，覆盖了广阔的区域，显示了从东亚到中亚的降水分布。雷达图主要用于探测降水的位置和强度，可以清晰看到不同区域的降雨状况。不同颜色代表降雨强度的变化，例如浅蓝色表示小雨，而深蓝色或绿色则表示中到大雨。\n"
            "**O - 目标 (Objective)：**\n"
            "识别并详细描述图中不同降雨强度的区域，找出最强降雨的位置及其覆盖的范围。分析降雨的空间分布模式，并解释这些区域降雨的可能原因和影响。\n"
            "**S - 风格 (Style)：**\n"
            "以专业气象分析师的风格进行阐述，提供科学的解释，内容需易于理解并兼具数据准确性。\n"
            "**T - 语气 (Tone)：**\n"
            "正式且客观，强调数据支持下的科学结论。\n"
            "**A - 受众 (Audience)：**\n"
            "气象学专家、政府应急管理人员，以及对降雨和天气有较高兴趣度的专业人员。\n"
            "**R - 响应 (Response)：**\n"
            "提供一个专业分析报告，包含以下部分：\n"
            "1. 降雨强度的空间分布：描述不同颜色区域代表的降雨情况。\n"
            "2. 重点降雨区域分析：指出最强降雨的位置和覆盖范围，讨论其潜在影响。\n"
            "3. 降雨成因及趋势预测：对造成当前降水格局的可能气象因素进行分析，并预测未来的变化趋势。"
        )
    elif "satellite" in image_type :
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Cloud Movement Prediction**\n"
            "**C - 上下文 (Context)：**\n"
            "这是一张卫星云图，覆盖了广泛的区域，从太平洋沿岸到东亚大陆，显示了大气中云层的分布。卫星图主要用于分析云层的密度、类型和覆盖范围，以便理解当前的天气状况及未来的变化。\n"
            "**O - 目标 (Objective)：**\n"
            "分析云层的移动方向和速度，描述云层的密度以及可能对区域天气造成的影响。提供未来几小时内云层的运动趋势和可能带来的天气变化。\n"
            "**S - 风格 (Style)：**\n"
            "采用科学、详尽的风格进行分析，详细解释云层的特性及其可能影响，突出云层与天气之间的联系。\n"
            "**T - 语气 (Tone)：**\n"
            "正式、权威，注重科学分析和事实依据。\n"
            "**A - 受众 (Audience)：**\n"
            "气象学家、政府部门决策人员，以及需要理解天气预测的公众。\n"
            "**R - 响应 (Response)：**\n"
            "提供云层行为的分析报告，包含以下内容：\n"
            "1. 云层分布和密度：描述不同区域的云层厚度和类型。\n"
            "2. 云层运动方向和速度：预测云层移动的方向及其潜在影响。\n"
            "3. 对天气的影响：解释云层移动对未来天气的可能作用，包括降雨、风力等变化。"
        )
    elif "wind" in image_type :
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Wind Analysis**\n"
            "**C - 上下文 (Context)：**\n"
            "这是一张显示某一地区风速和风向的风力天气图，覆盖了东亚至中亚的区域。图中不同颜色和箭头代表了风速的强度和风向，颜色从淡至浓表示风速从低到高，箭头指示风的流动方向。\n"
            "**O - 目标 (Objective)：**\n"
            "分析当前区域内风速和风向的分布情况，找出风速较大的区域以及风向的总体流动趋势。解释风力的空间特征，并预测这些风力可能带来的天气变化。\n"
            "**S - 风格 (Style)：**\n"
            "科学且详尽，风格注重对风力分布的解释和对天气影响的预测。\n"
            "**T - 语气 (Tone)：**\n"
            "正式且中立，基于科学的数据和分析。\n"
            "**A - 受众 (Audience)：**\n"
            "专业气象人员、航空和海洋运输从业者，以及政府应急部门。\n"
            "**R - 响应 (Response)：**\n"
            "提供风力的详细分析报告，包含以下部分：\n"
            "1. 风速和风向的空间分布：描述风力图中的颜色和箭头，指出高风速区域。\n"
            "2. 风力对天气的影响：解释风力对温度、湿度、降雨等可能的影响。\n"
            "3. 未来风力趋势预测：预测未来风力的变化趋势及其潜在影响。"
        )
    elif "temperature" in image_type :
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Temperature Trend Analysis**\n"
            "**C - 上下文 (Context)：**\n"
            "这是一张温度分布图，显示了从东亚到中亚不同城市的温度情况。图中用不同颜色表示各地的温度范围，从蓝色的低温到红色的高温，直观地展现了温度的空间分布。\n"
            "**O - 目标 (Objective)：**\n"
            "分析该区域内的温度分布，找出高温和低温区域的差异，描述这些温度特征如何与地理、季节和气象条件有关。预测温度在未来几小时的可能变化。\n"
            "**S - 风格 (Style)：**\n"
            "以科学而系统化的风格撰写，详细描述温度格局并解释其成因。\n"
            "**T - 语气 (Tone)：**\n"
            "正式、客观，强调数据支撑和科学解释。\n"
            "**A - 受众 (Audience)：**\n"
            "气象研究者、城市规划者，以及政府部门决策者。\n"
            "**R - 响应 (Response)：**\n"
            "提供温度分析的报告，包含以下部分：\n"
            "1. 温度分布描述：描述高温和低温区域的分布及其范围。\n"
            "2. 温差原因分析：解释温度差异的成因，如海洋效应、地形影响等。\n"
            "3. 温度趋势预测：基于当前温度情况，预测未来几小时内的温度变化。"
        )
    elif "rain" in image_type :
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Precipitation Pattern Identification**\n"
            "**Task: Extreme Weather Risk Assessment**\n"
            "**C - 上下文 (Context)：**\n"
            "这是一张降雨量分布图，覆盖了广阔的区域，从东亚到中亚，展示了过去一段时间的累计降雨量。不同颜色表示不同的降雨强度，蓝色到黄色逐渐增加，代表由小雨到暴雨的变化。\n"
            "**O - 目标 (Objective)：**\n"
            "识别降雨强度较高的区域，并评估这些区域内是否存在潜在的洪水或极端天气风险。分析当前降雨格局的成因并提出可能的应对措施。\n"
            "**S - 风格 (Style)：**\n"
            "科学、详细，注重对数据的分析及对风险的评估。\n"
            "**T - 语气 (Tone)：**\n"
            "正式且严肃，突出对降水带来风险的科学评估。\n"
            "**A - 受众 (Audience)：**\n"
            "政府应急管理人员、环境研究学者，以及当地政府和相关部门。\n"
            "**R - 响应 (Response)：**\n"
            "提供降雨量分布的分析报告，包含以下部分：\n"
            "1. 降雨分布描述：详细描述高降雨区域的位置及范围。\n"
            "2. 洪水或极端天气风险评估：评估当前降雨量可能带来的洪水或其他灾害的风险。\n"
            "3. 应对建议：根据降雨情况提出可能的应急措施或防灾建议。"
        )
    else:
        return "图像类型未知，请提供有效的图像类型。"
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

def interpret_image_with_chatgpt(image_str: str, prompt: str) -> str:
    """使用 ChatGPT 解读图像描述"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_str}"
                        }
                    }
                ]
            }
        ],
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

    # 提取并返回描述

@ray.remote
def run_download(url: str, output_path: str):
    downloader = WindyImageDownloader()
    downloader.execute(url=url, output_path=output_path)
    return {'image_path':output_path,}
# 定义并行抓取函数，包含五个URL
def parallel_image_capture(latitude: str, longitude: str) -> list:
    radar_url = f"https://www.windy.com/zh/-%E6%B0%94%E8%B1%A1%E9%9B%B7%E8%BE%BE-radar?radar,{latitude},{longitude},5"
    satellite_url = f"https://www.windy.com/zh/-%E5%8D%AB%E6%98%9F%E4%BA%91%E5%9B%BE-satellite?satellite,{latitude},{longitude},5"
    wind_url = f"https://www.windy.com/?{latitude},{longitude},5"
    temp_url = f"https://www.windy.com/zh/-%E6%B8%A9%E5%BA%A6-temp?temp,{latitude},{longitude},6"
    rain_url = f"https://www.windy.com/zh/-%E9%99%8D%E9%9B%A8%E9%87%8F-rainAccu?rainAccu,{latitude},{longitude},5"
    
    radar_image_path = f"radar_map_{latitude}_{longitude}.png"
    satellite_image_path = f"satellite_map_{latitude}_{longitude}.png"
    wind_image_path = f"wind_weather_{latitude}_{longitude}.png"
    temp_image_path = f"temp_map_{latitude}_{longitude}.png"
    rain_image_path = f"rain_map_{latitude}_{longitude}.png"
    image_infos = [{'url':radar_url,'output_path':radar_image_path,'image_type':'radar'},{'url':satellite_url,'output_path':satellite_image_path,'image_type':'satellite'},
                    {'url':wind_url,'output_path':wind_image_path,'image_type':'wind'},{'url':temp_url,'output_path':temp_image_path,'image_type':'temp'},
                    {'url':rain_url,'output_path':rain_image_path,'image_type':'rain'}]
    futures = [run_download.remote(x.get('url'),x.get('output_path')) for x in image_infos]

    results = ray.get(futures)
    print("图片下载地址是: ", results)
    return image_infos

# 定义图像解读函数
def interpret_images(image_infos: list) -> list:
    results = []
    for image_info in image_infos:
        image_path = image_info.get('image_path')
        image_str = encode_image(image_path)
        prompt_str = generate_prompt(image_path)
        results.append(interpret_image_with_chatgpt(image_str,prompt_str))
    return results




# 执行流程
latitude, longitude = "39.9042", "116.4074"  # 示例坐标（北京）
# images_infos = parallel_image_capture(latitude, longitude)
images_infos = [{'image_path': 'radar_map_39.9042_116.4074.png'}, {'image_path': 'satellite_map_39.9042_116.4074.png'}, {'image_path': 'wind_weather_39.9042_116.4074.png'}, {'image_path': 'temp_map_39.9042_116.4074.png'}, {'image_path': 'rain_map_39.9042_116.4074.png'}]
images_analyze = interpret_images(images_infos)
print(images_analyze)

# interpretation_texts = interpret_images(image_paths, prompts)
#
# # 输出解读结果
# for i, text in enumerate(interpretation_texts):
#     print(f"图像{i+1}解读内容：\n{text}")




