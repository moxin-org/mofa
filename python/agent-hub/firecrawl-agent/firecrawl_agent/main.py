import os

from dotenv import load_dotenv
from firecrawl.firecrawl import FirecrawlApp

from mofa.agent_build.base.base_agent import MofaAgent, run_agent

@run_agent
def run(agent:MofaAgent):
    url = agent.receive_parameter('url')
    load_dotenv('/.env.secret')
    app = FirecrawlApp(api_key=os.getenv('FC_API_KEY'))
    # Scrape a website:
    scrape_result = app.scrape_url(
        url,
        params={'formats': ['markdown', 'html']}
    )
    agent.send_output(agent_output_name='firecrawl_agent_result',agent_result=scrape_result)
def main():
    agent = MofaAgent(agent_name='firecrawl-agent')
    run(agent=agent)
if __name__ == "__main__":
    main()



