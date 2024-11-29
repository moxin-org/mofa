# xiaowang_start

基于MoFA的多层次动态反思智能体-xiaowang

**语言**

python3.10+
rust

## 1. 功能说明

xiaowang是多层次动态反思智能体，运行时会动态决策反思层数并根据动态决策节点的反思层数进行相应深度的反思，相当于人类对大模型结果不满意时多次prompt以增加大模型输出的丰富性，准确性，可靠性。

## 2. 使用场景

任意大模型均可通过此方法增加思考深度以提高结果的可靠性。


## 3. 配置方法

更改xiaowang_start/configs里的多个.yml配置信息来微调和定制每个节点的提示词，API，密钥等。

## 4. 运行xiaowang

1. 安装MoFA项目包,安装相关依赖
2. `dora up && dora build xiaowang_dataflow.yml && dora start xiaowang_dataflow.yml`
3. 3. 启动另外一个命令端,在另外一个命令端运行 `xiaowang`.然后输入任务即可


