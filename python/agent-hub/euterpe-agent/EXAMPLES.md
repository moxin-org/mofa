# Euterpe Agent 使用示例集合

本文档提供了一系列实际使用场景的示例，展示如何利用 Euterpe Agent 生成各种类型的视频内容。每个示例都包括完整的 JSON 参数配置和详细说明。

## 目录

1. [基本示例](#1-基本示例)
2. [商业与营销视频](#2-商业与营销视频)
3. [教育与教学视频](#3-教育与教学视频)
4. [艺术与创意视频](#4-艺术与创意视频)
5. [与其他 Agent 集成的示例](#5-与其他-agent-集成的示例)
6. [批处理示例](#6-批处理示例)

## 1. 基本示例

### 1.1 最简示例

这是一个最简单的示例，仅包含必要的参数：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "A beautiful landscape with mountains and a lake"
    },
    {
      "timestamp": 5.0,
      "prompt": "Same landscape during sunset, with orange sky"
    }
  ],
  "output_dir": "./euterpe_output"
}
```

### 1.2 带音乐的基本示例

添加背景音乐：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "A beautiful landscape with mountains and a lake"
    },
    {
      "timestamp": 5.0,
      "prompt": "Same landscape during sunset, with orange sky"
    }
  ],
  "music": {
    "prompt": "Calm and peaceful instrumental music with piano",
    "duration": 10.0
  },
  "output_dir": "./euterpe_output"
}
```

### 1.3 指定所有基本参数

完整指定所有常用参数：

```json
{
  "keyframes": [
    {
      "frame_id": "intro",
      "timestamp": 0.0,
      "prompt": "A beautiful landscape with mountains and a lake",
      "negative_prompt": "people, buildings, text, watermark"
    },
    {
      "frame_id": "sunset",
      "timestamp": 5.0,
      "prompt": "Same landscape during sunset, with orange sky",
      "negative_prompt": "people, buildings, text, watermark"
    }
  ],
  "music": {
    "prompt": "Calm and peaceful instrumental music with piano",
    "duration": 10.0,
    "genre": "ambient",
    "tempo": 80,
    "format": "mp3"
  },
  "output_dir": "./euterpe_output/basic_example",
  "aspect_ratio": "16:9",
  "image_model": "kling-v1-5",
  "fps": 30,
  "resolution": 720
}
```

## 2. 商业与营销视频

### 2.1 产品展示

适合展示产品特性和使用场景的视频：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "A sleek modern smartphone floating in white space, high-quality product photography, clean background",
      "negative_prompt": "people, hands, text, low quality, blurry"
    },
    {
      "timestamp": 3.0,
      "prompt": "Same smartphone from different angle showing profile view, with screen displaying colorful app interface",
      "negative_prompt": "people, hands, text, low quality, blurry"
    },
    {
      "timestamp": 6.0,
      "prompt": "Close-up of smartphone screen showing detailed app interface with graphs and charts",
      "negative_prompt": "people, hands, text, low quality, blurry"
    },
    {
      "timestamp": 9.0,
      "prompt": "Smartphone being used outdoors in a coffee shop setting, showing everyday usage scenario",
      "negative_prompt": "text, low quality, blurry"
    },
    {
      "timestamp": 12.0,
      "prompt": "Multiple smartphones arranged in a row showing different color options, product lineup display",
      "negative_prompt": "people, hands, text, low quality, blurry"
    }
  ],
  "music": {
    "prompt": "Modern upbeat corporate technology music, professional and positive",
    "duration": 15.0,
    "tempo": 100
  },
  "output_dir": "./euterpe_output/product_showcase",
  "aspect_ratio": "16:9",
  "resolution": 1080,
  "fps": 30
}
```

### 2.2 品牌故事

讲述品牌创立和发展历程的视频：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Old black and white photograph of a small workshop in the 1950s with vintage machinery",
      "negative_prompt": "color, modern, text"
    },
    {
      "timestamp": 5.0,
      "prompt": "1970s style photograph of growing factory with workers and expanded production line, slightly sepia toned",
      "negative_prompt": "modern computers, smartphones, text"
    },
    {
      "timestamp": 10.0,
      "prompt": "1990s style photograph of modern office building with company logo, business people with vintage computers",
      "negative_prompt": "smartphones, text, modern technology"
    },
    {
      "timestamp": 15.0,
      "prompt": "Modern sleek headquarters building with glass facade in beautiful sunshine, contemporary architectural photography",
      "negative_prompt": "text, watermark"
    },
    {
      "timestamp": 20.0,
      "prompt": "Diverse team of professionals in modern office space collaborating around high-tech displays",
      "negative_prompt": "text, watermark"
    }
  ],
  "music": {
    "prompt": "Inspirational corporate music that builds from simple and nostalgic to modern and powerful, storytelling journey",
    "duration": 25.0
  },
  "output_dir": "./euterpe_output/brand_story",
  "aspect_ratio": "16:9",
  "resolution": 1080
}
```

