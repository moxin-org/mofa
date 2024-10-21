import json
import os
from pathlib import Path

from dora import Node, DoraStatus
from openai import OpenAI

from mofa.utils.files.read import read_yaml
from mofa.utils.files.util import get_all_files
import os
import glob


def find_yml_files_with_dataflow(directory,file_local_name:str='dataflow'):
    # 使用 glob 模块查找目录下所有的 *.yml 文件
    yml_files = glob.glob(os.path.join(directory, "*.yml"))

    # 过滤文件名中包含 'dataflow' 的文件
    filtered_files = [file for file in yml_files if file_local_name in os.path.basename(file)]

    return filtered_files

markdown_path = os.getenv('markdown_path', "/Users/chenzi/Downloads/Final_evl")
text_dict = {}
readme_files = list(get_all_files(markdown_path, 'md'))
for readme_file in readme_files[7:]:
    with open(readme_file, 'r', encoding='utf-8') as file:
        dataflow_dir_path = str(Path(readme_file).parent)
        try:
            dataflow_yml  = find_yml_files_with_dataflow(dataflow_dir_path)[0]
            dataflow_data = json.dumps(read_yaml(dataflow_yml))

        except Exception as e :
            dataflow_data = ""
        dataflow_configs = dataflow_dir_path + '/configs'
        config_files = list(get_all_files(dataflow_configs, 'yml'))
        configs_data = ""
        for config_file in config_files:
            configs_data += json.dumps(read_yaml(config_file),ensure_ascii=False)
        text_dict[Path(readme_file).parent.name] = file.read() +"dataflow: "+ dataflow_data + "configs_data: "+configs_data



