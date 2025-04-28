# import os
#
# from dotenv import load_dotenv
# from firecrawl import FirecrawlApp
# import json
#
# from mofa.kernel.rag.embedding.huggingface import load_embedding_model
# from mofa.kernel.rag.vector.util import search_vector
# from mofa.kernel.tools.web_search import search_web_with_serper
# from mofa.utils.ai.conn import create_openai_client
# from mofa.utils.database.vector.chromadb import create_chroma_db_conn_with_langchain
#
#
# class FireCrawl:
#     def __init__(self, api_key: str = None, env_file: str = '.env.secret', crawl_params: dict = None):
#         if api_key is None:
#             load_dotenv(env_file)
#             api_key = os.getenv("FIRECRAWL_API_KEY",'fc-9756a3e36dee45f189c3b7b72bafa3c6')
#         self.crawl = FirecrawlApp(api_key=api_key)
#         if crawl_params is None:
#             crawl_params = {
#                 "maxDepth": 2,  # Number of research iterations
#                 "timeLimit": 180,  # Time limit in seconds
#                 "maxUrls": 12  # Maximum URLs to analyze
#             }
#         self.crawl_params = crawl_params
#
#     def on_activity(self, activity):
#         print(f"[{activity['type']}] {activity['message']}")
#
#     def deep_research(self, query: str, ):
#         analysis_prompt = """
# Development History: The speaker's growth path in the industry, major accomplishments, and technological breakthroughs.
#
# Personal Story: The speaker's background, career transitions, and challenges faced along the way, as well as how they overcame them.
#
# Educational Background: The speaker's education history, including undergraduate, master’s, and doctoral degrees, along with the universities attended.
#
# Patents: Whether the speaker holds any technological patents, and the number and scope of those patents.
#
# Personal Information: Basic details about the speaker, including life experiences that highlight their personal characteristics.
#
# Social Media and Open Source Contributions: The speaker’s activity on social media platforms and contributions to open-source projects (e.g., GitHub).
#
# Professional Experience: The speaker’s work history, including companies they’ve worked for, roles held, and key project experiences."""
#         results = self.crawl.deep_research(query=query,
#                                            max_depth=3,max_urls=12, on_activity=self.on_activity,analysis_prompt=analysis_prompt)
#         source_data = results['data']['sources']
#         analysis_data = results['data']['finalAnalysis']
#         return source_data, analysis_data
#
# def use_file_crawl(input_data:str):
#     firecrawl = FireCrawl()
#     result = firecrawl.deep_research(input_data)
#     print(result)
#     return result
# def get_llm_response(client,messages:list, model_name:str='gpt-4o',stream:bool=False):
#     response = client.chat.completions.create(
#         model=os.environ['LLM_MODEL_NAME'] if os.getenv('LLM_MODEL_NAME') is not None else model_name,
#         messages=messages,
#         stream=False
#     )
#     return response.choices[0].message.content
# env_file = '.env.secret'
# load_dotenv(env_file)
# os.environ["OPENAI_API_KEY"] = 'sk-'
#
# model_name='text-embedding-3-large'
# chroma_path = 'chroma_store'
# user_input = """
# Sray Agarwal
# Head of Responsible AI (EMEA & APAC) at Infosys
# linkedin
# Sray Agarwal has applied AI and analytics from Financial Services to Hospitality and has led the development of Responsible AI framework for multiple banks in the UK and the US.
# Based out of London, his is conversant in Predictive Modelling, Forecasting and advanced Machine Learning with profound knowledge of algorithms and advanced statistic, Sray is Head of Responsible AI (EMEA & APAC) at Infosys.
# He is an active blogger and has given his talks on Ethical AI at major AI conferences across the globe (more than 20) and has podcasts, video interviews and lectures on reputed websites and social media at United Nations, Microsoft, ODSC to name a few.
# His contribution to the development of the technology was recognised by Microsoft when he won the Most Valued Professional in AI award in 2020 to 2025. He is also an expert for United Nations (UNCEFACT) and have recently authored a book on Responsible AI published by Springer.
# He has been a trainer with leading consulting firms and have delivered training on business transformation using AI. He is guest lecturer at Jio institute. He holds patents on RAI system and methods.
# """
# extract_speaker_prompt = """
# # CONTEXT #
# You are an advanced AI assistant trained to extract and organize detailed information from speaker biographies. The provided text contains a speaker's professional background, achievements, and areas of expertise.
#
# # OBJECTIVE #
# Extract the following information from the provided biography:
# 1. **Name**: The full name of the speaker.
# 2. **Organization**: The current organization or company the speaker is affiliated with.
# 3. **Keywords**: A list of at least five keywords or phrases that encapsulate the speaker's areas of expertise or focus.
# 4. **Personal Journey**: A brief narrative highlighting the speaker's career path, significant achievements, and contributions to their field.
#
# # STYLE #
# Present the information in a structured and clear format, using bullet points or numbered lists where appropriate. Ensure that the response is easy to read and understand.
#
# # TONE #
# Maintain a professional and neutral tone throughout the response.
#
# # AUDIENCE #
# This information is intended for event organizers, researchers, and professionals seeking to understand the speaker's background and expertise.
#
# # RESPONSE FORMAT #
# Provide the extracted information in the following JSON format:
# {
#   "name": "Speaker's Full Name",
#   "organization": "Current Organization or Company",
#   "keywords": ["Keyword1", "Keyword2", "Keyword3", "Keyword4", "Keyword5"],
#   "personal_journey": "A brief narrative of the speaker's career path and achievements."
# }
#
# Input Biography:
# {Insert the speaker's biography text here}
#
# """
# summary_prompt = """
# # CONTEXT #
# You are an advanced AI assistant tasked with compiling a detailed and accurate biography of a speaker. The provided information includes data from multiple sources: academic papers, news articles, personal experiences, and media appearances.
#
# # OBJECTIVE #
# Consolidate the provided information into a cohesive and comprehensive speaker biography. Ensure that the summary is accurate, well-organized, and reflects the speaker's professional journey and contributions.
#
# # STYLE #
# The biography should be written in a formal, professional tone, suitable for inclusion in conference programs, academic publications, or professional networking platforms.
#
# # TONE #
# Maintain an objective and neutral tone, focusing on factual information and the speaker's professional achievements.
#
# # AUDIENCE #
# This biography is intended for an audience of professionals, academics, and industry experts seeking to understand the speaker's background and expertise.
#
# # RESPONSE FORMAT #
# Provide the consolidated biography in the following structured format:
#
# {
#   "name": "Speaker's Full Name",
#   "organization": "Current Organization or Affiliation",
#   "keywords": ["Keyword1", "Keyword2", "Keyword3", "Keyword4", "Keyword5"],
#   "personal_journey": "A detailed narrative of the speaker's career path, including education, key positions held, significant achievements, and contributions to their field.",
#   "papers": ["Title of Paper 1", "Title of Paper 2", "Title of Paper 3", "Title of Paper 4", "Title of Paper 5"],
#   "news": ["Title of News Article 1", "Title of News Article 2", "Title of News Article 3", "Title of News Article 4", "Title of News Article 5"],
#   "media": ["Title of Media Appearance 1", "Title of Media Appearance 2", "Title of Media Appearance 3", "Title of Media Appearance 4", "Title of Media Appearance 5"],
#   "awards": ["Award Name 1", "Award Name 2", "Award Name 3", "Award Name 4", "Award Name 5"],
#   "speaking_engagements": ["Event 1", "Event 2", "Event 3", "Event 4", "Event 5"],
#   "publications": ["Publication 1", "Publication 2", "Publication 3", "Publication 4", "Publication 5"]
#   "video": ["Video 1", "Video 2", "Video 3", "Video 4", "Video 5"],
# }
# """
# embedding = load_embedding_model(model_name=model_name)
# vectorstore = create_chroma_db_conn_with_langchain(embedding=embedding,db_path=chroma_path)
# llm_client = create_openai_client()
# speaker_info = get_llm_response(client=llm_client,messages=[
#             {"role": "system", "content": extract_speaker_prompt},
#             {"role": "user", "content": user_input},
#         ])
# speaker_info_data = speaker_info.replace('\n','').replace('```json','').replace('\n```','').replace('```','')
# speaker_info_data = json.loads(speaker_info_data)
# print(speaker_info)
# speaker_name_and_organization = speaker_info_data.get('name') + ' - ' + speaker_info_data.get('organization')
# firecrawl_result = use_file_crawl(speaker_name_and_organization)
# serper_result = search_web_with_serper(query=speaker_name_and_organization, subscription_key=os.getenv("SERPER_API_KEY"),search_num=15)
#
# vector_results = search_vector(vectorstore=vectorstore,keywords=[speaker_name_and_organization],k=12)
#
# summary_messages = [
#             {"role": "system", "content": summary_prompt},
#             {"role": "user", "content": 'firecrawl_result: ' + json.dumps(firecrawl_result)},
#             {"role": "user", "content": 'serper_result: ' +json.dumps(serper_result)},
#             {"role": "user", "content": 'rag_result : '+json.dumps(vector_results)},
#     ]
# summary_speaker_info = get_llm_response(client=llm_client,messages=summary_messages)
# print(summary_speaker_info)