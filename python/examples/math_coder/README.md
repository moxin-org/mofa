# Math Coder 案例

**语言**: 中文

## 1. 功能说明

Math Coder智能体通过从用户任务的输入，交予reasoner-agent进行分析，并生成代码执行输出数学相关问题的答案。
其设计模式为：**代码生成+代码执行**。

**流程说明：**

reasoner-agent ：接收任务关键词，围绕task做出简要回答。


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
   dora up && dora build reasoner_dataflow.yml && dora start reasoner_dataflow.yml --attach
   ```
3. 启动另一个终端，运行`terminal-input`，然后输入相应任务以启动Agent Fight流程。

                                                                                                                                                