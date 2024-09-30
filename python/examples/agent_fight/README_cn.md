# Agent Fight  

## 1. 功能说明
用于对比和评估两个Agent或LLM的输出结果.在多个维度上面进行打分和评估，比较两个输出结果相对的品质好坏。

## 2. 使用场景
竞赛中，对完成同样工作的LLM或智能体的输出结果进行评估和比较。

## 3. 配置方法
通过更改`agent-hub`下面的`content-evaluation`目录下面的`content_evaluation_agent.yml`模版里的配置信息来对`Prompt`等进行修改

## 4. 运行AgentFight

### 方法一：在Dora-rs命令里运行：

1. 安装MoFA项目包
2. `dora up && dora build  agent_fight_dataflow.yml && dora start reasoner_dataflow.yml`
3. 启动另外一个命令端,在另外一个命令端运行 `multiple-terminal-input`.然后输入需要输入三个参数
   - **primary_data** : 第一个agent/llm的输出结果(可以传输一个markdown的文件路径,要求是绝对路径)
   - **second_data** : 第二个agent/llm的输出结果(可以传输一个markdown的文件路径,要求是绝对路径)
   - **source_task** : 生成agent结果的任务. 例如: "primary_data"和"second_data"都是通过同一个任务去生成的. 
 
