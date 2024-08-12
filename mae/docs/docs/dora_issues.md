#  当我使用 dora 框架时，我遇到了哪些问题？


## Q: 在使用cmd命令运行的时候,我应该如何获取到这个dora-dataflow中node生成的日志信息?
**A:** : 

## Q: 一个dataflow的流程中,是否支持多个dynamic节点输入?
**A:** : 

## Q: 如何将当前的Agent-Dataflow接入到Node-Hub中?
**A:** : 

## Q: 使用dynamic作为输入节点时,似乎dynamic节点不关闭,不能正常发送以及接受不数据?
**A:** :


关于dynamic节点,我们现在有以下的问题:

1. 我们想让`dynamic-node`获取某一个节点的输出,之后使用`python dynamic.py`，然后在`terminal`中将接收到的数据展示出来
2. 当我们有多个`dataflow`流程的时候,当每个流程的`dynamic`节点的名称是一致的,为什么不能启动同一个`dynamic`节点向多个`dataflow`流程发送信息呢? 

