# Planning Agent in MoFA

## 1. 功能
Planning Agent 能够将复杂的大任务分解成小任务，并标注任务间的依赖关系以及执行方式（同步或异步）。

## 2. 用例
1. 输入一个大型任务，获取拆解后的小任务列表。
2. 获得结构化的任务信息，包括任务描述、依赖关系和执行类型。

## 3. 输出格式
代理返回的任务采用以下 JSON 结构：
```json
{
"tasks": [
{
"task_id": "1",
"description": "安装必要的开发工具（如IDE、编译器）",
"classification": "synchronous",
"is_synchronous": true,
"dependencies": []
},
// ... 更多任务 ...
]
}
```

## 4. 运行
1. 安装MoFA项目包
2. `dora up && dora build planning_agent.yml && dora start planning_agent.yml`
3. 启动另外一个命令端,在另外一个命令端运行 terminal-input.然后提问你要分解的任务。
4. 运行结果有两种：
   - 默认是用户易读的输出，会直接输出在终端中。
   - 还有一种是json格式，它可以作为下一个节点的输入，方便进行其他处理，你可以修改`scripts/planning_agent.py`文件中函数，已经写好了注释。

## 参考资料
-[agentic_patterns](https://github.com/neural-maze/agentic_patterns)