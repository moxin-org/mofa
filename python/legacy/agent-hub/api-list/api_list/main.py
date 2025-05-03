import re
import pandas as pd
from pathlib import Path
from typing import Dict, List


def parse_readme(readme_path: str) -> Dict[str, List[str]]:
    """
    解析README文件并提取关键信息
    返回包含标题、段落、代码块和链接的字典
    """
    content = Path(readme_path).read_text(encoding='utf-8')

    # 提取标题（Markdown格式）
    headers = re.findall(r'^#+\s*(.+)$', content, flags=re.MULTILINE)

    # 提取段落（非空行）
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', content) if p.strip()]

    # 提取代码块（三个反引号包围的内容）
    code_blocks = re.findall(r'```(?:.*?)\n(.*?)```', content, flags=re.DOTALL)

    # 提取所有链接（Markdown格式和HTML格式）
    links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)|href=["\']([^"\']+)["\']', content)
    formatted_links = []
    for link in links:
        if link[0]:  # Markdown链接
            formatted_links.append({'text': link[0], 'url': link[1]})
        elif link[2]:  # HTML链接
            formatted_links.append({'text': '', 'url': link[2]})

    # 初始化tables列表
    tables = []
    # 增强表格解析，支持复杂结构和HTML内容
    table_pattern = r'(?s)\|(.+?)\|[\s\S]+?\|[-:]+?\|[\s\S]+?((?:\|.+?\|)+)'
    for match in re.finditer(table_pattern, content):
        try:
            # 提取表头
            headers = [h.strip() for h in match.group(1).split('|') if h.strip()]
            
            # 提取表格内容行
            rows = []
            for row in match.group(2).split('\n'):
                if '|' in row:
                    # 清理HTML标签和多余空格
                    clean_row = re.sub(r'<[^>]+>', '', row).strip()
                    cells = [c.strip() for c in clean_row.split('|') if c.strip()]
                    if len(cells) == len(headers):
                        row_data = dict(zip(headers, cells))
                        
                        # 特殊处理包含Postman按钮的列
                        if 'Call this API' in row_data:
                            postman_link = re.search(r'href="([^"]+)"', row)
                            if postman_link:
                                row_data['postman_collection'] = postman_link.group(1)
                        
                        rows.append(row_data)
            
            if rows:
                tables.append(pd.DataFrame(rows))
                
        except Exception as e:
            print(f"表格解析错误: {str(e)}")
            continue

    return {
        'headers': headers,
        'paragraphs': paragraphs,
        'code_blocks': code_blocks,
        'links': formatted_links,
        'tables': tables
    }


def categorize_url(url: str) -> str:
    """根据URL路径特征分类API类型"""
    try:
        url = url.lower()
        if any(p in url for p in ['/pay/', '/transaction/', '/billing/']):
            return '支付'
        if any(s in url for s in ['/social/', '/wechat/', '/weibo/']):
            return '社交'
        if any(m in url for m in ['/map/', '/geocode/', '/route/']):
            return '地图'
        if any(a in url for a in ['/ai/', '/ml/', '/nlp/']):
            return '人工智能'
        if any(d in url for d in ['/data/', '/dataset/', '/storage/']):
            return '数据服务'
        return '其他'
    except AttributeError:
        return '未知'

def has_auth_requirement(url: str) -> bool:
    """通过URL参数判断是否需要认证"""
    try:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        return any(key in params for key in ['key', 'token', 'secret']) \
            or 'auth' in parsed.path
    except:
        return False

def url_to_name(url: str) -> str:
    """从URL路径生成默认名称"""
    try:
        # 获取最后一段有意义的路径
        clean_path = re.sub(r'\W+', '', url.split('/')[-1])
        return clean_path.capitalize() if clean_path else 'UnnamedAPI'
    except:
        return 'UnnamedAPI'

