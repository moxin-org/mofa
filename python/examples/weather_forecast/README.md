
# **项目名: 天气爬虫预测系统**

## **团队名称:**



**组员：**

- 肖申克的舅妈 (GitCode用户名: Julywwwww)




## **项目地址:**

https://gitcode.com/Julywwwww/mofa_local/

## **环境依赖:**
1. **浏览器**
2. **Selenium**
3. **其他必要的Python库**（如 requests, BeautifulSoup 等）

### **安装步骤:**

cd weather_forecast 
pip3 install -r requirements.txt

### **运行程序:**

1. **运行智能体框架：**

   ```bash
   dora up && dora build weather_predict_dataflow.yml && dora start weather_predict_dataflow.yml
   ```

2. **启动任务输入端：**

   - 打开另一个终端窗口，运行 `terminal-input`。
   - 在 `terminal-input` 中输入任务指令即可与智能体交互。

------

## **软件介绍**

**天气预测系统** 是一款智能化应用，旨在通过用户输入的问题，自动获取用户的地理位置，经纬度信息，并基于此进行天气数据的爬取并且保存气象图片,然后提取最近的5张图片进行交给llm进行重点气象信息提取以及气象预测。系统采用多节点架构，实现了数据的动态处理和高效预测，提升了用户体验和预测准确性。

### **突破点和创新点:**

- 更智能的天气预测： 利用大型语言模型（LLM）结合最近五张气象图，实现更准确和上下文相关的天气预测。

- 高效数据爬取： 自动化Selenium爬虫，实时获取Windy.com最新气象图，确保数据的时效性和准确性。

- 多节点协同工作： 设计多节点数据流，实现地理定位、数据爬取和预测分析的高效协同，提升系统整体性能和响应速度。

- 重点天气信息提取： 使用LLM分析五张气象图，自动识别并突出显示对用户影响较大的天气变化，提供更具实用价值的预报信息。


------

## **技术开发介绍**

### **使用的框架与工具:**

- **Dora-RS 框架:** 负责智能体间的分布式计算，确保各节点在任务执行中的顺畅协作。
- **MoFa 框架 (墨心智能体组合框架):** 为智能体之间的交互和编排提供了强大的基础设施。
- **Selenium:** 用于自动化网页操作，爬取 Windy.com 的气象图。
- **Python:** 主要编程语言，编写各智能体的脚本。

### **技术难点:**

1. **智能体协作:**
   - **难点:** 实现多个智能体之间的数据流动和实时交互，确保各节点高效协同工作。
   - **解决方案:** 使用 Dora-RS 框架实现动态智能体调度，确保数据在各节点之间无缝传递，提升整体系统性能。

2. **动态数据爬取与处理:**
   - **难点:** 如何快速的获取气象图等数据，并且跳过反爬措施。
   - **解决方案:** 使用 Selenium 自动化爬取动态气象图，跳过反爬并且处理和存储不同的气象图信息。

3. **天气预测算法:**
   - **难点:** 基于图像数据进行准确的天气预测和重点信息提取。
   - **解决方案:** 采用先进的图像处理和机器学习算法，结合历史数据进行模型训练，提高预测准确性。

------



## **使用案例**

### **案例 1: 用户查询当前天气**

**用户输入:** "陕西。"

**系统响应:**

geolocation_response: Answer: 35.1917°N, 108.8701°E 
windy_crawler_response: ./data/output/weather/20241015_231531.jpg 
weather_response: ### Weather Analysis and Forecast

#### Key Meteorological Features:
1. **Temperature Gradient**: The image shows a temperature range from the low teens in northern areas to around 30°C in parts of India, indicating a significant thermal contrast across the region.
2. **Wind Patterns**: Noticeable wind flows can be observed, particularly around the low-pressure center located in the northeastern Pacific. The curved isobars suggest the presence of a system potentially influencing nearby weather.
3. **Moisture Bands**: There are signs of moisture currents moving inland, mainly from the southeast, suggesting cloud formation and potential precipitation in southern parts of Asia.

#### Hourly Predictions:
1. **Temperature Changes**:
   - Expect slight temperature increases in southern regions (India and Southeast Asia) due to daytime heating, with highs potentially reaching 31-32°C.
   - Northern areas may see minor cooling, especially where cloud cover increases.

2. **Precipitation Likelihood and Intensity**:
   - Light to moderate rains may develop along the southeastern coast of India and in parts of Bangladesh, as moisture converges with local weather dynamics.
   - Overall precipitation is likely to be sporadic, with isolated thunderstorms possible but limited in coverage.

3. **Wind Speed and Direction Shifts**:
   - Wind speeds are expected to remain generally moderate (10-15 km/h). A possible increase in wind strength, particularly near the coastline and higher terrain, is anticipated in gustier areas.
   - Winds from the southeast will be predominant, shifting slightly to the east as the day progresses.

