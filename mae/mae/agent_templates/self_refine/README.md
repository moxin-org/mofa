# Reasoner Template  


**语言**
- [English](README.md)

# 1,功能说明
主要是根据用户的问题，使用llm生成答案。然后再让llm评估问题的结果，并且给出建议,根据建议再次生成答案，最后将答案再次给到llm，让llm评估他是否符合问题以及建议.符合则输出，否则继续虚幻

# 2，使用方法
1. 安装mae项目包
2. 在命令端 cd 到当前目录下
3. 在`configs\reasoner_agent.yml`中修改prompt以llm的key
4. `dora up && dora start self_refine_dataflow.yml`

# 3，存在的问题
1. 代码实现过程比较乱,需要优化
2. 没有添加一个`terminal-input`作为输入.是不合适的
3. 一些agent中没有做到可以接收多个输入

