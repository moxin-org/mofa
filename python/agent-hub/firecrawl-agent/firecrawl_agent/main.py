import json
import os

from dotenv import load_dotenv
from firecrawl.firecrawl import FirecrawlApp

from mofa.agent_build.base.base_agent import MofaAgent, run_agent

class FireCrawl:
    def __init__(self, api_key: str = None, env_file: str = '.env.secret', crawl_params: dict = None):
        if api_key is None:
            load_dotenv(env_file)
            api_key = os.getenv("FIRECRAWL_API_KEY")
        self.crawl = FirecrawlApp(api_key=api_key)
        if crawl_params is None:
            crawl_params = {
                "maxDepth": os.getenv('FIRECRAWL_MAXDEPTH',3),
                "timeLimit": 180,  # Time limit in seconds
                "maxUrls": os.getenv('FIRECRAWL_MAXUrls',15)  # Maximum URLs to analyze
            }
        self.crawl_params = crawl_params

    def on_activity(self, activity):
        print(f"[{activity['type']}] {activity['message']}")

    def deep_research(self, query: str, ):
        analysis_prompt = """
Development History: The speaker's growth path in the industry, major accomplishments, and technological breakthroughs.

Personal Story: The speaker's background, career transitions, and challenges faced along the way, as well as how they overcame them.

Educational Background: The speaker's education history, including undergraduate, master’s, and doctoral degrees, along with the universities attended.

Patents: Whether the speaker holds any technological patents, and the number and scope of those patents.

Personal Information: Basic details about the speaker, including life experiences that highlight their personal characteristics.

Social Media and Open Source Contributions: The speaker’s activity on social media platforms and contributions to open-source projects (e.g., GitHub).

Professional Experience: The speaker’s work history, including companies they’ve worked for, roles held, and key project experiences."""
        results = self.crawl.deep_research(query=query,
                                           max_depth=os.getenv('FIRECRAWL_MAXDEPTH',3),max_urls=os.getenv('FIRECRAWL_MAXURLS',10), on_activity=self.on_activity,analysis_prompt=analysis_prompt)
        source_data = results['data']['sources']
        analysis_data = results['data']['finalAnalysis']
        return source_data, analysis_data

@run_agent
def run(agent:MofaAgent):
    query = agent.receive_parameter('query')
    app = FireCrawl()
    # Scrape a website:
    scrape_result = json.dumps(app.deep_research(query=query))
    agent.send_output(agent_output_name='firecrawl_agent_result',agent_result=scrape_result)
def main():
    agent = MofaAgent(agent_name='firecrawl-agent')
    run(agent=agent)
if __name__ == "__main__":
    main()



