from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, Any, Optional

@run_agent
def run(agent: MofaAgent):
    """
    QuoteAnalyzer Agent for interacting with the Quotable API.
    Supports fetching random quotes, searching quotes by keyword, and retrieving author details.
    """
    try:
        # Input handling
        action = agent.receive_parameter('action')
        
        if action == 'random_quote':
            # Fetch a random quote
            url = "https://api.quotable.io/quotes/random"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                quote = f'"{data[0]["content"]}" - {data[0]["author"]}'
                agent.send_output(
                    agent_output_name='quote_result',
                    agent_result=quote
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )
        
        elif action == 'search_quotes':
            # Search quotes by keyword
            keyword = agent.receive_parameter('keyword')
            url = "https://api.quotable.io/search/quotes"
            params = {"query": keyword, "fields": "content"}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                quotes = [quote['content'] for quote in data['results']]
                agent.send_output(
                    agent_output_name='search_results',
                    agent_result=quotes
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )
        
        elif action == 'author_details':
            # Get author details by slug
            slug = agent.receive_parameter('slug')
            url = f"https://api.quotable.io/authors/slug/{slug}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                agent.send_output(
                    agent_output_name='author_details',
                    agent_result=data
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )
        
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result=f"Invalid action: {action}. Valid actions are 'random_quote', 'search_quotes', 'author_details'."
            )
    
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An unexpected error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='QuoteAnalyzer')
    run(agent=agent)

if __name__ == '__main__':
    main()