### 2.3 活动宣传

宣传即将到来的活动或会议的视频：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Elegant conference hall being prepared for an event, wide angle view, professional lighting",
      "negative_prompt": "people, text, watermarks"
    },
    {
      "timestamp": 3.0,
      "prompt": "Same conference hall filled with attendees, business people networking before presentation",
      "negative_prompt": "text, watermarks, poor quality"
    },
    {
      "timestamp": 6.0,
      "prompt": "Professional speaker on stage with presentation screen behind, audience visible in foreground",
      "negative_prompt": "text, watermarks, poor quality"
    },
    {
      "timestamp": 9.0,
      "prompt": "Interactive workshop session with small groups of people collaborating around tables",
      "negative_prompt": "text, watermarks, poor quality"
    },
    {
      "timestamp": 12.0,
      "prompt": "Evening networking reception with elegant lighting, people conversing with drinks",
      "negative_prompt": "text, watermarks, poor quality"
    }
  ],
  "music": {
    "prompt": "Energetic business event music, professional and motivating with a steady beat",
    "duration": 15.0,
    "tempo": 110
  },
  "output_dir": "./euterpe_output/event_promo",
  "aspect_ratio": "16:9",
  "resolution": 1080,
  "fps": 30
}
```

## 3. 教育与教学视频

### 3.1 科学概念讲解

展示科学概念或自然现象的视频：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Visualization of the solar system with sun at center and planets in orbit, educational style, scientifically accurate",
      "negative_prompt": "text, people, cartoonish, childish"
    },
    {
      "timestamp": 5.0,
      "prompt": "Close-up view of Earth and Moon showing their relative sizes and distance, realistic space visualization",
      "negative_prompt": "text, people, cartoonish, childish"
    },
    {
      "timestamp": 10.0,
      "prompt": "Cross-section view of Earth showing the core, mantle and crust layers, educational diagram style",
      "negative_prompt": "text, people, cartoonish, childish"
    },
    {
      "timestamp": 15.0,
      "prompt": "Tectonic plate boundaries with visible plate movement and magma, educational geology visualization",
      "negative_prompt": "text, people, cartoonish, childish"
    },
    {
      "timestamp": 20.0,
      "prompt": "Volcanic eruption showing cross-section of volcano with magma chamber and lava flow, educational style",
      "negative_prompt": "text, people, cartoonish, childish"
    }
  ],
  "music": {
    "prompt": "Educational documentary background music, subtle and scientific, suitable for learning",
    "duration": 25.0,
    "tempo": 70
  },
  "output_dir": "./euterpe_output/science_education",
  "aspect_ratio": "16:9",
  "resolution": 1080
}
```

### 3.2 历史事件讲述

讲述历史事件或时期的视频：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Ancient Egyptian construction site of the Great Pyramid of Giza, thousands of workers, realistic historical scene",
      "negative_prompt": "modern, text, anachronistic elements"
    },
    {
      "timestamp": 6.0,
      "prompt": "Egyptian workers cutting and moving limestone blocks using rope and wooden sleds, realistic historical reconstruction",
      "negative_prompt": "modern, text, anachronistic elements"
    },
    {
      "timestamp": 12.0,
      "prompt": "Egyptian engineers using simple tools to ensure precision alignment of the pyramid blocks, realistic historical scene",
      "negative_prompt": "modern, text, anachronistic elements"
    },
    {
      "timestamp": 18.0,
      "prompt": "Partially completed Great Pyramid with ramps for moving blocks to higher levels, realistic historical reconstruction",
      "negative_prompt": "modern, text, anachronistic elements"
    },
    {
      "timestamp": 24.0,
      "prompt": "Completed Great Pyramid of Giza with white limestone casing stones intact, as it looked when newly built, realistic historical scene",
      "negative_prompt": "modern, text, anachronistic elements"
    }
  ],
  "music": {
    "prompt": "Ancient Egyptian themed music with string instruments and percussion, mysterious and historical",
    "duration": 30.0
  },
  "output_dir": "./euterpe_output/history_education",
  "aspect_ratio": "16:9",
  "resolution": 1080
}
```

### 3.3 编程教程

展示编程概念的视频：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Clean modern coding workspace with computer screen showing Python code, programming IDE in dark mode",
      "negative_prompt": "text, people, handwritten"
    },
    {
      "timestamp": 4.0,
      "prompt": "Visual representation of variables and data types in Python, showing integers, strings and lists as physical objects, educational visualization",
      "negative_prompt": "text, people"
    },
    {
      "timestamp": 8.0,
      "prompt": "Flowchart visualization of a Python function with input and output, showing data flow, educational style",
      "negative_prompt": "text, people"
    },
    {
      "timestamp": 12.0,
      "prompt": "Visual representation of a Python loop iterating through a list, showing each step, educational programming concept visualization",
      "negative_prompt": "text, people"
    },
    {
      "timestamp": 16.0,
      "prompt": "Python code running on multiple devices, showing cross-platform compatibility, computers and mobile devices",
      "negative_prompt": "text, people"
    }
  ],
  "music": {
    "prompt": "Technology tutorial background music, modern electronic with a steady beat, focused and analytical",
    "duration": 20.0,
    "tempo": 90
  },
  "output_dir": "./euterpe_output/programming_tutorial",
  "aspect_ratio": "16:9",
  "resolution": 1080
}
```

