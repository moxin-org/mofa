
# Super Agent  Example
下面这个案例是我们使用多个小的Reasoner-Agent实现的Self-Refine的Super-Agent

# 1, 流程说明:
use_case : [self_refine_super_agent](self_refine_super_agent.yml)  
1. [writer_agent](use_case%2Fwriter_agent.yml)  : 负责根据任务,使用reasoner-agent,然后调用LLM生成结果
2. [feedback_agent](use_case%2Ffeedback_agent.yml)  :  负责根据问题以及`feedback_agent`生成的结果,给出关于结果的建议
3. [refinement_agent](use_case%2Frefinement_agent.yml)  :  根据问题和结果以及`feedback_agent`反馈的结果,让LLM根据建议优化结果
4. [evaluation_agent](use_case%2Fevaluation_agent.yml)  :  根据问题和`refinement_agent`的结果,评估结果是否符合要求,如果符合则返回结果. 如果不符合则判断重复次数,如果重复次数到达某个阈值,则返回结果.否则重新去调用`feedback_agent`


## 启动

**如果你需要运行这个案例，请先安装mae，然后运行下面的命令**：
~~~
dora up && dora start  self_refine_super_agent.yml  --attach
~~~

**如果你需要对配置进行修改,请查看[README_zh.md](..%2F..%2F..%2Fdocs%2FREADME_zh.md)**


**语言**: 
- [English](README.md)