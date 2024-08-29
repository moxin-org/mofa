# 构建一个标准的agent template 的规范

# 1，Dora Dataflow 的Yml构建规范
- 创建Agent的Dataflow的流程的时候，请你尽可能的模仿`reasoner_dataflow.yml`的流程以及`web_search_dataflow.yml`的流程
- Dataflow的流程中,第一个流程应该保证的是一个`dynamic`的输入,并且这个node的名称以及对应的`py`文件的名称也必须包含`task_input`这个字段
- Dataflow的流程中,最后一个流程应该保证的是一个`output`的输出,并且这个node的名称以及对应的`py`文件的名称也必须包含`output`这个字段
- 除了第一个和最后一个流程,其他流程中都应该带有`agent`这个名称的后缀
- 每一个`agent-node`的输出,应该包含自己agent的每一个输出.例如，你的agent输出了4个内容,那么你就应该输出这4个内容.并且加上一个总输出
- 最后一个output的输出应该输出之前所有agent的输出以及一个所有汇总的输出

# 2，Dora Dataflow 的Python构建规
- 文件的名称要和`Dataflow`的中的node名称相同
- 每一个`node`都应该输出一个`agent`输出的所有的值
- 所有的`node`,都应该是`agent`名称 加上 `dataflow`的名称