## 4. 艺术与创意视频

### 4.1 抽象艺术

纯粹的视觉艺术体验视频：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Abstract fluid art with vibrant flowing colors, purple and blue swirling together like cosmic nebula, high quality digital art",
      "negative_prompt": "realistic, photograph, text, faces, people, concrete objects"
    },
    {
      "timestamp": 4.0,
      "prompt": "Abstract fluid art transitioning to warm colors, red and orange flowing like lava, stylized digital painting",
      "negative_prompt": "realistic, photograph, text, faces, people, concrete objects"
    },
    {
      "timestamp": 8.0,
      "prompt": "Abstract geometric patterns emerging from the fluid colors, sacred geometry forms in gold on dark background",
      "negative_prompt": "realistic, photograph, text, faces, people, concrete objects"
    },
    {
      "timestamp": 12.0,
      "prompt": "Abstract digital fractal patterns growing and evolving, intricate and complex, green and turquoise colors",
      "negative_prompt": "realistic, photograph, text, faces, people, concrete objects"
    },
    {
      "timestamp": 16.0,
      "prompt": "Abstract cosmic scene with particles and light rays, ethereal and spiritual, purple and white colors",
      "negative_prompt": "realistic, photograph, text, faces, people, concrete objects"
    }
  ],
  "music": {
    "prompt": "Ambient electronic music with subtle evolving textures, ethereal and otherworldly, suitable for meditation",
    "duration": 20.0,
    "tempo": 70
  },
  "output_dir": "./euterpe_output/abstract_art",
  "aspect_ratio": "16:9",
  "image_model": "kling-v2",
  "resolution": 1080
}
```

### 4.2 幻想风景

创造不存在的风景场景：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Fantasy landscape with floating islands in the sky, waterfalls pouring off the edges, lush vegetation, magical lighting",
      "negative_prompt": "text, people, modern, buildings"
    },
    {
      "timestamp": 5.0,
      "prompt": "Fantasy crystal cave with giant glowing crystals in vibrant colors, magical light beams, underground lake with reflections",
      "negative_prompt": "text, people, modern, buildings"
    },
    {
      "timestamp": 10.0,
      "prompt": "Fantasy bioluminescent forest at night, glowing plants and mushrooms, magical particles in the air, moonlight through trees",
      "negative_prompt": "text, people, modern, buildings"
    },
    {
      "timestamp": 15.0,
      "prompt": "Fantasy ancient ruins overgrown with magical plants, stone arches and columns, mystical symbols glowing, fog and mist",
      "negative_prompt": "text, people, modern, buildings"
    },
    {
      "timestamp": 20.0,
      "prompt": "Fantasy mountain peak above clouds at sunrise, dragon silhouettes flying in distance, magical aurora in sky",
      "negative_prompt": "text, people, modern, buildings"
    }
  ],
  "music": {
    "prompt": "Epic fantasy orchestral music with choir, magical and adventurous, inspired by movie soundtracks",
    "duration": 25.0
  },
  "output_dir": "./euterpe_output/fantasy_landscapes",
  "aspect_ratio": "21:9",
  "image_model": "kling-v2",
  "resolution": 1080
}
```

### 4.3 艺术风格变化

展示同一场景在不同艺术风格下的变化：

