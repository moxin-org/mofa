# Web Search Super Agent Example
**Task Objective:**
- Based on the user's input task, retrieve relevant data from Google search results, summarize it through an Agent, and generate related questions based on the task content.

# 1. Process Description:
1. **[web_search_agent](use_case%2Fweb_search_agent.yml)**: Based on the user's question, search for the corresponding content on Google, extract URLs and summaries from the results, and provide them to the Agent. The Agent will then combine the web search results to provide an answer.
2. **[more_question_agent](use_case%2Fmore_question_agent.yml)**: Based on the user's question, the answer from the web search, and the result from the previous process, generate several highly relevant questions.

## Launching

**If you need to run this example, please install mae first. It is recommended to run the following two commands in two separate command windows in order:**
~~~
dora up && dora start  paper_dataflow.yml  --attach   
python3 task_input.py   
~~~


**Case Log Viewing**:
- [mae_web_search.md](data%2Foutput%2Flog%2Fmae_web_search.md)

**Language**: 
- [中文](README_zh.md)