
## 1, 向量数据库
我们的Rag的Vector数据库使用的是Postgres-Vector,我们本地必须运行一个Vector数据库(基于Docker运行)
```sh
docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16
```
- 如果你没有docker,那么可以使用我们公共测试的Pg-Vector账号密码. (注意,此账号密码可能因为安全原因被销毁,连接前请尝试去连接此数据库,确定此数据库可用)
```sh
postgresql+psycopg://mofa:MLbDGKC7d7IPBN@124.156.214.116:6024/mae_db
```
- Rag当前只支持`Txt`和`Pdf`文件格式