```json
{
  "keyframes": [
    {
      "timestamp": 0.0,
      "prompt": "Still life with fruit bowl in realistic Renaissance painting style, oil painting, detailed, Caravaggio lighting",
      "negative_prompt": "text, people, modern, cubism, abstract"
    },
    {
      "timestamp": 4.0,
      "prompt": "Same still life with fruit bowl in Impressionist style, visible brushstrokes, vibrant colors, Monet style",
      "negative_prompt": "text, people, modern, renaissance, realistic, cubism"
    },
    {
      "timestamp": 8.0,
      "prompt": "Same still life with fruit bowl in Cubist style, fragmented and geometric, multiple perspectives, Picasso style",
      "negative_prompt": "text, people, modern, renaissance, realistic, impressionist"
    },
    {
      "timestamp": 12.0,
      "prompt": "Same still life with fruit bowl in Surrealist style, dreamlike and impossible elements, Salvador Dali style",
      "negative_prompt": "text, people, modern, renaissance, realistic, impressionist, cubism"
    },
    {
      "timestamp": 16.0,
      "prompt": "Same still life with fruit bowl in Pop Art style, bold colors and outlines, Andy Warhol style",
      "negative_prompt": "text, people, renaissance, realistic, impressionist, cubism, surrealism"
    }
  ],
  "music": {
    "prompt": "Classical music that evolves through different musical periods from baroque to modern, artistic and evolving",
    "duration": 20.0
  },
  "output_dir": "./euterpe_output/art_style_evolution",
  "aspect_ratio": "16:9",
  "image_model": "kling-v2",
  "resolution": 1080
}
```

## 5. 与其他 Agent 集成的示例

### 5.1 与 LLM Agent 集成

以下是一个 LLM Agent 的示例实现，它生成关键帧描述，然后传递给 Euterpe Agent：

```python
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

@run_agent
def run(agent: MofaAgent):
    try:
        # 加载环境变量
        load_dotenv('.env.secret')
        
        # 获取用户输入
        user_input = agent.receive_parameter('query')
        agent.logger.info(f"Received query: {user_input}")
        
        # 初始化 OpenAI 客户端
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # 构建 prompt
        prompt = f"""
        Based on this description: "{user_input}"
        
        Create 3 keyframes for a short video. Each keyframe should include:
        1. A timestamp (in seconds, starting from 0)
        2. A detailed visual prompt describing what should be in the frame
        3. Optional negative prompts for elements to avoid
        
        Also create a music prompt that matches the mood and theme.
        
        Format your response as a JSON object with the following structure:
        {{
          "keyframes": [
            {{
              "timestamp": <number>,
              "prompt": "<detailed visual description>",
              "negative_prompt": "<elements to avoid>"
            }},
            ...
          ],
          "music": {{
            "prompt": "<music description>",
            "duration": <total duration in seconds>
          }}
        }}
        
        Only return the JSON object with no additional text.
        """
        
        # 调用 OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a creative video storyboard assistant that creates detailed keyframe descriptions for AI video generation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        # 获取生成的 JSON 结果
        result_json = response.choices[0].message.content.strip()
        
        # 解析 JSON 确保有效
        try:
            parsed_json = json.loads(result_json)
            # 添加其他必要参数
            parsed_json["output_dir"] = "./euterpe_output"
            parsed_json["aspect_ratio"] = "16:9"
            parsed_json["image_model"] = "kling-v1-5"
            parsed_json["fps"] = 30
            parsed_json["resolution"] = 720
            
            # 转回 JSON 字符串
            final_json = json.dumps(parsed_json, indent=2)
            
            # 发送给 Euterpe Agent
            agent.send_output(agent_output_name='llm_result', agent_result=final_json)
            
        except json.JSONDecodeError:
            agent.logger.error("Failed to parse LLM response as JSON")
            agent.send_output(
                agent_output_name='llm_result',
                agent_result={"error": "Failed to generate valid keyframe data"}
            )
        
    except Exception as e:
        agent.logger.error(f"Error in LLM agent: {str(e)}")
        agent.send_output(
            agent_output_name='llm_result',
            agent_result={"error": str(e)}
        )

def main():
    agent = MofaAgent(agent_name='llm-to-euterpe')
    run(agent=agent)

if __name__ == "__main__":
    main()
```

对应的数据流配置：

```yaml
nodes:
  - id: terminal-input
    build: pip install -e ../../node-hub/terminal-input
    path: dynamic
    outputs: data
    inputs:
      agent_response: euterpe-agent/euterpe_result

  - id: llm-to-euterpe
    build: pip install -e ../../agent-hub/llm-to-euterpe
    path: llm-to-euterpe
    outputs: llm_result
    inputs:
      query: terminal-input/data
    
  - id: euterpe-agent
    build: pip install -e ../../agent-hub/euterpe-agent
    path: euterpe-agent
    outputs: euterpe_result
    inputs:
      params: llm-to-euterpe/llm_result
    env:
      IS_DATAFLOW_END: true
      WRITE_LOG: true
```

