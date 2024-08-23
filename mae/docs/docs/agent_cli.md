# 1, 安装mae项目
查看[install_mae](install_mae.md)文档 安装mae项目

# 2，对Agent进行参数配置
在 `Moxin-App-Engine/mae/agent-applications` 这个目录下 就是我们所有的当前可用的agents,我们正在陆续增加
你需要对配置里面的configs下面的yml文件进行配置
尤其是 Api方面，当然你也可以配置成为Ollama模型
**Openai**：
~~~
MODEL:
  MODEL_API_KEY:  
  MODEL_NAME: gpt-4o-mini
  MODEL_MAX_TOKENS: 2048
~~~
**Ollama**:
~~~
MODEL:
  MODEL_API_KEY: ollama
  MODEL_NAME: qwen:14b
  MODEL_MAX_TOKENS: 2048
  MODEL_API_URL: http://192.168.0.1:11434
~~~

# 3, 在命令端启用Agent

## 3.1 不同cmd命令

**获取当前可用Agent**:
~~~ /shell
mae agent-list
~~~ 

**运行Agent**:
~~~ /shell
mae run --agent-name reasoner
~~~
**如何关闭呢**? 
在命令端输入exit/quit即可关闭



## Q: 如果遇到Dora卡死的情况怎么办? 
**A:** :  建议在sudo命令下面使用 
~~~
pkill dora 
~~~
注意 它会删除所有的关于dora的进程 请谨慎使用



