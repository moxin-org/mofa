import io
import json

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
from PIL import Image

from mofa.utils.envs.util import init_proxy_env

# 设置 OpenAI API 密钥
api_key = "sk-proj-"
client = OpenAI(api_key=api_key)
chromedriver_autoinstaller.install()
def encode_image(image_path:str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def generate_prompt(image_type: str) -> str:
    """Generate an appropriate prompt based on the image type."""
    if "radar" in image_type:
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Precipitation Pattern Identification**\n"
            "**C - Context:**\n"
            "This is a radar weather map covering a large area from East Asia to Central Asia, showing the distribution of precipitation. Radar maps are primarily used to detect the location and intensity of precipitation. Different colors represent varying precipitation intensities, such as light blue for light rain, and darker blues or greens for moderate to heavy rain.\n"
            "**O - Objective:**\n"
            "Identify and describe areas with different rainfall intensities, pinpoint the region with the heaviest precipitation, and analyze the spatial distribution of rainfall. Explain the possible causes and impacts of the rainfall in these areas.\n"
            "**S - Style:**\n"
            "The analysis should be written in a professional meteorological style, providing clear scientific explanations that are accurate yet easily understandable.\n"
            "**T - Tone:**\n"
            "Formal and objective, emphasizing conclusions drawn from scientific data.\n"
            "**A - Audience:**\n"
            "Meteorologists, emergency management officials, and professionals with an interest in rainfall and weather.\n"
            "**R - Response:**\n"
            "Provide a professional analysis report containing the following sections:\n"
            "1. Spatial distribution of rainfall intensity: Describe the rainfall situation represented by different colored regions.\n"
            "2. Focused rainfall analysis: Identify the region with the heaviest rainfall, discuss its potential impacts.\n"
            "3. Causes and trend prediction: Analyze the meteorological factors behind the current precipitation pattern and predict future trends."
        )
    elif "satellite" in image_type:
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Cloud Movement Prediction**\n"
            "**C - Context:**\n"
            "This is a satellite cloud image covering a wide region, from the Pacific coastline to East Asia, showing the distribution of clouds in the atmosphere. Satellite images are used to analyze cloud density, types, and coverage to understand the current weather conditions and predict future changes.\n"
            "**O - Objective:**\n"
            "Analyze the movement direction and speed of the clouds, describe their density, and predict potential weather changes based on the cloud patterns in the next few hours.\n"
            "**S - Style:**\n"
            "The analysis should be thorough and scientific, with detailed explanations of cloud characteristics and their potential impact on weather patterns.\n"
            "**T - Tone:**\n"
            "Formal and authoritative, focusing on scientific analysis and factual basis.\n"
            "**A - Audience:**\n"
            "Meteorologists, government decision-makers, and the public interested in weather forecasting.\n"
            "**R - Response:**\n"
            "Provide a cloud behavior analysis report including the following:\n"
            "1. Cloud distribution and density: Describe cloud thickness and types in different areas.\n"
            "2. Cloud movement: Predict the direction and speed of cloud movement and its potential impact.\n"
            "3. Weather implications: Explain how cloud movements might influence future weather, including rain, wind, and other changes."
        )
    elif "wind" in image_type:
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Wind Analysis**\n"
            "**C - Context:**\n"
            "This is a wind map showing wind speed and direction across a region, from East Asia to Central Asia. The map uses colors and arrows to represent wind speed and direction, with color intensity indicating wind strength, and arrows showing the direction of wind flow.\n"
            "**O - Objective:**\n"
            "Analyze the distribution of wind speed and direction in the region, identify areas with high wind speeds, and understand the overall wind flow. Explain the spatial features of wind and predict the potential weather changes these winds may bring.\n"
            "**S - Style:**\n"
            "The analysis should be scientific and detailed, with a focus on explaining the wind distribution and forecasting its effects on the weather.\n"
            "**T - Tone:**\n"
            "Formal and neutral, based on scientific data and analysis.\n"
            "**A - Audience:**\n"
            "Meteorologists, aviation and maritime professionals, and government emergency departments.\n"
            "**R - Response:**\n"
            "Provide a detailed wind analysis report with the following sections:\n"
            "1. Wind speed and direction distribution: Describe the wind speed and direction in different regions.\n"
            "2. Impact of wind on weather: Explain how wind might affect temperature, humidity, rainfall, and other weather phenomena.\n"
            "3. Future wind trend prediction: Predict the future changes in wind and their possible impacts on weather conditions."
        )
    elif "temperature" in image_type:
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Temperature Trend Analysis**\n"
            "**C - Context:**\n"
            "This is a temperature distribution map showing the temperatures across cities from East Asia to Central Asia. Different colors represent temperature ranges, from blue for low temperatures to red for high temperatures, providing a clear view of spatial temperature distribution.\n"
            "**O - Objective:**\n"
            "Analyze the temperature distribution in the region, identify areas with high and low temperatures, and explain the relationship between temperature patterns and geographical, seasonal, and meteorological factors. Predict temperature changes in the coming hours.\n"
            "**S - Style:**\n"
            "Write in a scientific and systematic style, describing the temperature patterns and explaining their causes.\n"
            "**T - Tone:**\n"
            "Formal and objective, focusing on data-supported scientific explanations.\n"
            "**A - Audience:**\n"
            "Meteorological researchers, urban planners, and government decision-makers.\n"
            "**R - Response:**\n"
            "Provide a temperature analysis report including the following sections:\n"
            "1. Temperature distribution description: Describe the regions with high and low temperatures.\n"
            "2. Temperature difference causes: Explain factors contributing to temperature differences, such as ocean effects or terrain influences.\n"
            "3. Temperature trend prediction: Predict temperature changes based on current conditions."
        )
    elif "rain" in image_type:
        return (
            "**Task: Weather Analysis**\n"
            "**Task: Precipitation Pattern Identification**\n"
            "**Task: Extreme Weather Risk Assessment**\n"
            "**C - Context:**\n"
            "This is a rainfall distribution map showing accumulated rainfall over a large area, from East Asia to Central Asia, for a specific time period. Different colors represent varying rainfall intensities, from blue for light rain to yellow for heavy rain.\n"
            "**O - Objective:**\n"
            "Identify areas with heavy rainfall and assess the potential risk of flooding or extreme weather in those regions. Analyze the causes of the current precipitation pattern and suggest possible mitigation measures.\n"
            "**S - Style:**\n"
            "The analysis should be scientific and detailed, emphasizing data analysis and risk assessment.\n"
            "**T - Tone:**\n"
            "Formal and serious, highlighting the scientific evaluation of weather risks.\n"
            "**A - Audience:**\n"
            "Government emergency management officials, environmental researchers, and local government authorities.\n"
            "**R - Response:**\n"
            "Provide an analysis report on rainfall distribution including the following:\n"
            "1. Rainfall distribution description: Detail the location and extent of high rainfall areas.\n"
            "2. Flood and extreme weather risk assessment: Evaluate the potential risk of flooding or other disasters caused by current rainfall.\n"
            "3. Recommendations: Suggest possible emergency measures or disaster prevention strategies based on the rainfall patterns."
        )
    else:
        return "Unknown image type. Please provide a valid image type."

