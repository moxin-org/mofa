# Crawl and Analysis Agent in MoFA

## 1. 功能
MoFA Crawl and Analysis Agent 能够从互联网上抓取数据，并进行分析，配置记忆功能。

## 2. 用例
1. 指定一个 url，结合该 url 的内容对大模型进行提问
2. 指定一个 url，生成爬网页的脚本代码
3. 对大模型进行提问，抓取搜索引擎的相关网页进行分析并使用大模型给出最终答案
## 3. 配置方法

## 4. 运行
1. 安装MoFA项目包
2. dora up && dora build  crawl_analysis_dataflow.yml && dora start crawl_analysis_dataflow.yml
3. 启动另外一个命令端,在另外一个命令端运行 multiple-terminal-input.然后提示词

## 参考资料
-[scrapegraph-ai](https://scrapegraph-ai.readthedocs.io/en/latest/index.html)