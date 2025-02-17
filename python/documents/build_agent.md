1. 当我要创建agent的时候,需要确保你的agent的代码是能正常运行的
2. 在你的agent代码中,你需要按照你的配置，将他们分为密钥文件配置(存放所有密钥，如数据库密码/llm_api_key等)和yml文件配置(agent需要的文件)
3. 你的agent代码中的输入以及输出要注意，输入输出在mofa中默认都是字符串类型
4. 一般我们的核心代码都写在While True循环中，这样可以保证你的agent一直在运行.但是如果你的agent是在某些情况下，只需要实例化一次(例如agent会读取模型，那么模型不需要每次都加载，那么这些代码可以放到while true之前)


# tips:
1. dora中使用下面的方式去做的无限循环，这一块是否存在可以优化的地方? 导致我们的程序重复分配资源
```python 
for event in node:
    event_type = event["type"]
    if event_type == "INPUT":
        event_id = event["id"]
```
2. while True 能否去除掉
3. 是否用装饰器的方式解决改程序的问题
4. 大语言模型的加载能否使用一些统一的方法去做处理
5. 每一个Agent存在不同的环境依赖，有些agent之间的环境会有冲突，如果把这些agent分别放在dora的不同的node上，是否就解决了环境依赖冲突的问题
6. 启动dora-node这个process的进程是否可以根据不同环境的路径去启动不同的环境的dora-process
7. Dora如何部署在分布式的集群中? 不同的node可以运行在不同的机器节点上？ `https://github.com/dora-rs/dora/issues/535`