import json
import re
import time
from typing import Union, List
import dspy

from mofa.agent_build.base.module import BaseModule

from mofa.agent_build.base.signature import init_costar_signature, costar_signature
from mofa.kernel.rag.embedding.huggingface import load_embedding_model
from mofa.kernel.rag.vector.pgvector import create_pgvector, delete_vector_collection
from mofa.kernel.rag.vector.util import search_vector, upload_files_to_vector
from mofa.utils.ai.util import json_output_openai_result
from mofa.utils.database.vector.chromadb import create_chroma_db_conn_with_langchain


class BaseRag(BaseModule):
    def __init__(self,role:str=None,backstory:str=None, module_path:str=None,model_name:str=None, pg_connection:str=None, collection_name:str='my_docs', is_upload_file:bool=False, files_path:Union[List[str],str]=None, model_kwargs:dict={'device':0}, chunk_size:int=256, encoding:str= 'utf-8',multi_process:bool=False,context:str=None,temperature:float=0.7,objective:str=None, specifics:str=None, actions:str=None, results:str=None, example:str=None, answer:str=None,input_fields:dict=None,chroma_path:str=None):
        super().__init__(temperature=temperature,context=context,role=role,backstory=backstory,objective=objective, specifics=specifics, actions=actions, results=results, example=example, answer=answer,input_fields=input_fields)

        self.embedding = load_embedding_model(module_path=module_path,model_kwargs=model_kwargs,multi_process=multi_process,model_name=model_name)
        if pg_connection is None and chroma_path is not None:
            self.vectorstore = create_chroma_db_conn_with_langchain(embedding=self.embedding,db_path=chroma_path)
        elif chroma_path is None and pg_connection is not None:
            self.vectorstore = create_pgvector(embedding=self.embedding, collection_name=collection_name, pg_connection=pg_connection)
        if is_upload_file is True and files_path is not None:
            try:
                # self.vectorstore.drop_tables()
                upload_files_to_vector(vectorstore=self.vectorstore,files_path=files_path, chunk_size=chunk_size, encoding=encoding)
            except Exception as e :
                self.embedding = load_embedding_model(module_path=module_path, model_kwargs=model_kwargs,
                                                      multi_process=multi_process, model_name=model_name)
                self.vectorstore = create_pgvector(embedding=self.embedding, collection_name=collection_name,
                                                   pg_connection=pg_connection)
                upload_files_to_vector(vectorstore=self.vectorstore, files_path=files_path, chunk_size=chunk_size,
                                       encoding=encoding)

    def delete_collection(self):
        delete_vector_collection(vectorstore=self.vectorstore)

    def search(self, keywords: Union[List[str],str], k: int = 6):
        return search_vector(vectorstore=self.vectorstore,keywords=keywords,k=k)

    def get_result(self,result_module):
        answer = ''
        try:
            if result_module.answer == '':
                answer = result_module.objective
            else:
                answer = result_module.answer
        except:
            answer = answer = result_module.results
        return answer

    def replace_prefix(self,data:str):
        return data.replace('Question:','').replace('Answer: ','')