readme_data = json.dumps(text_dict,ensure_ascii=False)
prompt = f"""
Background:
Participants have designed advanced AI Agents using the latest technologies, such as multi-agent collaboration, Dora-RS and MoFA frameworks, and open-source large language models like Llama 3.2 405B, to solve complex problems. Each project provides a README file, a Dataflow file, and a model configuration file. As an expert judge, your goal is to evaluate each project's provided files, assessing their innovation and breakthrough achievements, and then determine the ranking of these projects based on their total scores.

Objective:
Your objective is to evaluate the provided README files, Dataflow, and model configuration files based on four aspects: Innovation or Breakthrough (50%), Technical Implementation (20%), Practicality (20%), and Completion (10%, default full marks, no need to fill in). Specifically, you need to assess key areas based on the details provided in these files (such as software name, team members, project introduction, technical development, data flow, model configuration, and case demonstrations). After evaluation, rank the projects from highest to lowest based on the total scores, selecting the top 10 projects with the highest scores.

Project Data:
Below are the README files, Dataflow, and model configuration files of the projects to be evaluated:

README Files:

Please insert each project's README file content here, following the template below:

# **Project Name: [Project Name]**

## **Team Name:**

[Team Name]

**Members:**

- [Member Name] (GitCode Username: [GitCode Username])
- [Member Name] (GitCode Username: [GitCode Username])
- ...

## **Project Repository:**

[Project Repository URL]

## **Environment Dependencies:**

1. **[Dependency 1]**
2. **[Dependency 2]**
3. ...

### **Installation Steps:**

[Detailed installation instructions]

### **Running the Program:**

1. **Run the main program:**

   ```bash
   [Run command]
Start the task input terminal:

Open another terminal window and run [Input Terminal Program Name].
In [Input Terminal Program Name], enter task instructions to interact with the program.
Software Introduction
[Project Name] is a [nature or characteristic of the software] software designed for [main functions or purposes]. Through [core technology or method], the software not only [function or advantage 1] but also [function or advantage 2].

Breakthroughs and Innovations:
[Innovation 1]: [Detailed description]
[Innovation 2]: [Detailed description]
...
Technical Development Introduction
Frameworks and Tools Used:
[Framework or Tool 1]: [Function or purpose]
[Framework or Tool 2]: [Function or purpose]
...
Technical Challenges:
[Technical Challenge 1]:
Challenge: [Description of the challenge]
Solution: [Description of the solution]
[Technical Challenge 2]:
Challenge: [Description of the challenge]
Solution: [Description of the solution]
...
Case Demonstrations
Case 1: [Case Title]
Prompt: [Prompt content]

Output:

[Program output content]

Analysis:

[Analysis or evaluation of the output]
Case 2: [Case Title]
Prompt: [Prompt content]

Output:

[Program output content]

Analysis:

[Analysis or evaluation of the output]
Case 3: [Case Title]
Prompt: [Prompt content]

Output:

[Program output content]

Analysis:

[Analysis or evaluation of the output]
...

复制代码
Dataflow Files:

Please insert each project's Dataflow file content here.

Model Configuration Files:

Please insert each project's model configuration file content here.

Evaluation Criteria:
The total score is 100 points, with the following scoring weights and detailed criteria:

1. Innovation or Breakthrough (50 points)
Evaluation Criteria:

Has the project made unprecedented attempts in the use of open-source large language models, AI Agent tools, Dataflow, and model configurations?
Has it surpassed the existing ChatGPT performance in some functions?
Considerations:

Unique Approach: Introduction of novel methods or frameworks not seen in existing solutions.
Advancement over Existing Models: Demonstrable improvements in performance, capabilities, or efficiency compared to existing models.
Integration of Technologies: Innovative combination of open-source models, AI Agent tools, Dataflow, and model configurations to create new functionalities.
Creativity in Problem-Solving: Original approaches to tackling challenges within AI and machine learning.
Why It Matters: Innovation and breakthroughs drive technological progress by introducing new methods, solving long-standing challenges, and enhancing the performance of existing technologies.

Scoring Guidelines:

45-50 points: Exceptional innovation with groundbreaking attempts that significantly surpass existing models in multiple aspects.
40-44 points: Strong innovation with notable advancements and clear improvements over existing models.
35-39 points: Good innovation with some unique features or improvements in specific functions.
30-34 points: Moderate innovation with enhancements that build upon existing technologies.
Below 30 points: Limited innovation with minimal or no significant advancements beyond current models.
2. Technical Implementation (20 points)
Evaluation Criteria:

Evaluate the technical complexity of the project, code quality, functionality completeness, and the rationality of the Dataflow and model configuration.
Considerations:

Technical Complexity: Use of advanced algorithms, architectures, or technologies.
Code Quality: Cleanliness, readability, documentation, and adherence to best coding practices.
Functionality Completeness: Implementation of all intended features with working functionalities.
Scalability and Performance: Ability of the system to perform efficiently under various conditions.
Design of Dataflow: Whether the data flow design is reasonable and efficient.
Rationality of Model Configuration: Whether the model configuration is optimized and suitable for the project requirements.
Why It Matters: A high-quality technical implementation ensures the project's reliability, scalability, maintainability, and usability.

Scoring Guidelines:

18-20 points: Excellent technical implementation with high complexity, superior code quality, complete functionalities, and well-designed Dataflow and model configuration.
15-17 points: Strong technical work with good code quality, mostly complete functionalities, minor areas for improvement in Dataflow or model configuration.
12-14 points: Adequate technical implementation with some complexity; noticeable areas for improvement; Dataflow or model configuration needs optimization.
8-11 points: Basic technical implementation; significant issues with code quality or incomplete functionalities.
Below 8 points: Poor technical implementation with major flaws in code quality and functionality.
3. Practicality (20 points)
Evaluation Criteria:

Does the project have the potential to solve real-world problems?
Can it be practically applied?
Considerations:

Real-World Relevance: Alignment with current industry needs or societal challenges.
Applicability: Ease with which the solution can be integrated into existing systems or processes.
User Impact: Potential benefits to end-users, including improvements in efficiency, cost savings, or user experience.
Market Potential: Opportunity for adoption in relevant markets or industries.
Why It Matters: Practicality determines the project's value in real-world applications and its potential impact on society or industry.

Scoring Guidelines:

18-20 points: Highly practical with clear, significant benefits and strong potential for real-world adoption.
15-17 points: Practical with identifiable applications and benefits; some considerations needed for implementation.
12-14 points: Moderately practical; potential applications exist but may require further development.
8-11 points: Limited practicality with few real-world applications; significant challenges to implementation.
Below 8 points: Low practicality with unclear applications and minimal potential impact.
4. Completion (10 points)
Evaluation Criteria: Participants have submitted a complete system that can be run.

Note: The initial screening stage has ensured project completeness. Default score is 10 points; judges do not need to evaluate this item.

Tasks:
Review each project's README file, Dataflow, and model configuration file to understand the project's technology, concepts, and applications.

Assess the first three dimensions (Innovation or Breakthrough, Technical Implementation, Practicality) by assigning scores according to the detailed scoring guidelines and providing detailed reasoning.

Compare the total scores of all projects (out of 100 points).

Select the top 10 projects with the highest total scores.

Rank the selected projects from highest to lowest total score.

Document your evaluations using the provided template, ensuring consistency and fairness.

Evaluation Logic Template:
Project Evaluation: [Project Name]
1. Innovation or Breakthrough (50 points)

Evaluation Criteria: Assess the project's unprecedented attempts in using open-source large language models, AI Agent tools, Dataflow, and model configurations, and whether it surpasses ChatGPT in some functions.

Why It Matters: Drives technological progress by introducing new methods and enhancing existing technologies.

Score: X points

Reasoning: Provide detailed justification, citing specific examples from the README, Dataflow, and model configuration files that demonstrate innovation and breakthroughs.

2. Technical Implementation (20 points)

Evaluation Criteria: Evaluate the technical complexity, code quality, functionality completeness, and the rationality of the Dataflow and model configuration.

Why It Matters: Ensures the project's reliability, scalability, and usability.

Score: X points

Reasoning: Detail the technical aspects, code quality, and completeness of functionalities, referencing the README, Dataflow, and model configuration files.

3. Practicality (20 points)

Evaluation Criteria: Determine the project's potential to solve real-world problems and its applicability.

Why It Matters: Measures the project's value and impact on society or industry.

Score: X points

Reasoning: Explain how the project can be applied in real-world scenarios and the benefits it offers, citing relevant information from the provided files.

4. Completion (10 points)

Score: 10 points (Default)
Total Score: X points (out of 100)

Overall Evaluation: Summarize the project's strengths and areas for improvement, providing a balanced assessment.
Ranking Summary:
After evaluating all projects, select the top 10 projects with the highest scores and rank them as follows:

Project Name - Total Score: X points

Reasoning: Highlight why this project stands out, referencing the evaluation criteria.
Project Name - Total Score: X points

Reasoning: ...
(Continue ranking up to the 10th project.)

Detailed Instructions:
Insert Project Data:

In the Project Data section, insert each project's README file, Dataflow, and model configuration file content.
Conduct Evaluations:

For each project, state the evaluation criteria and explain why it matters before assigning a score and providing detailed reasoning.

Ensure that your reasoning is thorough and directly references information from the README, Dataflow, and model configuration files.

Scoring:

Be objective and consistent in your scoring across all projects.

Use the Scoring Guidelines provided to determine the appropriate score range.

Selection and Ranking:

After all evaluations, calculate each project's total score (out of 100).

Select the top 10 projects with the highest total scores.

Rank the selected projects from highest to lowest total score.

Provide detailed explanations for the ranking, highlighting specific strengths and areas where the project excelled or lacked.

Note:
Based on Provided Information: All assessments should be based solely on the information provided in the README files, Dataflow, and model configuration files.

Avoid External Biases: Avoid any external biases or assumptions not supported by the provided data.

Fair and Just: The final evaluation should be thorough, fair, and reflective of each project's actual performance.

I believe that using multimodal approaches, along with employing crawlers and LLM-based prediction, can lead to better extra-credit projects

this all data:
{text_dict}
"""
# 请替换为您的实际 API 密钥
api_key = ' '

client = OpenAI(api_key=api_key)

messages = [
    {"role": "system", "content": "You are an expert AI assistant helping to evaluate software projects based on their README files."},
    {"role": "user", "content": prompt}
]
response = client.chat.completions.create(
    model="gpt-4o",  # 或者使用 'gpt-3.5-turbo'，如果您没有 gpt-4 的权限
    messages=messages,
    temperature=0.7,
    stream=True,  # 启用流式输出
)
result = []
if response:
    if True:
        # 对于流式输出，遍历 response 并收集每个 chunk 的内容
        for chunk in response:
            response_text = chunk.choices[0].delta.content
            if response_text is not None:
                result.append(response_text)
final_result = ' '.join(result) if result else "No output available."
final_result = final_result.replace('  ', '').replace(' ', '')
print(final_result)



