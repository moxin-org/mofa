


# Dora Server Q&A

## Q: Can Front-end start the Dora Process? (前端可以启动 Dora 进程吗？)
**A:** : 不可以，前端只能调用后端的Api接口,Dora的流程由Api接口调用


## Q: Can Front-end work at a different machine?(前端可以在不同的机器上工作吗？)
**A:** : 前后端都可以在不同的机器上面单独启动，由于前端需要知道后端的Ip地址，所以后端最好放到一个有公网IP的机器上面启动。

## Q: Can a middle Dora node request and receive input from the front end? (中间的 Dora 节点可以请求并接收来自前端的输入吗？)
**A:** : 由于Dora流程启动的过程中,前端无法访问流程中的Node的节点的输出,所以可能依赖于其他的方案来访问流程中的输出

当前有三个方案
1. 当前端点击启动之后，后端返回一个流程的id，然后流程运行过程中,前端带着这个id去访问一个api，这个api会读取流程输出的日志，以达到我们要求获取流程过程中输出结果的方法
2. 每个Node运行之后将结果发送到一个消息队列中,然后前端通过订阅这个消息队列来获取结果
3. 前端Node启动一个服务,然后当我的每个Node运行完毕之后,就将数据发送到服务中，服务根据发送过来的数据在页面上展示

## Q: Can a node fire up a new webpage in the front-end browser? (节点可以在前端浏览器中启动一个新网页吗？)
**A:** :

## Q: What is the protocol between FrontEnd and BackEnd to ensure a simple, easy, and flexible interface? (前端和后端之间的协议是什么，以确保接口简单、易用和灵活？)
**A:**  : 
1. 协议使用HTTP协议，前端通过http请求后端的api接口.
2. 接口请求与返回: 采用统一的JSON格式进行数据交换，定义标准的响应结构（如包含状态码、消息、数据等字段）。
3. 使用Swagger工具生成API文档，确保前后端开发人员都能清晰了解接口定义和使用方法。

## Q: Can a Dora-Flow end when the frontend ends or give instruction to end the Dora-flow?  (当前端结束时，Dora 流程可以结束或指示结束 Dora 流程吗？)
**A:** : 可以做一个api接口，前端调用这个接口，后端收到这个请求之后，通过 `Dora stop` 强制结束这个流程 