class TaskAnalysisModule(BaseModule):
    def __init__(self,role: Union[str, None] = None, backstory: Union[str, None] = None, output_fields: dict = None, input_fields: list[str] = None,objective:str=None,specifics:str=None,actions:str=None,results:str=None,example:str=None):
        super().__init__()
        if role == None:
            self.role = "You're a mission analysis assistant."
        if objective == None:
            self.objective = 'The main goal of the task is to extract and summarize the key information from the submitted task description, clarifying the main points and key requirements.'
        if specifics ==None:
            self.specifics = ('Main elements involved in the task description (e.g., goals, objects, environment).'
                         'Specific requirements and expected outcomes of the task.'
                         'Key points and potential challenges to focus on during task execution.')

        if results == None:
            self.results = "The returned result is a json object No other format or content is required {'task_description':', 'keywords':} task_description is the result of summary and analysis of the task. Keywords is the keyword about this task, which cannot exceed 3 keywords. If keywords cannot be parsed, return []"
        if example == None:
            self.example = """
            问题: "Provide a detailed summary of the theme and explanation of the paper 'Text-Animator Controllable Visual Text Video Generation'. Additionally, explain which papers it cites, what achievements it has made, when it was written, and who the authors are."
            结果: {"task_description": "Provide a detailed summary of the theme and explanation of the paper 'Text-Animator Controllable Visual Text Video Generation'. Additionally, explain which papers it cites, what achievements it has made, when it was written, and who the authors are.","keywords": ["summary", "theme", "Text-Animator Controllable Visual Text Video Generation", "achievements", "authors"]}

            问题: 研究《红楼梦》中人物关系的复杂性。
            {"task_description": "研究《红楼梦》中人物关系的复杂性。","keywords": ["红楼梦", "人物关系", "复杂性"]}
            
            问题: 中国的四大名著是什么?
            {"task_description": "中国的四大名著是什么?","keywords": ["四大名著", "中国"]}
            
            """
        task_analysis_signature = init_costar_signature(role=role, backstory=backstory, output_fields=output_fields, input_fields=input_fields, objective=objective, specifics=specifics, actions=actions, results=results, example=example)
        self.predict = dspy.Predict(task_analysis_signature)
    def forward(self,question:str):
        predict = self.predict(question=question,role=self.role,example=self.example,specifics=self.specifics,results=self.results,**self.no_cache)
        return predict


class FindTaskKeyWordsModule(BaseModule):
    def __init__(self, role: Union[str, None] = None, backstory: Union[str, None] = None, output_fields: dict = None,
                 input_fields: list[str] = None, objective: str = None, specifics: str = None, actions: str = None,
                 results: str = None, example: str = None):
        super().__init__()
        if role == None:
            self.role = "Data extraction assistant"
        if backstory == None:
            self.backstory = "You are a data extraction assistant. Your task is to identify and extract relevant information from the provided task description to enhance data retrieval accuracy."

        if specifics == None:
            self.specifics = """
            Identify key elements (e.g., time frames, authors, topics).Note any specific requirements or constraints.Ensure keywords reflect the main aspects of the question."""

        if results == None:
            self.results = """Return a JSON object structured as {"task_description":"Original question", 'keywords': [up to 3 key terms that clarify aspects of the question]}. The original question should also be included in the keywords but not counted within the limit of three key terms. If specific keywords are not identifiable, return an empty list []."""
        if example == None:
            self.example = """
            question： 你是谁？
            answer： {"task_description": "你是谁？","keywords": ['你是谁？']}
            
            question: "Provide a detailed summary of the theme and explanation of the paper 'Text-Animator Controllable Visual Text Video Generation'. Additionally, explain which papers it cites, what achievements it has made, when it was written, and who the authors are."
            answer: {"task_description": "Provide a detailed summary of the theme and explanation of the paper 'Text-Animator Controllable Visual Text Video Generation'. Additionally, explain which papers it cites, what achievements it has made, when it was written, and who the authors are.","keywords": ["summary", "theme", "Text-Animator Controllable Visual Text Video Generation", "achievements", "authors"]}

            question: 研究《红楼梦》中人物关系的复杂性。
            answer: {"task_description": "研究《红楼梦》中人物关系的复杂性。","keywords": ["红楼梦中人物关系的复杂性", "研究《红楼梦》中人物关系的复杂性。"]}

            question: 中国的四大名著是什么?
            answer： {"task_description": "中国的四大名著是什么?","keywords": ["中国的四大名著是什么?", "中国四大名著"]}

            """

        self.answer='Must return a JSON object or a None'
        task_analysis_signature = costar_signature(role=self.role,
                                                   actions=self.actions,
                                                   results=self.results, example=self.example, specifics=self.specifics, answer=self.answer)
        self.task_predict = dspy.Predict(task_analysis_signature)
    def serialization_result(self,result:str):
        try:
            return json_output_openai_result(data=result)
        except:
            match = re.search(r'Answer:\s*(\{.*\})', result)
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                return data
        else:
            return result

    def forward(self, question: str,*args,**kwargs):
        result = self.task_predict(question=question, role=self.role, example=self.example,
                               results=self.results,specifics=self.specifics,actions=self.actions)
        return result


