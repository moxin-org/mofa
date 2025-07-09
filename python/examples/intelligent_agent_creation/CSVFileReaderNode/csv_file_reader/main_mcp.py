from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import csv
from io import StringIO
def read_csv(file_content):
    csv_reader = csv.reader(StringIO(file_content))
    data = [row for row in csv_reader]
    return data
@run_agent
def run(mofa_agent: MofaAgent):
    mofa_agent.register_mcp_tool(read_csv)
    mofa_agent.run_mcp()

def main():
    agent = MofaAgent(agent_name='CSVFileReaderNode')
    run(mofa_agent=agent)

if __name__ == '__main__':
    main()