4. **Cloud Cover Developments**:
   - Significant cloud cover is forecast to develop over the central regions of India, with increasing opacity in the areas expected to experience precipitation. 
   - Over the northwest, clearer conditions may persist.

#### Meteorological Anomalies:
- A potential **localized low-pressure area** may form in northeastern India, enhancing wind speeds and leading to unpredictable weather patterns in that locale.
- Interaction between the moist winds and the higher terrain could lead to localized heavy rainfall or sudden thunderstorm activity.

#### Geographic Areas of Concern:
1. **Eastern India and Bangladesh** - These regions may experience enhanced rainfall and potential flooding in low-lying areas.
2. **Northeast India** - A watch for thunderstorms and localized heavy rain, given the converging atmospheric conditions.

#### Short-Term Risks:
- **Aviation**: Potential for turbulence and delays in northeastern and eastern India due to weather fluctuations and thunderstorms.
- **Marine Activities**: Increased caution advised near the coasts where wind patterns may shift suddenly, possibly escalating sea conditions.
- **Outdoor Events**: Light rain and potential thunderstorms could disrupt outdoor plans, especially in southeastern India.

#### Meteorological Processes and Uncertainties: 
- The forecasted changes are driven primarily by thermodynamic processes related to daytime heating in the southern regions and moisture influx from the southeast. 
- Uncertainties include variations in precipitation intensity and the exact path of any emerging low-pressure systems, which could significantly alter local weather conditions.

In summary, expect mostly warm and moderately breezy conditions with localized precipitation in southeastern regions, while keeping an eye on developing storm systems that could pose risks in specific areas highlighted. :dataflow_status


### **案例 2: 用户查询未来天气趋势**

**用户输入:** "北京？"

**系统响应:**

### Weather Analysis and Prediction

#### 1. Key Meteorological Features
The provided weather image displays several key features:

- **Pressure Centers**: There are indications of a low-pressure system, particularly to the east of the image over the ocean, which is likely generating enhanced winds and precipitation in its vicinity.
- **Wind Patterns**: The image shows strong, organized wind patterns emanating from the low-pressure zone, with directional flow indicating potential coastal impacts.
- **Temperature Gradients**: Significant temperature variations are evident, reflected by color changes which suggest contrasting air masses. This can be a precursor to instability.
- **Cloud Cover**: There’s an indication of cloud formations, particularly along the eastern coastal regions, hinting at possible precipitation zones.

#### 2. Weather Predictions for the Next Hour
   **a) Temperature Changes**: 
   Minimal temperature fluctuations are expected, with localized areas experiencing slight cooling due to increased cloud cover and potential precipitation, particularly near coastal regions.

   **b) Precipitation Likelihood and Intensity**: 
   There’s a moderate likelihood of precipitation, especially in areas east of the central low. Rainfall intensity could vary, with localized heavy showers possible along the coastal zones due to convergence driven by wind flow.

   **c) Wind Speed and Direction Shifts**: 
   Wind speeds are projected to increase from the current speeds (around 10-13 knots) to 15-20 knots as the low-pressure system influences wind patterns. The direction will remain largely consistent but may shift slightly towards a more north-easterly flow in affected regions.

   **d) Cloud Cover Developments**: 
   Expect an increase in cloud cover, notably over eastern regions, as moisture converges and lifts, leading to denser cloud formations and reduced visibility.

#### 3. Meteorological Anomalies
An unusual meteorological pattern may develop due to the interaction between the warmer air masses over land and the cooler, moist air from the ocean. Increased wind shear could also lead to localized downdrafts in stormy areas, which may potentially trigger isolated severe weather events, such as gusty winds or brief thunderstorms.

#### 4. Areas of Concern
- **Coastal Regions**: Areas from southern China to parts of Japan, particularly around the low-pressure system, are likely to experience the most significant changes, including heavy rain and strong winds.
- **Urban Centers near the coast**: Cities in the impacted zones may face reduced visibility and potential flooding in low-lying areas.

#### 5. Short-Term Risks and Impacts
- **Aviation**: Increased turbulence and wind shear, particularly during take-off and landing in coastal airports, could pose risks.
- **Marine Activities**: Shipping and fishing activities should be cautious of elevated sea states and strong currents, especially near the low-pressure core.
- **Outdoor Events**: Given the likelihood of precipitation and shifting winds, outdoor events should be prepared for wet conditions and potential cancellations.

#### 6. Meteorological Processes and Uncertainties
The anticipated weather changes are largely driven by the interaction of the low-pressure system with warmer land air masses, leading to lift and precipitation. Additional uncertainties include variability in the exact track of the low-pressure system and local topographical influences that may enhance or diminish rainfall intensity. 

In conclusion, while predictions suggest significant weather impacts over the next hour, localized variations can occur due to inherent uncertainties in dynamic weather systems. Continuous monitoring and updates would be prudent to better assess developing conditions.
