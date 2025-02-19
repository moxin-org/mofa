# from datetime import datetime
#
# from pydantic import BaseModel, Field
# from typing import Optional
# import instructor
# import json
# import os
# from dotenv import load_dotenv
# from openai import OpenAI
#
# from mofa.utils.ai.conn import structor_llm
# from mofa.utils.files.read import read_yaml
#
#
#
# class LLMGeneratedRequire(BaseModel):
#     readme: Optional[str] = Field(
#         default=None,
#         json_schema_extra={
#             "description": "遵循GitHub标准，包含安装、使用、贡献者指南的README文件",
#             "example": """# Project\n\n## Installation\n```bash\npip install ...\n```"""
#         }
#     )
#
#     toml: Optional[str] = Field(
#         default=None,
#         json_schema_extra={
#             "description": "符合PEP 621规范的pyproject.toml配置内容",
#             "example": """[tool.poetry]\nname = "..."\n"""
#         }
#     )
#
#     generation_time: str = Field(
#         default_factory=lambda: datetime.now().isoformat(),
#         json_schema_extra={
#             "description": "ISO标准时间戳",
#             "example": "2023-10-01T12:00:00Z"
#         }
#     )
#
#
# def generate_agent_config(user_query:str,agent_config_path:str,env_file_path:str,response_model:object) -> LLMGeneratedRequire:
#     agent_config = read_yaml(
#         file_path=agent_config_path
#     )
#     sys_prompt = agent_config.get('agent', {}).get('prompt', '')
#
#
#     messages = [
#         {
#             "role": "system",
#             "content": sys_prompt
#         },
#         {
#             "role": "user",
#             "content": user_query
#         }
#     ]
#
#     # 关键差异点：直接结构化调用
#     response = structor_llm(env_file=env_file_path, messages=messages, prompt=user_query,response_model=response_model)
#
#     return response
#
#
# # 示例使用程序
# if __name__ == "__main__":
#     try:
#         response_model = LLMGeneratedRequire
#         agent_config_path = '/Users/chenzi/project/zcbc/mofa/python/agent-hub/create-agent-require/create_agent_require/configs/agent.yml'
#         user_query = """
#            下面的代码就是我的数据库的读取代码，我想要你帮我生成一个agent：
#            import psycopg2
#            def read_postgres_database(db_name, db_user, db_password, db_host, db_port, table_name):
#
#                conn = None  # Initialize conn to None
#                try:
#                    conn = psycopg2.connect(
#                        dbname=db_name,
#                        user=db_user,
#                        password=db_password,
#                        host=db_host,
#                        port=db_port
#                    )
#                    cursor = conn.cursor()
#
#                    cursor.execute(f"SELECT * FROM {table_name}")
#                    rows = cursor.fetchall()
#
#                    return rows
#
#                except psycopg2.Error as e:
#                    print(f"Database error: {e}")
#                    return []
#
#                finally:
#                    if conn:
#                        conn.close()
#            """
#
#         env_file_path = '/Users/chenzi/project/zcbc/mofa/python/agent-hub/create-agent-config/create_agent_config/.env.secret'
#
#         result = generate_agent_config(response_model=LLMGeneratedRequire, user_query=user_query, agent_config_path=agent_config_path, env_file_path=env_file_path)
#         print(f"生成结果验证通过：{result.model_dump_json(indent=2)}")
#
#         # 文件保存逻辑（可保持原样）
#         with open("README.md", "w") as f:
#             f.write(result.readme)
#         with open("pyproject.toml", "w") as f:
#             f.write(result.toml)
#
#     except Exception as e:
#         print(f"生成失败：{e}")
