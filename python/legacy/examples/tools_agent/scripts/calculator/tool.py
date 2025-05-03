from operator import pow, truediv, mul, add, sub
# import wolframalpha
import requests

from langchain.tools import tool

# Define a custom calculator tool
def calculator(query: str) -> str:
    """A simple calculator for performing basic arithmetic operations."""
    try:
        # Use eval to handle basic math expressions, but be careful with security!
        result = eval(query)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def calculator_2(input_query: str):
    """A simple calculator for performing basic arithmetic operations."""
    operators = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
        '^': pow
    }
    try:
        input_query = input_query.replace(' ', '')
        if input_query.isdigit():
            return float(input_query)
        for c in operators.keys():
            left, operator, right = input_query.partition(c)
            if operator in operators:
                return round(operators[operator](calculator(left), calculator(right)), 2)
    except:
        return "The input query is not a methematical expression."

# @tool
# def wolfram_alpha_calculator(input_query: str, api_key: str = ''):
#     wolfram_client = wolframalpha.Client(api_key)
#     res = wolfram_client.query(input_query)
#     # assumption = next(res.pods).text
#     answer = next(res.results).text
#     try:
#         return round(float(answer), 2)
#     except:
#         return "The input query is not for calculating."

@tool
def newton_calculator(operation: str, expression: str):
    """A simple calculator for performing basic arithmetic operations."""
    operation = operation.lower()
    expression = expression.replace('+', '%2B')
    url = f'https://newton.now.sh/api/v2/{operation}/{expression}'

    response = requests.get(url)
    try:
        observation = response.json()
    except:
        observation = response.text
    return observation 
   