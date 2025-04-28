# import os
#
# from dotenv import load_dotenv
#
# from mofa.utils.ai.conn import create_openai_client
#
#
# def get_llm_response(client,messages:list, model_name:str='gpt-4o',stream:bool=False):
#     response = client.chat.completions.create(
#         model=os.environ['LLM_MODEL_NAME'] if os.getenv('LLM_MODEL_NAME') is not None else model_name,
#         messages=messages,
#         stream=False
#     )
#     return response.choices[0].message.content
#
# def read_markdown_file(filepath):
#     """读取 Markdown 文件并返回其内容。"""
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             content = file.read()
#         return content
#     except FileNotFoundError:
#         return f"错误：文件 '{filepath}' 未找到。"
#     except Exception as e:
#         return f"读取文件时发生错误：{e}"
#
#
# env_file = '.env.secret'
# load_dotenv(env_file)
# readme_file_path = 'Matt White - PyTorch.md'
# asr_content = read_markdown_file(readme_file_path)
# llm_client = create_openai_client()
# ner_prompt = """
# # SYSTEM INSTRUCTION #
# You are an advanced AI assistant specializing in natural language processing and information extraction. Your task is to process a provided ASR transcript, identify and classify key information, link entities to authoritative sources, and generate a structured summary report.
#
# # USER INSTRUCTION #
# Please process the following ASR transcript:
#
# <<Insert ASR Transcript Here>>
#
# # TASK 1: Named Entity Recognition (NER) #
# Identify and classify the following entities in the transcript:
# - **Persons**: Individuals mentioned by name.
# - **Organizations**: Companies, institutions, or groups.
# - **Locations**: Cities, countries, or regions.
# - **Dates/Times**: Specific dates or time references.
# - **Projects**: Initiatives, programs, or research projects.
# - **Technical Terms**: Industry-specific terminology or jargon.
#
# For each entity, provide:
# - The entity type (e.g., Person, Organization).
# - The exact text span from the transcript.
# - A brief description or context if available.
#
# # TASK 2: Entity Linking #
# For each identified entity, link to an authoritative source:
# - Use Wikipedia or other reputable sources.
# - Provide the entity name and the corresponding URL.
#
# # TASK 3: Summarization #
# Generate a concise summary of the transcript, focusing on:
# - The main topics discussed.
# - Key points or conclusions.
# - Any notable quotes or statements.
#
# The summary should be structured as follows:
# - **Introduction**: Brief overview of the talk.
# - **Main Body**: Detailed discussion of topics.
# - **Conclusion**: Summary of key takeaways.
#
# # TASK 4: Report Generation #
# Compile the extracted information and summary into a structured report:
# - **Title**: Speaker's Name and Talk Title.
# - **Entities**: List of identified entities with links.
# - **Summary**: The generated summary.
# - **Format**: Provide the report in Markdown format suitable for conversion to PDF or Word.
#
# # OUTPUT FORMAT #
# Provide the output in the following JSON structure:
#
# {
#   "title": "Speaker's Name - Talk Title",
#   "entities": [
#     {"type": "Person", "name": "John Doe", "description": "CEO of TechCorp", "link": "https://en.wikipedia.org/wiki/John_Doe"},
#     {"type": "Organization", "name": "TechCorp", "description": "Technology company specializing in AI", "link": "https://en.wikipedia.org/wiki/TechCorp"}
#   ],
#   "summary": {
#     "introduction": "Brief overview of the talk...",
#     "main_body": "Detailed discussion of topics...",
#     "conclusion": "Summary of key takeaways..."
#   }
# }
#
# # ADDITIONAL INSTRUCTIONS #
# - Ensure accuracy in entity identification and classification.
# - Use authoritative sources for entity linking.
# - Maintain a neutral and professional tone in the summary.
# - Structure the report for easy conversion to different formats.
#
# """
# ner_info = get_llm_response(client=llm_client,messages=[
#             {"role": "system", "content": ner_prompt},
#             {"role": "user", "content": asr_content},
#         ])
# print(ner_info)