from typing import Union

import dspy

from mofa.utils.variable.util import get_variable_name




def init_costar_signature(role: Union[str, None] = None, backstory: Union[str, None] = None, output_fields: dict = None, input_fields: dict = None, objective:str=None, specifics:str=None, actions:str=None, results:str=None, example:str=None, answer:str=None):
    """
    Backstory: Provides the background information of the task.
    Objective: Clearly defines the main goal of the task.
    Specifics: Lists the specific requirements of the task.
    Tasks: Describes the tasks that need to be completed.
    Actions: Lists the specific steps to be taken.
    Results: Describes the expected outcomes or results.
    Example: A case study of the task.
    """

    inputs = {}

    for input_field in [role,backstory,objective,specifics,actions,results,example,answer]:
        if input_field is None:
            input_field = ''
        inputs[get_variable_name(input_field, locals())[0]] = input_field

    fields = {
        'question': dspy.InputField(desc="The question we're trying to answer."),
        'objective': dspy.InputField(desc=inputs.get('objective', 'Provides the background information for the task.')),
        'specifics': dspy.InputField(desc=inputs.get('specifics', 'Lists specific requirements for the task.')),
        'actions': dspy.InputField(desc=inputs.get('actions','Enumerates the specific steps that need to be executed.')),
        'results': dspy.InputField(desc=inputs.get('results','Task result output type')),
        'example': dspy.InputField(desc=inputs.get('example','Provides an example related to the task. If there is none, then it is empty. ')),
        'answer': dspy.OutputField(desc=inputs.get('answer','Answer result: ')),
        'role': dspy.InputField(desc=inputs.get('role','Specifies the role or purpose of the module.')),
        'backstory': dspy.InputField(desc=inputs.get('backstory','Provides the background information for the task.'))
    }

    if input_fields:
        for field_name, field_desc in input_fields.items():
            fields[field_name] = dspy.InputField(desc=field_desc)

    if output_fields:
        for field_name, field_desc in output_fields.items():
            fields[field_name] = dspy.OutputField(desc=field_desc)
    # all_fields = {}
    # for field_name, field_desc in fields.items():
    #
    #     if field_desc.json_schema_extra.get('__dspy_field_type') == 'output':
    #         all_fields[field_name] = field_desc
    #
    #     if field_desc.json_schema_extra.get('__dspy_field_type') == 'input':
    #         if field_desc.json_schema_extra.get('desc') != '':
    #             all_fields[field_name] = field_desc
    #         if field_name in ['answer', 'role', 'backstory']:
    #             all_fields[field_name] = field_desc
    #         all_fields[field_name] = field_desc
    COStarSignature = type('COStarSignature', (dspy.Signature,), fields)

    return COStarSignature


def costar_signature(role: Union[str, None] = None, backstory: Union[str, None] = None, output_fields: dict = None, input_fields: dict = None, objective:str=None, specifics:str=None, actions:str=None, results:str=None, example:str=None, answer:str=None):
    """
    Backstory: Provides the background information of the task.
    Objective: Clearly defines the main goal of the task.
    Specifics: Lists the specific requirements of the task.
    Tasks: Describes the tasks that need to be completed.
    Actions: Lists the specific steps to be taken.
    Results: Describes the expected outcomes or results.
    Example: A case study of the task.
    """

    inputs = {}

    for input_field in [role,backstory,objective,specifics,actions,results,example,answer]:
        if input_field is None:
            input_field = ''
        inputs[get_variable_name(input_field, locals())[0]] = input_field

    fields = {
        'question': dspy.InputField(desc="The question we're trying to answer."),
        'objective': dspy.InputField(desc=inputs.get('objective', '')),
        'specifics': dspy.InputField(desc=inputs.get('specifics', '')),
        'actions': dspy.InputField(desc=inputs.get('actions','')),
        'results': dspy.InputField(desc=inputs.get('results','')),
        'example': dspy.InputField(desc=inputs.get('example','')),
        'answer': dspy.OutputField(desc=inputs.get('answer','Answer: ')),
        'role': dspy.InputField(desc=inputs.get('role','Specifies the role or purpose of the module.')),
        'backstory': dspy.InputField(desc=inputs.get('backstory',''))
    }

    if input_fields:
        for field_name, field_desc in input_fields.items():
            fields[field_name] = dspy.InputField(desc=field_desc)

    if output_fields:
        for field_name, field_desc in output_fields.items():
            fields[field_name] = dspy.OutputField(desc=field_desc)
    all_fields = {}
    for field_name, field_desc in fields.items():

        if field_desc.json_schema_extra.get('__dspy_field_type') == 'output':
            all_fields[field_name] = field_desc

        if field_desc.json_schema_extra.get('__dspy_field_type') == 'input':
            if field_desc.json_schema_extra.get('desc') != '':
                all_fields[field_name] = field_desc
            if field_name in ['answer', 'role',]:
                all_fields[field_name] = field_desc
    COStarSignature = type('COStarSignature', (dspy.Signature,), all_fields)

    return COStarSignature