def extract_api_info(parsed_data: dict) -> pd.DataFrame:
    """从解析结果中提取API信息"""
    api_data = []

    # 从表格中提取（适配新的表格格式）
    for table in parsed_data['tables']:
        # 统一处理不同表格结构
        for record in table.to_dict('records'):
            # 处理API信息表格
            normalized = {
                'name': record.get('API') or record.get('Service') or url_to_name(record.get('URL', '')),
                'url': record.get('URL') or record.get('Endpoint') or '',
                'description': record.get('Description') or record.get('功能') or '',
                'auth_required': any(keyword in str(record.get('Auth', '')).lower() 
                                   for keyword in ['apiKey', 'key', 'token', 'secret']),
                'category': categorize_url(record.get('Category') or 
                                         record.get('URL') or 
                                         record.get('Endpoint') or '')
            }
            
            # 处理特殊列（包含Postman按钮的列）
            if 'Call this API' in record:
                postman_link = re.search(r'href="([^"]+)"', str(record['Call this API']))
                if postman_link:
                    normalized['postman_collection'] = postman_link.group(1)
            
            api_data.append(normalized)

    # 从代码块中提取
    for code in parsed_data['code_blocks']:
        # 匹配带参数的API端点
        for url in re.findall(r'(https?://[^\s/$.?#]+\.[^\s)\'"]+)', code):
            api_data.append({
                'name': re.sub(r'\W+', '', url.split('/')[-1]).capitalize(),
                'url': url,
                'description': '从代码块中提取的API端点',
                'auth_required': 'api_key' in url or 'token' in url,
                'category': categorize_url(url)
            })

    # 从链接中提取
    for link in parsed_data['links']:
        if 'api' in link['url'].lower():
            api_data.append({
                'name': link['text'] or url_to_name(link['url']),
                'url': link['url'],
                'description': '从文档链接中提取的API',
                'auth_required': has_auth_requirement(link['url']),
                'category': categorize_url(link['url'])
            })

    return pd.DataFrame(api_data).drop_duplicates()


if __name__ == "__main__":
    # 指定具体README文件路径
    readme_path = Path(__file__).parent.parent / "api_list/API-LIST-README.md"
    print(f"正在读取文件: {readme_path.absolute()}")
    
    if not readme_path.exists():
        print(f"错误：文件 {readme_path} 不存在")
        print("请确认以下情况：")
        print("1. 文件是否位于python/agent-hub/api-list目录")
        print("2. 文件名是否确认为API-LIST-README.md")
        print("3. 文件内容是否包含API表格（Markdown格式）")
        import sys
        sys.exit(1)

    try:
        parsed = parse_readme(str(readme_path))
        print(f"成功解析文件，找到 {len(parsed['tables'])} 个数据表")
    except Exception as e:
        print(f"解析文件失败: {str(e)}")
        print("调试信息：")
        print(f"- 文件大小: {readme_path.stat().st_size} 字节")
        print(f"- 文件内容开头: {readme_path.read_text(encoding='utf-8')[:200]}...")
        import sys
        sys.exit(1)

    print("提取到的标题：")
    print("\n".join(parsed['headers'][:3]) + "...")

    print("\n提取到的API信息：")
    api_df = extract_api_info(parsed)

    # 数据清洗与校验
    try:
        if not api_df.empty and 'url' in api_df.columns:
            api_df = api_df[~api_df['url'].str.contains('example.com|localhost', na=False)]
        else:
            print("警告：未提取到有效的API数据")
            api_df = pd.DataFrame(columns=['name', 'url', 'description', 'auth_required', 'category'])

        # 确保必要字段存在
        required_columns = ['name', 'url', 'category', 'auth_required', 'description']
        for col in required_columns:
            if col not in api_df.columns:
                api_df[col] = '未知' if col != 'auth_required' else False

        # 显示结果
        if not api_df.empty:
            print("成功提取的API列表：")
            print(api_df[['name', 'url', 'category', 'auth_required']].head().to_string(index=False))
        else:
            print("没有符合条件的数据需要展示")
    except Exception as e:
        print(f"数据处理过程中发生错误: {str(e)}")

    # 保存结果
    api_df.to_csv('extracted_apis.csv', index=False)
    print("\n结果已保存到 extracted_apis.csv")
