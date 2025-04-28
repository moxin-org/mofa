import os

from dotenv import load_dotenv

from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mofa.kernel.rag.embedding.huggingface import load_embedding_model
from mofa.kernel.rag.vector.util import search_vector
from mofa.utils.database.vector.chromadb import create_chroma_db_conn_with_langchain


@run_agent
def run(agent:MofaAgent):
    env_file = '.env.secret'
    load_dotenv(env_file)
    chroma_path = os.getenv('VECTOR_CHROME_PATH','chroma_store')
    model_name = os.getenv('EMBEDDING_MODEL_NAME', 'text-embedding-3-large')
    os.environ["OPENAI_API_KEY"] = os.getenv('EMBEDDING_API_KEY', )
    embedding = load_embedding_model(model_name=model_name)
    vectorstore = create_chroma_db_conn_with_langchain(embedding=embedding, db_path=chroma_path)

    query = agent.receive_parameter('query')
    vector_results = search_vector(vectorstore=vectorstore, keywords=[query], k=os.getenv('VECTOR_SEARCH_NUM', 12))
    agent.send_output(agent_output_name='gosim_rag_result',agent_result=vector_results)
def main():
    agent = MofaAgent(agent_name='gosim-rag-agent')
    run(agent=agent)
if __name__ == "__main__":
    main()
