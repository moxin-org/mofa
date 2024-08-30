
# Web Search Super Agent  Example
**任务目标:**
- 根据用户任务输入的任务从Google搜索结果中获取相关数据，通过Agent进行总结，并且得到和任务内容相关连的问题


# 1, 流程说明:
1. **[web_search_agent](use_case%2Fweb_search_agent.yml)** : 根据用户提出的问题，从Google中搜索对应的内容,并且将里面的网址和概括拿下来。给到Agent，让它结合Web中搜索的内容给出一个结果
2. **[more_question_agent](use_case%2Fmore_question_agent.yml)** : 根据用户提出的问题结合Web中搜索的答案以及上一个流程给出的结果，生成和问题相关性比较高的几个问题

## 启动

**如果你需要运行这个案例，请先安装mae，推荐在两个命令窗口按照顺序运行下面两个命令.**：
~~~
dora up && dora start  paper_dataflow.yml  --attach   
python3 task_input.py   
~~~

**语言**: 
- [English](README.md)

**案例日志查看**:
- [mae_web_search.md](data%2Foutput%2Flog%2Fmae_web_search.md)