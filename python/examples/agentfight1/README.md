# Agent Fight 案例

**语言**: 中文

## 1. 功能说明

Agent Fight智能体通过从用户任务的输入，交予两个不同大模型的agent回答任务问题，judge agent同时根据用户输入的任务生成评价标准，并对两个answer agent的回来做出评分与评价。
其设计模式为：**任务提取 + 任务回答 + 生成评分标准 + 结果评价**。

**流程说明：**

answer_agent_1 ：接收任务关键词，围绕task做出简要回答。

answer_agent_2 ：接收任务关键词，围绕task做出简要回答。

judge_agent ：生成评价标准，接收answer1和2的结果，进行评价后反馈至终端。


## 2. 配置方法

### 配置说明

配置文件位于`configs`目录下，`.py`文件为实际运行的智能体代码。配置文件指定了各个Agent的行为、参数和模型提示等。

### 配置步骤


#### 3. 修改配置

根据具体需求，编辑`configs`目录下的`.yml`配置文件。
可以自定义修改里面的模型参数，建议不要修改以及提示词。


## 4. 运行智能体

使用Dora-rs命令行运行

1. 安装MoFA项目包。
2. 执行以下命令以启动智能体流程：
   ```bash
   dora up && dora build fight_dataflow.yml && dora start fight_dataflow.yml --attach
   ```
3. 启动另一个终端，运行`terminal-input`，然后输入相应任务以启动Agent Fight流程。

                                                                                                                                                 
bug:
1.首次输入task后，judge agent 无法正确给出评分与评价。但后续的输入task后，judge正常 （暂时归结为LLM的自身问题，考虑更换更好的LLM）
2.terminal中输出answer1的回答，无法输出judge的评价与answer2的答案 （已解决）