### 5.2 与其他多个 Agent 集成

一个更复杂的数据流示例：

```yaml
nodes:
  - id: terminal-input
    build: pip install -e ../../node-hub/terminal-input
    path: dynamic
    outputs: data
    inputs:
      agent_response: euterpe-agent/euterpe_result

  - id: llm-to-euterpe
    build: pip install -e ../../agent-hub/llm-to-euterpe
    path: llm-to-euterpe
    outputs: llm_result
    inputs:
      query: terminal-input/data
    
  - id: image-enhancer
    build: pip install -e ../../agent-hub/image-enhancer
    path: image-enhancer
    outputs: enhanced_params
    inputs:
      params: llm-to-euterpe/llm_result
      
  - id: euterpe-agent
    build: pip install -e ../../agent-hub/euterpe-agent
    path: euterpe-agent
    outputs: euterpe_result
    inputs:
      params: image-enhancer/enhanced_params
    env:
      IS_DATAFLOW_END: true
      WRITE_LOG: true
  
  - id: notification-agent
    build: pip install -e ../../agent-hub/notification-agent
    path: notification-agent
    outputs: notification_result
    inputs:
      status: euterpe-agent/euterpe_result
```

## 6. 批处理示例

### 6.1 多视频批处理

处理多个视频生成任务的 JSON 格式：

```json
[
  {
    "keyframes": [
      {
        "timestamp": 0.0,
        "prompt": "Mountain landscape in spring, green valleys, snow on peaks"
      },
      {
        "timestamp": 5.0,
        "prompt": "Same mountains in summer, lush green everywhere"
      }
    ],
    "music": {
      "prompt": "Cheerful spring music with birds and light instruments",
      "duration": 10.0
    },
    "output_dir": "./euterpe_output/seasons/spring_summer"
  },
  {
    "keyframes": [
      {
        "timestamp": 0.0,
        "prompt": "Mountain landscape in autumn, red and orange foliage"
      },
      {
        "timestamp": 5.0,
        "prompt": "Same mountains in winter, covered in snow, barren trees"
      }
    ],
    "music": {
      "prompt": "Melancholic autumn music transitioning to winter sounds",
      "duration": 10.0
    },
    "output_dir": "./euterpe_output/seasons/autumn_winter"
  }
]
```

### 6.2 批处理脚本示例

处理批量任务的简单 Python 脚本：

```python
import json
import os
import sys
import time
import subprocess

def process_batch(batch_file):
    """
    处理批量视频生成请求
    
    Args:
        batch_file: 包含批处理任务的JSON文件路径
    """
    # 读取批处理文件
    with open(batch_file, 'r') as f:
        batch_tasks = json.load(f)
    
    # 确保是数组格式
    if not isinstance(batch_tasks, list):
        batch_tasks = [batch_tasks]
    
    print(f"Found {len(batch_tasks)} tasks to process")
    
    # 逐个处理任务
    for i, task in enumerate(batch_tasks):
        print(f"\nProcessing task {i+1}/{len(batch_tasks)}")
        
        # 创建临时JSON文件
        temp_file = f"temp_task_{i}.json"
        with open(temp_file, 'w') as f:
            json.dump(task, f)
        
        # 调用终端输入命令
        try:
            print(f"Sending task to Euterpe Agent...")
            
            # 将JSON文件内容作为输入发送到terminal-input
            with open(temp_file, 'r') as f:
                task_json = f.read()
                
            # 使用echo命令将内容传递给terminal-input
            cmd = f'echo \'{task_json}\' | terminal-input'
            subprocess.run(cmd, shell=True)
            
            # 等待处理完成
            print(f"Task {i+1} submitted. Waiting for processing...")
            time.sleep(5)  # 添加一些延迟，等待处理完成
            
        except Exception as e:
            print(f"Error processing task {i+1}: {str(e)}")
        
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print("\nAll tasks submitted.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_process.py <batch_file.json>")
        sys.exit(1)
    
    batch_file = sys.argv[1]
    process_batch(batch_file)
```

使用方法：

```bash
# 启动数据流
dora up
dora build euterpe_dataflow.yml
dora start euterpe_dataflow.yml

# 在另一个终端中运行批处理脚本
python batch_process.py batch_tasks.json
```
