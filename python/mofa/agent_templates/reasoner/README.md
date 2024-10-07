# Basic Reasoner Template  

MoFA中最基本的智能体设计模式的实现

**语言**


## 1. 功能说明

Reasoner可以说是最简单的智能体。它的设计模式是：定制的大语言模型提示 + 大语言模型推理。

## 2. 使用场景

在智能体想定制大语言模型的提示时使用。
比如：

- 做一个以“爱因斯坦”的口吻和用户聊天的智能体。
- 做一个将一个问题分成五个小问题的智能体


## 3. 配置方法

基本的配置原理就是通过更改Reasoner模版里的配置信息来生成一个定制的智能体。

### 方法一：使用文本编辑器编辑MoFA配置文件

1. 模版拷贝：将包含这个智能体模版（Reasoner）的子目录拷贝到您指定的目录（比如hello_world)。 在目录里有两个目录，共三个文件

   | 文件                         | 说明                                                         |
   | ---------------------------- | ------------------------------------------------------------ |
   | `reasoner_dataflow.yml`      | Dora数据流配置文件                                           |
   | `configs\reasoner_agent.yml` | MoFA配置文件，包括大语言模型相关参数配置和定制提示参数配置等。 |
   | `scripts\reasoner_agent.py`  | 智能体所要完成的功能的Python Operator工具                    |

2. 智能体命名：可以将您的智能体重新命名。比如，如果您希望自己的Agent的名字为Hello World，您可以做如下重新的命名：

   | 文件                         | 说明                            |
   | ---------------------------- | ------------------------------- |
   | `reasoner_dataflow.yml`      | `hello_world_dataflow.yml`      |
   | `configs\reasoner_agent.yml` | `configs\hello_world_agent.yml` |
   | `scripts\reasoner_agent.py`  | 无需改名                        |

   

3. 修改配置

   

   | 文件                            | 说明                                                         |
   | ------------------------------- | ------------------------------------------------------------ |
   | `hello_world_dataflow.yml`      | 根据当前目录，需要更改`build: pip install -e ../../../node-hub/terminal-input`的路径(可以在mofa/node-hub/terminal-input中找到. 可以填写绝对路径) |
   | `configs\hello_world_agent.yml` | 根据定制要求，改写定制Prompts和大语言模型参数等. 包括Rag              |
   | `scripts\reasoner_agent.py`     | 修改`reasoner_agent.py`文件中`yaml_file_path`变量对应的configs的`yml`文件路径                                                     |

   

### 方法二：(待定)

## 4. 运行Agent

### 方法一：在Dora-rs命令里运行：

1. 安装MoFA项目包
2. `dora up && dora build  reasoner_dataflow.yml && dora start reasoner_dataflow.yml`
3. 启动另外一个命令端,在另外一个命令端运行 `terminal-input`.然后输入任务即可


### 方法二：（待定）