class QualityEnhancerModule(BaseModule):
    def __init__(self, role: Union[str, None] = None, backstory: Union[str, None] = None, output_fields: dict = None,
                 input_fields: list[str] = None, objective: str = None, specifics: str = None, actions: str = None,
                 results: str = None, example: str = None):
        super().__init__()
        if role is None:
            self.role = "Quality Enhancer"
        if backstory is None:
            self.backstory = 'This module is designed to enhance the quality of answers by integrating RAG and LLM outputs.Primarily use data from rag_data, with llm_result as a supplement'
        if objective is None:
            self.objective = """To optimize the final result for a given question, integrate the outputs generated by the Retrieval-Augmented Generation (RAG) system with the responses generated by the Large Language Model (LLM). This involves combining the retrieved and generated information based on the question to provide a more accurate and comprehensive answer. Primarily use data from rag_data, with llm_result as a supplement. If rag_data is empty, use llm_result as the main data source; if llm_result is empty, use rag_data as the main data source"""
        if actions is None:
            self.actions = "Merge and analyze RAG and LLM outputs to generate the final answer.Primarily use data from rag_data, with llm_result as a supplement."
        if input_fields is None:
            self.input_fields = {'rag_data':'Data after rag query','llm_data':'Data after LLM query'}

        data_merge_signature = costar_signature(role=self.role, backstory=self.backstory, objective=self.objective, actions=self.actions, input_fields=self.input_fields)
        self.qualit_yenhancer_predict = dspy.Predict(data_merge_signature)

    def forward(self,question:str, rag_data: str, llm_data: str):
        predict = self.qualit_yenhancer_predict(question=question,rag_data=rag_data,llm_data=llm_data,role=self.role,backstory=self.backstory,objective=self.objective,actions=self.actions,**self.no_cache)
        return predict

class EvaluationResultModule(BaseModule):
    def __init__(self, role: Union[str, None] = None, backstory: Union[str, None] = None, output_fields: dict = None,
                 input_fields: list[str] = None, objective: str = None, specifics: str = None, actions: str = None,
                 results: str = None, example: str = None):
        super().__init__()
        if role is None: role = 'Response validation assistant.'
        if objective is None: objective = "Determine if the answer satisfies the question's requirements."
        if specifics is None:  specifics = """Analyze the question to identify key elements and expectations.
        Compare the answer against these elements.
        Assess whether the answer fully addresses the question."""
        if results is None: results = 'Respond with "Yes" if the answer meets the requirements, or "No" if it does not.'
        if example is None: example = """
        1. **Question:** "List all publications in AI from 2015 to 2023 focusing on neural networks."
           - **Answer:** "Publications include research on neural networks in AI from 2015 to 2023."
           - **Result:** "Yes"
        2. **Question:** "Find research articles about quantum computing breakthroughs in 2021."
           - **Answer:** "Articles from 2020 on general quantum computing topics."
           - **Result:** "No"
        """
        self.role = role
        self.objective = objective
        self.specifics = specifics
        self.results = results
        self.example = example
        self.evaluation_result =  dspy.Predict(init_costar_signature(input_fields={'context':"The content that needs suggestions"},role=role,objective=objective,specifics=specifics,
                                                                  results=results,example=example))

    def forward(self,question:str,context:str)->bool:
        stop_condition = self.evaluation_result(role=self.role,
                                                objective=self.objective,
                                                specifics=self.specifics,
                                                results=self.results,
                                                example=self.example, question=question, context=context,
                                                **self.no_cache)
        status = False
        if stop_condition.answer =='':
            if 'Yes' in stop_condition.actions or 'Yes' in stop_condition.backstory:
                status= True
        else:
            if 'Yes' in stop_condition.answer :
                status = True
        return status

