import requests
import yaml
import json

from mofa.utils.files.read import read_yaml


def analyze_openapi_spec_to_list_of_dicts(openapi_url):
    """
    分析 OpenAPI 规范文件，将每个 API 操作转换为一个字典，并收集到列表中。

    Args:
        openapi_url (str): OpenAPI YAML/JSON 文件的 URL。

    Returns:
        list: 包含每个 API 操作信息的字典列表。
    """
    try:
        response = requests.get(openapi_url)
        response.raise_for_status() # 检查 HTTP 错误

        # 尝试解析为 YAML，如果失败则尝试 JSON
        try:
            spec = yaml.safe_load(response.text)
        except yaml.YAMLError:
            spec = json.loads(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching OpenAPI spec: {e}")
        return []
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        print(f"Error parsing OpenAPI spec: {e}")
        return []

    # 最终存放所有 API 字典的列表
    api_operations_list = []

    # 遍历 OpenAPI 规范中的 'paths' 部分
    # 'paths' 包含了所有 API 的端点（例如 '/v1/auditevents'）
    for path, methods_details in spec.get('paths', {}).items():
        # 'methods_details' 是一个字典，包含了该路径下支持的 HTTP 方法 (GET, POST 等) 及其详细信息
        for method, operation_details in methods_details.items():
            # 确保我们处理的是实际的 HTTP 方法，而不是 OpenAPI 规范中的其他元数据
            if method.lower() not in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
                continue

            # **这就是您要的“每一个 API 变成一个 dict”**
            # 为当前遍历到的 HTTP 方法 (method) 在特定路径 (path) 下的操作，创建一个字典
            api_info_dict = {
                "api_name": operation_details.get('summary') or operation_details.get('operationId') or f"{method.upper()} {path}",
                "description": operation_details.get('description', 'No description provided.'),
                "request_method": method.upper(), # HTTP 请求方法 (GET, POST等)
                "path": path, # API 的路径
                "request_parameters": [], # 请求参数列表
                "response_parameters": [] # 响应参数列表
            }

            # --- 处理请求参数 ---
            if 'parameters' in operation_details:
                for param in operation_details['parameters']:
                    param_detail = {
                        "name": param.get('name'),
                        "in": param.get('in'),  # 例如 'query', 'header', 'path', 'cookie'
                        "description": param.get('description', ''),
                        "type": param.get('schema', {}).get('type'), # 参数类型 (string, integer等)
                        "required": param.get('required', False)
                    }
                    api_info_dict["request_parameters"].append(param_detail)

            # --- 处理请求体 (requestBody) ---
            # 如果 API 有请求体 (例如 POST 或 PUT 请求通常有)
            if 'requestBody' in operation_details:
                request_body_content = operation_details['requestBody'].get('content', {})
                for media_type, media_details in request_body_content.items():
                    schema = media_details.get('schema', {})
                    if '$ref' in schema:
                        # 如果是引用其他数据模型
                        ref_name = schema['$ref'].split('/')[-1]
                        api_info_dict["request_parameters"].append({
                            "name": "body",
                            "in": "body",
                            "description": f"Request body referencing {ref_name} schema.",
                            "type": "object",
                            "schema_reference": ref_name,
                            "required": operation_details['requestBody'].get('required', False)
                        })
                    else:
                        # 如果是内联定义的数据模型
                        api_info_dict["request_parameters"].append({
                            "name": "body",
                            "in": "body",
                            "description": media_details.get('description', 'Request body.'),
                            "type": schema.get('type'),
                            "properties": schema.get('properties'), # 如果是对象，可能包含属性定义
                            "required": operation_details['requestBody'].get('required', False)
                        })
                    # 通常一个请求体只取一个媒体类型（如 application/json）
                    break # 处理完第一个媒体类型就跳出

            # --- 处理响应参数 ---
            if 'responses' in operation_details:
                for status_code, response_details in operation_details['responses'].items():
                    # 仅处理成功的响应 (状态码以 '2' 开头)
                    if status_code.startswith('2'):
                        response_content = response_details.get('content', {})
                        for media_type, media_details in response_content.items():
                            schema = media_details.get('schema', {})
                            if '$ref' in schema:
                                # 如果是引用其他数据模型
                                ref_name = schema['$ref'].split('/')[-1]
                                api_info_dict["response_parameters"].append({
                                    "status_code": status_code,
                                    "media_type": media_type,
                                    "description": response_details.get('description', ''),
                                    "type": "object",
                                    "schema_reference": ref_name
                                })
                            else:
                                # 如果是内联定义的数据模型
                                api_info_dict["response_parameters"].append({
                                    "status_code": status_code,
                                    "media_type": media_type,
                                    "description": response_details.get('description', ''),
                                    "type": schema.get('type'),
                                    "properties": schema.get('properties') # 如果是对象，可能包含属性定义
                                })
                            # 找到一个成功响应的媒体类型就跳出
                            break
                        # 找到一个成功响应码（如 200）就跳出
                        break

            # 将填充好的当前 API 字典添加到总列表中
            api_operations_list.append(api_info_dict)

    return api_operations_list

# --- 使用示例 ---
# 1Password Events API 1.2.0 的 OpenAPI YAML 文件原始 URL
openapi_spec_url = "https://raw.githubusercontent.com/APIs-guru/openapi-directory/main/APIs/1password.com/events/1.2.0/openapi.yaml"

# 调用函数获取分析结果
analyzed_apis = analyze_openapi_spec_to_list_of_dicts(openapi_spec_url)

# 打印结果，使用 JSON 格式化输出，使其更易读
print(json.dumps(analyzed_apis, indent=2, ensure_ascii=False))
data = read_yaml('openapi.yaml')
print(data)

x1data = read_yaml('openapi.yaml')
all_apis = []
for api_path,api_info in x1data['paths'].items():
    all_apis.append({'api_path': api_path, 'api_path_info': api_info,'api_info':x1data['info']})
print(x1data)
# 您也可以将结果保存到文件
# with open('1password_events_api_list.json', 'w', encoding='utf-8') as f:
#     json.dump(analyzed_apis, f, indent=2, ensure_ascii=False)