def future_weather_analysis(image_analysis:list[str],lng_lat:str=None):
    prompt = f"""
        Task: Future Weather Prediction Based on Multi-Source Analysis

        C - Context: You have conducted detailed analyses of the following five types of weather images and generated corresponding analysis reports:

        Radar Weather Map: Analyzed the spatial distribution of precipitation intensity, identified regions with the strongest rainfall and their coverage, and explored the causes and impacts of precipitation.
        Satellite Cloud Map: Predicted cloud movement direction and speed, described cloud density, and assessed their potential impact on regional weather.
        Wind Weather Map: Analyzed wind speed and direction distribution, identified areas with high wind speeds, and predicted the potential weather changes due to wind strength.
        Temperature Distribution Map: Described temperature conditions across various cities and regions, analyzed temperature differences related to geography, seasons, and meteorological conditions, and predicted temperature changes over the next few hours.
        Precipitation Distribution Map: Evaluated areas with high precipitation intensity, analyzed potential flood or extreme weather risks in these areas, and proposed mitigation measures.
        O - Objective: Based on the analyses of these five weather images, provide a comprehensive weather forecast for the next 24 hours for the East Asia to Central Asia region. The forecast should include:

        Precipitation Prediction: Identify areas expected to experience rain or heavy rainfall, the intensity of precipitation, and the duration of rainfall.
        Cloud Layer Changes: Describe cloud type changes, density variations, and their impact on weather, such as cooling, precipitation probability, or visibility.
        Wind Force Changes: Predict changes in wind speed and direction, especially in areas with high wind speeds, and their potential effects like storms or high winds.
        Temperature Trends: Forecast temperature changes, including areas of warming or cooling.
        Extreme Weather Risk Assessment: Identify potential extreme weather events such as floods, thunderstorms, heatwaves, or cold spells, and assess their risks and impacts.
        S - Style: Adopt the style of a professional meteorological analyst. The content should be scientific, detailed, and well-structured. Provide clear data support and logical explanations to ensure high credibility and practicality of the forecast.

        T - Tone: Formal and objective, emphasizing data-driven scientific conclusions while avoiding subjective judgments or emotional language.

        A - Audience:

        Government Emergency Management Departments: For formulating and adjusting emergency response plans.
        Meteorological Researchers and Academics: For further research and analysis.
        Aviation and Marine Transport Professionals: For planning and adjusting routes to ensure safety.
        General Public: Especially residents in the affected areas, to help them prepare for weather changes.
        R - Response: Generate a comprehensive future weather prediction report that includes the following sections:

        Overall Weather Overview:
        Summarize the main weather trends over the next 24 hours, including precipitation, cloud layers, wind forces, and temperature fluctuations.
        Precipitation Prediction:
        Regional Breakdown: Detailed description of specific areas expected to receive precipitation.
        Precipitation Intensity: Classification of precipitation levels (light rain, moderate rain, heavy rain, torrential rain).
        Duration: Expected duration of precipitation in each region.
        Precipitation Causes: Analysis of the main meteorological factors leading to precipitation.
        Cloud Layer Changes:
        Cloud Types and Densities: Description of cloud types (e.g., cumulonimbus, stratus) and their densities in different regions.
        Cloud Movement Trends: Predicted movement direction and speed of cloud layers.
        Weather Impact: How changes in cloud layers will affect cooling, precipitation probability, and visibility.
        Wind Force Changes:
        Wind Speed and Direction: Changes in wind speeds (light breeze, moderate breeze, strong breeze, gale) and direction across regions.
        High Wind Areas: Identification of areas with high wind speeds and their potential impacts.
        Wind Force Causes: Analysis of the main causes for changes in wind force, such as shifting pressure systems.
        Temperature Trends:
        Current Temperature Distribution: Description of current temperatures across major cities and regions.
        Future Temperature Changes: Predicted temperature increases or decreases over the next 24 hours.
        Temperature Difference Causes: Explanation of temperature changes related to geographic and meteorological factors.
        Extreme Weather Risk Assessment:
        Flood Risks: Based on precipitation and topography, assess the likelihood of floods and their risk levels.
        Thunderstorms and Storms: Identification of potential thunderstorms or storms and their expected impacts.
        Heatwaves or Cold Spells: Evaluation of the possibility of extreme temperature events and their consequences.
        Mitigation Recommendations: Specific emergency measures or precautions based on the identified risks.

        image_analysis: {json.dumps(image_analysis, ensure_ascii=False)}
    
        
    
"""
    if lng_lat is not None:
        prompt += f"And I am particularly concerned about this latitude and longitude information. {lng_lat}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ]
            }
        ], )
    return response.choices[0].message.content

