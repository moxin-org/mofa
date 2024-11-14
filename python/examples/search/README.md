
# Web Search 项目

## 1. 功能说明

**Web Search** 项目旨在通过自动化的方式，从不同类型的网页中提取和处理数据。该项目支持针对各种网页页面类型（例如包含搜索框的网页）生成多个 **connector**（连接器），用于与网页进行交互。同时，项目中包含多个 **extractor**（提取器），专门用于从网页中提取所需的信息.


## 2. 设计方式


- **多类型网页的自动化交互**：生成针对不同网页类型的connector，实现自动化操作。
- **批量搜索和查询执行**：使用预先配置的多个connector，自动执行各种搜索和查询。
- **多样化的数据提取**：利用多个extractor，从不同网页中提取所需的数据和信息。

## 3. 配置方法

项目包含两个主要的流程：

- **Web Connector Configuration**：通过检测网页中的搜索表单，生成适用于不同网页类型的connector配置。
- **Web Search Box Extractor**：通过加载保存的不同connector，执行搜索查询并使用相应的extractor提取结果。

以下是详细的配置步骤和说明。（图为Web Search项目的Dora Data Flow）
![memaid_process.png](memaid_process.png)

### 配置说明

配置文件位于`configs`目录下，`.py`文件为实际运行的Agent代码。配置文件指定了各个Agent的行为、参数和逻辑。

#### 配置文件

- **Connector相关配置**：

  | **文件**                                 | **作用**                                                         |
  | ---------------------------------------- | ---------------------------------------------------------------- |
  | `configs/load_url_connector_agent.yml`       | 配置加载网页URL的Agent，定义如何从用户输入中获取URL并加载内容。     |
  | `configs/discovery_search_box_agent.yml`     | 配置检测网页搜索表单的Agent，提取form的action URL和输入字段。       |
  | `configs/search_box_connector_agent.yml`     | 配置搜索框connector的Agent，加载保存的connector配置。             |

- **Extractor相关配置**：

  | **文件**                                 | **作用**                                                         |
  | ---------------------------------------- | ---------------------------------------------------------------- |
  | `configs/search_box_extractor_agent.yml`     | 配置执行搜索查询的Agent，发送查询关键字到搜索引擎并获取结果。       |

#### 脚本文件

- **Connector相关脚本**：

  | **文件**                              | **作用**                                                         |
  | ------------------------------------- | ---------------------------------------------------------------- |
  | `scripts/load_url_connector_agent.py`      | 实际执行加载网页URL操作，根据用户输入的URL加载网页内容。          |
  | `scripts/discovery_search_box_agent.py`    | 实际执行搜索表单检测，提取form元素信息并生成connector配置。       |
  | `scripts/search_box_connector_agent.py`    | 实际加载保存的connector配置，为查询做好准备。                    |

- **Extractor相关脚本**：

  | **文件**                              | **作用**                                                         |
  | ------------------------------------- | ---------------------------------------------------------------- |
  | `scripts/search_box_extractor_agent.py`    | 实际执行查询操作，将查询关键字发送到搜索引擎并提取结果。          |

### 配置步骤

1. **环境配置**

   - 确保已安装必要的Python包和依赖项。
   - 确保已安装Dora框架和相关工具。

2. **检测网页并生成多个Connector配置**

   - 运行`web_connector_configuration_dataflow.yml`流程：
     ```bash
     dora up
     dora build web_connector_configuration_dataflow.yml
     dora start web_connector_configuration_dataflow.yml --attach
     ```
   - 在终端中，`terminal-input`会提示输入，需要输入想要配置的网页URL，例如：https://www.example.com。
   - 系统将自动加载URL，检测搜索表单，生成并保存针对该网页的connector配置。

3. **执行搜索查询并提取数据**

   - 运行`web_search_box_extractor_dataflow.yml`流程：
     ```bash
     dora build web_search_box_extractor_dataflow.yml
     dora start web_search_box_extractor_dataflow.yml --attach
     ```
   - 在终端中，`terminal-input`会提示输入查询关键字，例如：人工智能。
   - 系统将使用之前保存的对应connector，发送查询关键字到网页的搜索引擎，并使用相应的extractor获取并提取搜索结果。

4. **注意事项**

   - **自定义和扩展**：可以根据需要添加新的connector和extractor，以支持更多类型的网页和数据提取需求。
   - **配置文件管理**：确保`configs`目录下的配置文件正确无误，可以根据需求调整参数。
   - **脚本文件修改**：脚本文件位于`scripts`目录下，可以根据需要进行定制和优化。
   - **环境依赖**：确保运行环境中已安装所有必要的依赖项，包括Python库和外部工具。
   - **API和权限**：如果需要访问特定的API或受限内容，请确保已获得必要的权限和API密钥。

---

# 模块说明

该项目通过灵活的connector和extractor设计，实现了对不同网页类型的通用支持。通过添加和配置不同的connector，可以适配各种网页的搜索框和交互方式；通过设计多种extractor，可以满足不同的数据提取需求。

此架构的优势在于：

- **模块化设计**：connector和extractor彼此独立，便于维护和扩展。
- **高可扩展性**：可以轻松添加新的网页支持，只需编写相应的connector和extractor。
- **自动化流程**：从网页检测、配置生成到查询执行和数据提取，全部流程自动化，提高效率。

---

# 常见问题解答

**Q1：如何添加新的网页支持？**

A1：您可以编写新的connector和extractor配置和脚本，放置在`configs`和`scripts`目录下。然后，更新相应的dataflow配置文件以包含新的Agent。

**Q2：是否可以定制数据提取的方式？**

A2：是的，您可以修改或编写新的extractor脚本，以适应特定的数据提取需求。

**Q3：运行过程中遇到错误怎么办？**

A3：请检查配置文件和脚本是否正确，确保依赖项已安装，并查看终端输出的错误信息以定位问题。

---





