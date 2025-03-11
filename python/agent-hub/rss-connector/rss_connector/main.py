from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import feedparser
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs, unquote

def extract_real_url(redirect_url):
    """
    处理新浪跳转链接，提取真实新闻地址
    示例输入：http://go.rss.sina.com.cn/redirect.php?url=http%3A%2F%2Fnews.sina.com.cn%2Fc%2F2018-09-23%2Fdoc-ifxeuwwr7441548.shtml
    示例输出：http://news.sina.com.cn/c/2018-09-23/doc-ifxeuwwr7441548.shtml
    """
    try:
        # 解析URL参数
        parsed = urlparse(redirect_url)
        params = parse_qs(parsed.query)

        # 获取url参数值（可能包含多个值，取第一个）
        encoded_url = params.get('url', [''])[0]

        # URL解码处理
        decoded_url = unquote(encoded_url)

        # 处理多重编码情况（有些RSS可能多次编码）
        while '%' in decoded_url:
            prev_decoded = decoded_url
            decoded_url = unquote(decoded_url)
            if decoded_url == prev_decoded:
                break

        return decoded_url or redirect_url  # 失败时返回原链接

    except Exception as e:
        print(f"URL解析失败: {e}")
        return redirect_url  # 异常时返回原始链接

def parse_rss(rss_url):
    # 解析RSS源
    feed = feedparser.parse(rss_url)

    news_list = []

    for i, entry in enumerate(feed.entries, 1):
        # 构建新闻条目
        news_item = {
            "title": entry.get("title", ""),
            "summary": entry.get("description", ""),
            "url": extract_real_url(entry.get("link", "")),
            "time": entry.published
        }

        news_list.append(news_item)

    return json.dumps(news_list, ensure_ascii=False, indent=2)

@run_agent
def run(agent:MofaAgent):
    rss_url = agent.receive_parameter('rss_url')
    result_data = parse_rss(rss_url)
    agent_output_name = 'rss_content'
    agent.send_output(agent_output_name=agent_output_name,agent_result=result_data)


def main():
    agent = MofaAgent(agent_name='you-agent-name')
    run(agent=agent)
if __name__ == "__main__":
    main()
