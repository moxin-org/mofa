import sympy as sp

# Define the variable n as a symbol
n = sp.symbols('n')

# Define the expression for the limit
expression = ((n**4 + 3*n**3 - 6)**0.5 - (n-1)*(n+1)) / n

# Compute the limit as n approaches infinity
limit_result = sp.limit(expression, n, sp.oo)

# Print the result
print(f"The limit of the given expression as n approaches infinity is: {limit_result}")