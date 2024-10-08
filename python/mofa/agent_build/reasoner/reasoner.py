import json
import time
from typing import List, Union

import dspy

from mofa.agent_build.base.module import BaseModule


from mofa.agent_build.reasoner.base import BaseRag, FindTaskKeyWordsModule, QualityEnhancerModule
from mofa.kernel.tools.web_search import search_web_with_serper


class ReasonerModule(BaseModule):
    def __init__(self,reasoner_signature: dspy.Signature=None,role:str=None,backstory:str=None,temperature:float = 0.7,context:str=None,objective:str=None, specifics:str=None, actions:str=None, results:str=None, example:str=None, answer:str=None,input_fields:dict=None):
        super().__init__(temperature=temperature,context=context,role=role,backstory=backstory,objective=objective, specifics=specifics, actions=actions, results=results, example=example, answer=answer,input_fields=input_fields)
class ReasonerWebSearchModule(ReasonerModule):
    def __init__(self,serper_api_key: str,reasoner_signature: dspy.Signature=None,role:str=None,backstory:str=None,temperature:float = 0.7,context:str=None,objective:str=None, specifics:str=None, actions:str=None, results:str=None, example:str=None, answer:str=None,input_fields:dict=None,search_num:int=10,search_engine_timeout:int=5):
        super().__init__(temperature=temperature,context=context,role=role,backstory=backstory,objective=objective, specifics=specifics, actions=actions, results=results, example=example, answer=answer,input_fields=input_fields)
        self.search_num = search_num
        self.search_engine_timeout = search_engine_timeout
        self.serper_api_key = serper_api_key

    def forward(self, question:str,*args,**kwargs,) -> str:
        web_result = json.dumps(search_web_with_serper(query=question, subscription_key=self.serper_api_key,search_num=self.search_num,search_engine_timeout=self.search_engine_timeout))
        print('web_search  : ',web_result )
        variable_dict = self.create_signature_variable_dict
        if 'answer' in variable_dict:
            del variable_dict['answer']
        if len(kwargs) >0:
            variable_dict.update(kwargs.get('kwargs'))
        if 'context' in list(variable_dict.keys()):
            del variable_dict['context']
        if self.context is None:
            predict = self.predict(question=question,web_context=web_result,**variable_dict,**self.no_cache)
        else:
            predict = self.predict(question=question,context=self.context,web_context=web_result, **variable_dict, **self.no_cache)
        return {'web_search_results':predict.answer,'web_search_resource':web_result}
class ReasonerRagModule(BaseRag):
    def __init__(self, module_path:str=None,model_name:str=None, pg_connection:str=None, collection_name:str='my_docs', is_upload_file:bool=False, files_path:Union[List[str],str]=None,encoding:str= 'utf-8',chunk_size:int=256,multi_process:bool=False,rag_search_num:int=5,context:str=None,temperature:float=0.7,objective:str=None, specifics:str=None, actions:str=None, results:str=None, example:str=None, answer:str=None,input_fields:dict=None,backstory:str=None,role:str=None,chroma_path:str=None):
        super().__init__(module_path=module_path,chroma_path=chroma_path, pg_connection=pg_connection, collection_name=collection_name, is_upload_file=is_upload_file, files_path=files_path,encoding=encoding,chunk_size=chunk_size,multi_process=multi_process,model_name=model_name,context=context,temperature=temperature,role=role,backstory=backstory,objective=objective, specifics=specifics, actions=actions, results=results, example=example, answer=answer,input_fields=input_fields)

        self.task_evaluation = FindTaskKeyWordsModule()
        self.quality_enhancer = QualityEnhancerModule()
        self.rag_search_num = rag_search_num
    def rag_retrieval(self,question:str):
        try:
            task_result = self.task_evaluation.serialization_result(self.task_evaluation.forward(question=question).answer)
            keywords = task_result.get('keywords')
            keywords.append(question)
            keywords = list(set(keywords))
        except Exception as e:
            print(e)
            keywords = [question]
        print('task keywords  : ', keywords)

        all_rag_result = self.search(keywords=keywords, k=self.rag_search_num)
        return all_rag_result
    def rag_search(self, question: str, llm_result: str = ''):
        try:
            task_result = self.task_evaluation.serialization_result(self.task_evaluation.forward(question=question).answer)
            keywords = task_result.get('keywords')
            keywords.append(question)
        except:
            keywords = [question]
        print('task keywords  : ', keywords)

        all_rag_result = self.search(keywords=keywords, k=self.rag_search_num)
        rag_datas = []
        for rag_result in all_rag_result:
            if isinstance(rag_result,dict):
                for key, value in rag_result.items():
                    if len(value) >0: rag_datas+=(value)
        t3 = time.time()
        quality_enhancer_result = self.quality_enhancer.forward(question=question, rag_data=json.dumps(all_rag_result),
                                                                llm_data=llm_result, )


        result = ''
        if quality_enhancer_result.answer == '':
            result = quality_enhancer_result.specifics
        else:
            result = quality_enhancer_result.answer
        return result

    def forward(self, question:str,*args,**kwargs):
        return self.rag_search(question=question)
