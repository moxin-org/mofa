import json
import os
from pathlib import Path

from dora import Node, DoraStatus
import pyarrow as pa
from openai import OpenAI

from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.files.util import get_all_files
from mofa.utils.log.agent import record_agent_result_log

# yaml_file_path = "/Users/chenzi/project/zcbc/mofa/python/Agent_Evaluation/configs/agent.yml"
# inputs = load_agent_config(yaml_file_path)
# markdown_path = os.getenv('markdown_path', "/Users/chenzi/project/zcbc/mofa/python/examples")
# text_dict = {}
# readme_files = list(get_all_files(markdown_path, 'md'))
# for readme_file in readme_files:
#     with open(readme_file, 'r', encoding='utf-8') as file:
#         text_dict[Path(readme_file).parent.name] = file.read()
# inputs['input_fields'] = text_dict
# print('inputs: ', inputs)
# agent_result = run_dspy_or_crewai_agent(agent_config=inputs)

import openai
import os
markdown_path = os.getenv('markdown_path', "/Users/chenzi/project/zcbc/mofa/python/examples")
text_dict = {}
readme_files = list(get_all_files(markdown_path, 'md'))
for readme_file in readme_files:
    with open(readme_file, 'r', encoding='utf-8') as file:
        text_dict[Path(readme_file).parent.name] = file.read()
readme_data = json.dumps(text_dict)
prompt = f"""
Background:
Participants have designed advanced AI Agents using the latest technologies, such as multi-agent collaboration, Dora-RS and MoFA frameworks, and open-source large language models like Llama 3.2 405B, to solve complex problems. As an expert judge, your goal is to evaluate each project's README file, assessing their innovation and breakthrough achievements, and then determine the ranking of these projects based on their total scores.

Objective:
Your goal is to evaluate the provided README files based on four aspects: Innovation or Breakthrough, Technical Implementation, Practicality, and Completion (default 10 points, no need to fill in). Specifically, you need to assess key areas based on the details provided in the README (such as software name, team members, project introduction, technical development, and case comparisons). After evaluation, rank the projects from highest to lowest based on the total scores, selecting the top 10 projects with the highest scores.

README Data:
Below are the README files of the projects to be evaluated:

Please insert all the examples from {readme_data} here for analysis.

Evaluation Criteria:
The total score is 100 points, with the following scoring weights and detailed criteria:

1. Innovation or Breakthrough (50 points)
Evaluation Criteria: Has the project made unprecedented attempts in the use of open-source large language models and AI Agent tools? Has it surpassed the existing ChatGPT performance in some functions?

Considerations:
Uniqueness of Approach: Introduction of novel methods or frameworks not seen in existing solutions.
Advancement over Existing Models: Demonstrable improvements in performance, capabilities, or efficiency compared to models like ChatGPT.
Integration of Technologies: Innovative combination of open-source models and AI Agent tools to create new functionalities.
Creativity in Problem-Solving: Original approaches to tackling challenges within AI and machine learning.
Why It Matters: Innovation and breakthroughs drive technological progress by introducing new methods, solving long-standing challenges, and enhancing the performance of existing technologies.

Scoring Guidelines:

45-50 points: Exceptional innovation with groundbreaking attempts that significantly surpass existing models in multiple aspects.
40-44 points: Strong innovation with notable advancements and clear improvements over existing models.
35-39 points: Good innovation with some unique features or improvements in specific functions.
30-34 points: Moderate innovation with enhancements that build upon existing technologies.
Below 30 points: Limited innovation with minimal or no significant advancements beyond current models.
2. Technical Implementation (20 points)
Evaluation Criteria: Evaluate the technical complexity of the project, code quality, and functionality completeness.

Considerations:
Technical Complexity: Use of advanced algorithms, architectures, or technologies.
Code Quality: Cleanliness, readability, documentation, and adherence to best coding practices.
Functionality Completeness: Implementation of all intended features with working functionalities.
Scalability and Performance: Ability of the system to perform efficiently under various conditions.
Why It Matters: A high-quality technical implementation ensures the project's reliability, scalability, maintainability, and usability.

Scoring Guidelines:

18-20 points: Excellent technical implementation with high complexity, superior code quality, and complete functionalities.
15-17 points: Strong technical work with good code quality and mostly complete functionalities; minor issues present.
12-14 points: Adequate technical implementation with some complexity; noticeable areas for improvement.
8-11 points: Basic technical implementation; significant issues with code quality or incomplete functionalities.
Below 8 points: Poor technical implementation with major flaws in code quality and functionality.
3. Practicality (20 points)
Evaluation Criteria: Does the project have the potential to solve real-world problems? Can it be practically applied?

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
Review each README file to understand the project's technology, concepts, and applications.

Assess the first three dimensions (Innovation or Breakthrough, Technical Implementation, Practicality) by assigning scores according to the detailed scoring guidelines and providing detailed reasoning.

Compare the total scores of all projects.

Select the top 10 projects with the highest total scores.

Rank the selected projects from highest to lowest total score.

Document your evaluations using the provided template, ensuring consistency and fairness.

Evaluation Logic Template:
For each project, structure your evaluation as follows:

Project Evaluation: [Project Name]
Innovation or Breakthrough (50 points)

Evaluation Criteria: Assess the project's unprecedented attempts in using open-source large language models and AI Agent tools, and whether it surpasses ChatGPT in some functions.

Why It Matters: Drives technological progress by introducing new methods and enhancing existing technologies.

Score: X points

Reasoning: Provide detailed justification, citing specific examples from the README that demonstrate innovation and breakthroughs.

Technical Implementation (20 points)

Evaluation Criteria: Evaluate the technical complexity, code quality, and functionality completeness.

Why It Matters: Ensures reliability, scalability, and usability of the project.

Score: X points

Reasoning: Detail the technical aspects, code quality, and completeness of functionalities, referencing the README.

Practicality (20 points)

Evaluation Criteria: Determine the project's potential to solve real-world problems and its applicability.

Why It Matters: Measures the project's value and impact on society or industry.

Score: X points

Reasoning: Explain how the project can be applied in real-world scenarios and the benefits it offers.

Completion (10 points)

Score: 10 points (Default)
Total Score: X points (out of 100)

Overall Reasoning: Summarize the project's strengths and areas for improvement, providing a balanced assessment.
Ranking Summary:
After evaluating all projects, select the top 10 projects and rank them as follows:

Project Name - Total Score: X points

Reasoning: Highlight why this project stands out, referencing the evaluation criteria.
Project Name - Total Score: X points

Reasoning: ...
(Continue ranking up to the 10th project.)

Detailed Instructions:
Insert README Data:

Replace the placeholder text in the README Data section with the actual content of each project's README file.
Conduct Evaluations:

For each project, state the evaluation criteria and explain why it matters before assigning a score and providing detailed reasoning.

Ensure that your reasoning is thorough and directly references information from the README files.

Scoring:

Be objective and consistent in your scoring across all projects.

Use the Scoring Guidelines provided to determine the appropriate score range.

Selection and Ranking:

After all evaluations, calculate each project's total score (out of 100).

Select the top 10 projects with the highest total scores.

Rank the selected projects from highest to lowest total score.

Provide detailed explanations for the ranking, highlighting specific strengths and areas where the project excelled or lacked.

Note:
All assessments should be based solely on the information provided in the README files.

Avoid any external biases or assumptions not supported by the provided data.

The final evaluation should be thorough, fair, and reflective of each project's merits.

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



