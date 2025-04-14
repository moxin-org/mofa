from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        action = agent.receive_parameter('action')
        
        if action == 'random_cat':
            # API 1: Random Cat Image with JSON Metadata
            url = "https://cataas.com/cat?json=true"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "image_url": f"https://cataas.com{data['url']}",
                    "tags": data['tags']
                }
                agent.send_output('random_cat_result', result)
            else:
                agent.send_output('error', f"Request to {url} failed with status code: {response.status_code}")
        
        elif action == 'filter_cats':
            # API 2: Filter Cats by Tags
            tags = agent.receive_parameter('tags')
            url = f"https://cataas.com/api/cats?tags={tags}&limit=3"
            response = requests.get(url)
            
            if response.status_code == 200:
                cats = response.json()
                result = [{
                    "id": cat['_id'],
                    "tags": cat['tags']
                } for cat in cats]
                agent.send_output('filtered_cats_result', result)
            else:
                agent.send_output('error', f"Request to {url} failed with status code: {response.status_code}")
        
        elif action == 'get_tags':
            # API 3: Get All Tags
            url = "https://cataas.com/api/tags"
            response = requests.get(url)
            
            if response.status_code == 200:
                tags = response.json()
                agent.send_output('all_tags_result', tags)
            else:
                agent.send_output('error', f"Request to {url} failed with status code: {response.status_code}")
        
        else:
            agent.send_output('error', f"Invalid action: {action}")
    
    except Exception as e:
        agent.send_output('error', f"An error occurred: {str(e)}")

def main():
    agent = MofaAgent(agent_name='CatAPIIntegrator')
    run(agent=agent)

if __name__ == '__main__':
    main()