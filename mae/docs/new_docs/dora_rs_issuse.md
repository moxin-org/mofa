与Dora团队的合作解决的一些问题以及解决方案：

# 1，解决的问题

## 1.1 Dora-dataflow中存在多个Dynamic-node

`https://github.com/dora-rs/dora/issues/616?notification_referrer_id=NT_kwDOAWHpcbQxMTg1NzM5MTkzMToyMzE5Mzk2OQ#issuecomment-2277280459`

## 1.2 在terminal展示llm的结果
`https://github.com/dora-rs/dora/issues/618`


# 2. 未解决的问题
在程序中，使用`subprocess`的模块，不能获得对应的`dora-process`中的日志输出,因为在`terminal`中是没有返回当前运行的`dora-process`的日志输出日志的id的。
