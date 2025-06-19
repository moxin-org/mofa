

## 智能生成Agent方案

### 1. 主要 API 数据源

#### （1）APIs.guru OpenAPI Directory
- **简介**：全球最大的开放 API 目录，收录了数千个公开 API 的 OpenAPI 规范。
- **获取方式**：直接克隆 [APIs.guru GitHub 仓库](https://github.com/APIs-guru/openapi-directory)。
- **内容特点**：每个 API 都有标准化的 OpenAPI/Swagger 文件，包含接口路径、请求方法、参数、响应、认证方式等详细信息。
- **使用方法**：直接clone项目,然后读取文件中的apis中的api内容,给到生成agent的流程即可


#### （2）public-apis（GitHub 开源项目）
- **简介**：收录了数百个免费、公开 API，按类别分类，附有简要描述和文档链接。
- **获取方式**：访问 [public-apis GitHub 仓库](https://github.com/public-apis/public-apis)。
- **使用方法**：clone项目之后,通过爬虫爬取内容,然后根据爬取的内容通过llm去处理,处理之后给到llm进行api的prompt生成。保存结果后给到Agent生成的流即可

#### （3）FreePublicAPIs.com
- **简介**：FreePublicAPIs.com 收录了 400+ 个免费、公开的 API，涵盖各类开发和学习场景，并且每天自动测试，保证可用性。
- **获取方式**：直接访问 FreePublicAPIs 官网 或使用其官方 API。
- **内容特点**：提供 RESTful API，可直接获取所有 API 的详细信息，支持分页、分类、随机获取等功能。
    - 每个 API 包含名称、描述、文档链接、认证方式、类别等详细字段。

- **使用方法**: 爬虫爬取这个网页内容，根据不同的url网址,获取对应的api内容。然后llm生成api-prompt就可以了

## 二、Agent优化方案

### 1. README.md优化
在agent_dependency_generator中,存在README.md写出不好以及不标准的问题,我们需要重新构建这个prompt. 可以参考 `https://github.com/dora-rs/dora/tree/main/node-hub/dora-cotracker`.需要根据这个文档内容,生成一个node模版



