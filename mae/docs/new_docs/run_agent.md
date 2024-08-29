# 1, 如何运行Dora-Dataflow
首先你需要创建两个`Terminal`,并且在`Terminal`中分别运行以下命令:

## 1.1 首先激活你的环境
如果你使用的是conda环境,那么使用以下命令激活

~~~/shell
conda activate mae_env  
~~~
其中`mae_env`是你的conda环境名


### 1.2 删除旧的日志信息
删除旧的日志信息,防止日志信息混乱
请你在`/Moxin-App-Engine/mae/examples/agents/super_agent/web_search/data/output/log/mae_web_search.md`文件夹中找到这个文件，并且删除它
它将会在下一次dora-dataflow运行时重新生成

### 1.3 修改配置文件
你需要在`/Moxin-App-Engine/mae/examples/agents/super_agent/web_search/use_case`文件中修改配置文件
分别修改下面文件中的api配置参数
- more_question_agent.yml
- web_search_agent.yml


### 1.4 运行Dora-Dataflow
请你在两个`Terminal`中的一个运行以下命令:
- 首先 `cd /Moxin-App-Engine/mae/examples/agents/super_agent/web_search`
~~~
dora start web_search.yml --attach
~~~
运行完毕之后程序会等待 `dynamic-node`的输入

### 1.5 运行Dynamic-node
请你在两个`Terminal`中的一个运行以下命令:
- 首先 `cd /Moxin-App-Engine/mae/examples/agents/super_agent/web_search`
~~~
python3 task_input.py
~~~
然后输入你的任务即可

## 1.6 查看运行结果
在当前目录下,找到 `/Moxin-App-Engine/mae/examples/agents/super_agent/web_search/data/output/log/mae_web_search.md`
使用`Typora`打开文件,查看运行结果即可




# 2, 关于Dora的问题

## Q: 在Dora-DataFlow中,从中间Node节点获取多个输出,以便在客户端网页上展示.

## Q: 在Dora-DataFlow中,从客户端网页上获取多个输入,提供给中间Node节点.

## Q: source1-flow和source2-flow拼接成target-flow.注意source1-flow可能有m个输出，source2-flow可能需要处理n个输入。

## Q: 在dora是否可能支持简单的逻辑判断和循环
例如:
Ansible 会在其 YAML 配置文件中提供条件判断的支持。
~~~
tasks:
  - name: Install packages on CentOS
    yum:
      name: httpd
      state: present
    when: ansible_os_family == "RedHat"

  - name: Install packages on Debian
    apt:
      name: apache2
      state: present
    when: ansible_os_family == "Debian"
~~~





