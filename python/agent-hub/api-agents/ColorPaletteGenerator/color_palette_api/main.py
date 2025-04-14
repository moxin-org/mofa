from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import logging
from typing import Optional, Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@run_agent
def run(agent: MofaAgent):
    """
    Main execution function for the ColorPaletteGenerator agent.
    Handles input, processes the color palette request, and sends the output.
    """
    try:
        # Input handling
        input_params = agent.receive_parameters(['model', 'input_colors'])
        model = input_params.get('model', 'default')
        input_colors = input_params.get('input_colors', [[44, 43, 44], [90, 83, 82], "N", "N", "N"])

        # Validate input_colors
        if not isinstance(input_colors, list) or len(input_colors) != 5:
            raise ValueError("Input colors must be a list of 5 elements (RGB values or 'N').")

        # Prepare API request data
        data = {
            "model": model,
            "input": input_colors
        }

        # Make API request
        response = requests.post("http://colormind.io/api/", json=data)

        if response.status_code == 200:
            palette = response.json().get('result', [])
            logger.info(f"Generated color palette: {palette}")
            agent.send_output(
                agent_output_name='color_palette',
                agent_result=palette
            )
        else:
            logger.error(f"Request failed with status code: {response.status_code}")
            agent.send_output(
                agent_output_name='error',
                agent_result=f"API request failed with status code: {response.status_code}"
            )

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def main():
    """
    Initialize and run the ColorPaletteGenerator agent.
    """
    agent = MofaAgent(agent_name='ColorPaletteGenerator')
    run(agent=agent)

if __name__ == '__main__':
    main()