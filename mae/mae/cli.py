import json
import click
import yaml
from pathlib import Path
from pathlib import Path

from mae.utils.files.dir import get_subdirectories

current_path = Path.cwd()
from mae.agent_link.merge_agents.merge_dataflow import MergeDataflow

@click.command()
@click.option(
    '--main-dataflow-yml',
    required=True,
    type=click.Path(exists=True),
    help="Main dataflow YAML file path. Example: --main-dataflow-yml ./Moxin-App-Engine/mae/mae/agent_link/agent_template/web_search/web_search_dataflow.yml"
)
@click.option(
    '--additional-dataflow-yml',
    required=True,
    type=click.Path(exists=True),
    help="Additional dataflow YAML file path. Example: --additional-dataflow-yml ./Moxin-App-Engine/mae/mae/agent_link/agent_template/reasoner/reasoner_dataflow.yml"
)
@click.option(
    '--dependencies',
    required=True,
    type=str,
    help="Dependencies as JSON string. Example: --dependencies '[{\"source_node_id\": [\"more_question_agent\"], \"target_node_id\": \"reasoner_agent\", \"target_node_inputs\": [{\"output_node_id\": \"more_question_agent\", \"output_params_name\": \"more_question_results\"}]}]'")
@click.option(
    '--output-directory',
    type=click.Path(exists=True),
    help="Output directory path. Example: --output-directory /path/to/output_directory",
    default = str(current_path.parent /'examples'/'generate')
)
@click.option(
    '--search-directory',
    type=click.Path(exists=True),
    help="Search directory path. Example: --search-directory ./Moxin-App-Engine/mae/mae/agent_link/agent_template",
    default=str(current_path/'agent_link'/'agent_template')
)
def generate_agents_cli(main_dataflow_yml:str, additional_dataflow_yml:str, dependencies:str, output_directory:str, search_directory:str):
    """
    CLI to generate merged agents configuration.
    """
    dependencies = json.loads(dependencies)

    merge_dataflow = MergeDataflow()
    merge_dataflow.copy_agents_files(agents_dir_path=search_directory, agents_name=get_subdirectories(directory=search_directory),
                                     output_dir_path=output_directory, subdirectories=['scripts', 'configs'])
    merged_agents = merge_dataflow.generate_agents(
        main_dataflow_yml=main_dataflow_yml,
        additional_dataflow_yml=additional_dataflow_yml,
        dependencies=[dependencies],
        output_dir_path=output_directory,
        search_directory=search_directory
    )

    click.echo(f"Merged agents configuration has been written to {output_directory}")

if __name__ == '__main__':
    # main_dataflow_yml = '/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/mae/agent_link/agent_template/web_search/web_search_dataflow.yml'
    # additional_dataflow_yml = '/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/mae/agent_link/agent_template/reasoner/reasoner_dataflow.yml'
    # dependencies = "{ \"target_node_id\": \"reasoner_agent\", \"target_node_inputs\": [{\"output_node_id\": \"more_question_agent\", \"output_params_name\": \"more_question_results\"}]}"
    # output_directory = str(current_path.parent /'examples'/'generate')
    # search_directory = str(current_path/'agent_link'/'agent_template')
    # generate_agents_cli(main_dataflow_yml=main_dataflow_yml, additional_dataflow_yml=additional_dataflow_yml,
    #                     dependencies=dependencies, output_directory=output_directory, search_directory=search_directory)
    generate_agents_cli()

