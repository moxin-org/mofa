import random
from typing import Union
import dspy
from mofa.agent_build.base.signature import costar_signature


class BaseModule(dspy.Module):
    def __init__(self,role: Union[str, None] = None, backstory: Union[str, None] = None, context:str=None,temperature:float=0.7,objective:str=None, specifics:str=None, actions:str=None, results:str=None, example:str=None, answer:str=None,predict_type:str='predict',input_fields:dict=None):
        super().__init__()
        self.context = context
        self.temperature = temperature
        self.role = role
        self.backstory = backstory
        self.objective = objective
        self.specifics = specifics
        self.actions = actions
        self.results = results
        self.example = example
        self.answer = answer
        self.predict_type = predict_type
        self.input_fields = input_fields
        self.predict = self.creat_predict
    @property
    def no_cache(self):
        return dict(temperature=self.temperature + 0.0001 * random.uniform(-1, 1))

    @property
    def create_signature_variable_dict(self) -> dict:
        base_fields = {'role': self.role, 'backstory': self.backstory}
        insert_fields = {}

        for field,field_value in {'objective':self.objective, 'specifics':self.specifics, 'actions':self.actions, 'results':self.results, 'example':self.example, 'answer':self.answer}.items():
            if field_value is not None:
                if isinstance(field_value,list):
                    field_value = '\n'.join(field_value)
                insert_fields[field] = field_value
        if len(insert_fields) > 0:
            base_fields.update(insert_fields)
        return base_fields
    @property
    def create_signature(self):
        variable_dict = self.create_signature_variable_dict
        if self.input_fields is not None:
            variable_dict.update(self.input_fields)
        return costar_signature(**self.create_signature_variable_dict, input_fields=self.input_fields)

    @property
    def creat_predict(self):
        if self.predict_type == 'predict':
            return dspy.Predict(self.create_signature)
        if self.predict_type == 'cot' or self.predict_type=='COT':
            return dspy.ChainOfThought(self.create_signature)


    def forward(self, question:str,*args,**kwargs,) -> str:
        variable_dict = self.create_signature_variable_dict
        if 'answer' in variable_dict:
            del variable_dict['answer']
        if len(kwargs) >0:
            variable_dict.update(kwargs.get('kwargs'))
        if 'context' in list(variable_dict.keys()):
            del variable_dict['context']
        if self.context is None:
            predict = self.predict(question=question,**variable_dict,**self.no_cache)
        else:
            predict = self.predict(question=question,context=self.context, **variable_dict, **self.no_cache)
        return predict.answer