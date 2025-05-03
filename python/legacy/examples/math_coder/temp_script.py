import sympy as sp

# Define the variable
x = sp.symbols('x')

# Define the equation
equation = x**2 + 2*x + 1

# Solve the equation
solutions = sp.solve(equation, x)

# Print the solutions
print("The solutions to the equation x**2 + 2*x + 1 = 0 are:")
for solution in solutions:
    print(solution)