class WindyImageDownloader():
    """从Windy.com自动下载气象图的脚本
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 自动下载和安装匹配的ChromeDriver
        chromedriver_autoinstaller.install()

    def execute(self, url: str, output_path: Optional[str] = "windy_image.png"):
        # 创建一个新的浏览器实例

        # options = webdriver.ChromeOptions()
        options = webdriver.SafariOptions()
        options.headless = True
        # options.add_argument('--headless')  # 无头模式
        # options.add_argument('--disable-gpu')  # 禁用GPU
        # options.add_argument('--start-maximized')  # 设置窗口大小
        # options.add_argument('--disable-gpu')  # 禁用GPU加速（可选）
        # options.add_argument('--enable-webgl')  # 启用WebGL
        # options.add_argument('--ignore-gpu-blacklist')  # 忽略GPU黑名单
        # options.add_argument('--use-gl=desktop')  # 使用桌面OpenGL
        # options.add_argument('--no-sandbox')  # 在某些环境下需要
        # options.add_argument('--disable-software-rasterizer')  # 禁用软件光栅化器
        # 创建一个Service实例（不需要指定路径，chromedriver_autoinstaller已处理）
        service = Service()

        # driver = webdriver.Chrome(service=service, options=options)
        driver = webdriver.Safari(options=options,)

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

            # 给一点额外的时间让地图完全加载
            time.sleep(15)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "leaflet-pane")))
            wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
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
        model="gpt-4o-mini",
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
        ],    )
    print(response.choices[0].message.content)
    print('运行完毕')

    return response.choices[0].message.content

    # 提取并返回描述
def resize_image(input_path, output_path, size=(512, 512)):
    with Image.open(input_path) as img:
        # 使用 ANTIALIAS（高质量缩放滤镜）
        img_resized = img.resize(size, Image.Resampling.LANCZOS)
        img_resized.save(output_path)
        print(f"Image saved to {output_path} with size {size}")
@ray.remote
def run_download(url: str, output_path: str):
    downloader = WindyImageDownloader()
    downloader.execute(url=url, output_path=output_path)
    resize_image(input_path=output_path, output_path=output_path)
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
        image_path = image_info.get('output_path')
        image_str = encode_image(image_path)
        prompt_str = generate_prompt(image_path)
        results.append(interpret_image_with_chatgpt(image_str,prompt_str))
    return results



# init_proxy_env(proxy_url='127.0.0.1:8950')
# 执行流程
downloader = WindyImageDownloader()
downloader.execute(url="https://www.windy.com/zh/-%E5%8D%AB%E6%98%9F%E4%BA%91%E5%9B%BE-satellite?satellite,36.069,113.263,3", output_path="satellite_map_39.9042_116.4074.png")

latitude, longitude = "39.9042", "116.4074"  # 示例坐标（北京）
images_infos = parallel_image_capture(latitude, longitude)
# images_infos = [{'url': 'https://www.windy.com/zh/-%E6%B0%94%E8%B1%A1%E9%9B%B7%E8%BE%BE-radar?radar,39.9042,116.4074,5',
#   'output_path': 'radar_map_39.9042_116.4074.png',
#   'image_type': 'radar'},
#  {'url': 'https://www.windy.com/zh/-%E5%8D%AB%E6%98%9F%E4%BA%91%E5%9B%BE-satellite?satellite,39.9042,116.4074,5',
#   'output_path': 'satellite_map_39.9042_116.4074.png',
#   'image_type': 'satellite'},
#  {'url': 'https://www.windy.com/?39.9042,116.4074,5',
#   'output_path': 'wind_weather_39.9042_116.4074.png',
#   'image_type': 'wind'},
#  {'url': 'https://www.windy.com/zh/-%E6%B8%A9%E5%BA%A6-temp?temp,39.9042,116.4074,6',
#   'output_path': 'temp_map_39.9042_116.4074.png',
#   'image_type': 'temp'},
#  {'url': 'https://www.windy.com/zh/-%E9%99%8D%E9%9B%A8%E9%87%8F-rainAccu?rainAccu,39.9042,116.4074,5',
#   'output_path': 'rain_map_39.9042_116.4074.png',
#   'image_type': 'rain'}]
images_analyze = interpret_images(images_infos)
# images_analyze = ['### 专业气象分析报告\n\n#### 1. 降雨强度的空间分布\n\n根据雷达天气图，不同颜色区域代表着降水强度的变化。具体分布如下：\n\n- **浅蓝色区域**：表示小雨的区域，降水量少，主要分布在东亚部分地区，影响日常生活通常较小。\n- **蓝色和绿色区域**：代表中到大雨的区域，普遍覆盖中国东部及日本部分地区，降水量增加，可能导致局部水涝。\n- **深蓝色和紫色区域**：指示大雨以及潜在的暴雨区，这些区域主要集中在日本东南部与中国南方，降水强度可达普降性降雨，带来显著影响。\n\n#### 2. 重点降雨区域分析\n\n本次降雨中最强降雨的位置集中在日本东南沿海及中国南方。特别是：\n\n- **日本东南沿海**：该地区出现深蓝色及紫色区域，降水强度最高，覆盖范围约100公里，降水量可能达到50毫米以上，极有可能对交通和农业产生不利影响。\n- **中国南方**：这里同样显示出中到大雨的迹象，强降雨可能影响城市基础设施，导致内涝事件。\n\n#### 3. 降雨成因及趋势预测\n\n当前降水格局的形成可能与以下气象因素相关：\n\n- **气旋活动**：东海和日本海一带的气旋活动增强，促使湿润气流向东北方向移动，导致降水的增强。\n- **地形影响**：该区域的地形尤其是沿海地区的山地，对气流有明显影响，助长了降水量。\n\n**未来趋势预测**：\n- 预计未来几天内，气旋活动仍将持续，造成间歇性的强降雨。特别是沿海地区，需高度警惕潜在的暴雨风险。\n- 再者，考虑到季节变化，未来降雨量可能会有所增加，尤其是在进入秋季时，适度监测与预警措施需要增强，以应对可能引发的洪涝灾害。\n\n本报告旨在为气象学专家及政府应急管理人员提供科学依据，以便制定相应的应对措施，对公众安全给予更有效的保障。',
#  '### 云层分析报告\n\n#### 1. 云层分布和密度\n当前卫星云图显示，从太平洋沿岸到东亚大陆的广泛区域内，云层的分布情况相对复杂。图中可以观察到以下特点：\n\n- **东南部海域（近日本和韩国）：** 此区域云层较为密集，主要为低层云和中层云，厚度较大，可能会影响到降雨的强度和持续时间。\n- **中心区域（中国沿海）：** 云层分布较为稀疏，主要呈现出少量高层云，预计对当地天气影响较小。\n- **西北部（中国西北）：** 此区域云层稀薄，基本无云，气候相对干燥，未来的天气情况可能以晴朗为主。\n\n#### 2. 云层运动方向和速度\n根据当前的云层运动趋势，预测云层的移动方向及速度如下：\n\n- **运动方向：** 整体云层正在向东北方向移动，尤其是在东南海域，由台风或低气压系统引导。\n- **速度：** 预计云层的移动速度为每小时20到30公里。在未来几个小时内，云层将进一步向北移动，沿着日本和朝鲜半岛的东侧推进。\n\n#### 3. 对天气的影响\n根据当前云层的分布和移动趋势，预期对天气的影响包括：\n\n- **降雨：** 东南海域及邻近地区可能出现间歇性降雨，由于云层较厚，降水量可能较大。预期会导致局部地区发生强降雨现象，特别是在台风影响区域。\n- **风力：** 随着云层的移动，预计上述海域的风速将增强，可能出现强风天气，需注意沿海地区的防风措施。\n- **其他天气现象：** 在中心区域云层稀薄的地方，预计未来几小时内将以晴天为主，增加气温升高的可能性。\n\n### 总结\n综合以上分析，当前云层的分布和运动将对未来天气产生显著影响。特别是在东南部海域，加上云层的厚度和移动速度，降雨及强风现象将更为明显。各相关决策部门需密切关注天气变化，并提前做好应对准备。',
#  '### 风力分析报告\n\n#### 1. 风速和风向的空间分布\n根据风力天气图，东亚至中亚区域的风速和风向分布情况表现出显著的差异。图中使用渐变色彩来表示风速强度，从淡蓝色（低风速）到深蓝色（高风速）。红色斑块显示出风速较高的区域，特别是在东海和西北太平洋，风速可达到中等至强风水平。\n\n箭头的方向清晰地指示了风的流动趋势。总体来看，主要的风流动方向为东南至西北，这意味着来自海洋的湿润气流正在向内陆发展。此外，在某些区域（例如靠近台风的区域），风速相对强劲，表明气压低的条件造成了较强的风场。\n\n#### 2. 风力对天气的影响\n风速的提升直接影响了气温、湿度和降水。较强的风速有助于：\n\n- **温度调节**：强风能加速热量的传播，造成局部地区的温度下降。\n- **湿度变化**：来自海洋的风将携带较高的水分，可能导致湿度增加，而内陆地区在强风影响下则可能出现干燥。\n- **降水模式**：风速的增加伴随湿润气流的引导，可能导致降水的增强，尤其是在迎风坡和山地地区，形成局部强降雨的可能性高。\n\n对周边地区的影响尤为显著，特别是海洋运输和航空运输领域，较强的风速可能导致航行和飞行的不稳定性。\n\n#### 3. 未来风力趋势预测\n未来几天的风力趋势预测显示，预计东南部的风速可能会有所增强，特别是在接近台风的区域。随着台风的移动，风向可能会随之改变，导致风速的局部增强。\n\n同时，彼时气压的变化可能影响到周围地区的天气条件，预计一旦气压降低，降水和强风现象将更加突出。根据历史气象数据，建议密切关注沿海航运和航空优秀计划，及时发布相关气象预警，以应对突发的极端天气情况。\n\n### 总结\n整体来看，本次风力天气图显示出东亚至中亚区域的风速与风向具有复杂的空间分布特征。风力预计将在未来几天内持续影响该地区的天气，尤其是在相关的海洋和航空领域。各相关部门需采取必要措施，以保证安全与应对可能的气象风险。',
#  '这是一幅天气地图，展示了中国东部地区的温度和气流分布。这种类型的图像通常用于气象分析和天气预测。',
#  '### 降雨量分布分析报告\n\n#### 1. 降雨分布描述\n近期的降雨量分布图显示，从东亚到中亚的广泛区域中，有几个明显的高降雨区域。以颜色表示的降雨强度变化中，蓝色到黄色的范围表明：\n\n- **东亚地区**（如中国南部、韩国、日本沿海）：该区域的累积降雨量明显增加，尤其是在沿海地区，出现了暴雨的迹象。\n- **中亚部分地区**：部分山区和河流流域显示出较高的降雨量，这表明可能会对当地的水资源管理造成压力。\n\n#### 2. 洪水或极端天气风险评估\n基于目前的降雨模式，以下区域面临洪水或极端天气的风险：\n\n- **东海岸地区**：尤其是受影响的沿海城市，暴雨累积后可能导致城市内涝及土壤饱和，增加了山体滑坡的风险。\n- **南部山区**：由于降雨集中，河流可能迅速上涨，造成洪水，特别是在地形陡峭的地区。\n\n总体评估表明，随着降雨的继续，相关区域的洪水风险显著增加，尤其是在近期的天气系统影响下，需高度关注。\n\n#### 3. 应对建议\n根据目前的降雨情况，建议采取以下应急措施：\n\n- **实时监测与预警**：加强气象监测，及时发布降雨和洪水预警，确保公众能够提前获取信息。\n- **加强基础设施建设**：对易受洪水影响的区域，要加强排水系统的建设，提高防洪能力。\n- **应急响应计划**：制定和完善地方应急响应计划，确保能迅速动员资源应对可能的洪水灾害。\n- **公众教育和参与**：通过媒体和社区活动，增强公众的防灾意识和应对能力，确保社区在面临极端天气时能够有效响应。\n\n通过对降水数据的分析与风险评估，希望本报告能为相关部门和人员提供决策支持，以有效应对当前的降雨挑战。']
print(images_analyze)
feature_weather = future_weather_analysis(images_analyze,latitude + ','+longitude)
print(feature_weather)

