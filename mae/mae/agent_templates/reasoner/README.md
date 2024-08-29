# Reasoner Template  


**语言**
- [English](README.md)

# 1,功能说明
主要是根据用户的问题，使用大模型生成答案。

# 2，使用方法
1. 安装mae项目包
2. 在命令端 cd 到当前目录下
3. 在`configs\reasoner_agent.yml`中修改prompt以llm的key
4. `dora up && dora build  reasoner_dataflow.yml && dora start reasoner_dataflow.yml`
5. 在另外一个命令端运行 `terminal-input`
