from amplify import VariableGenerator
from qubo_constraints import create_Q_matrix, print_str_matrix
from dwave_config import print_magic_square

def display_amplify_solution(binary_vars, n):
    magic_sqaure = [[None] * unary_matrix_len for i in range(unary_matrix_len)]

    print("result binary vars:")
    ordered = {}
    for var in binary_vars:
        #print(f"{var} == {value}")
        #print(f"{var} == {binary_vars[var]}")
        ordered[var] = binary_vars[var]
    
    magic_square = [[None] * n for i in range(n)]
    row_index = 0
    col_index = 0

    s = 0

    i = 0
    for var in binary_vars:
        #print(f"{var} == {value}")
        #print(f"{var} == {binary_vars[var]}")
        print(binary_vars[var], ",", end="")
        s+= int(binary_vars[var])

        if ((i+1) % int(n_squared) == 0):
            print(f"   Variable {i/int(n_squared)} == ", s)
            magic_square[row_index][col_index] = s

            s = 0

            col_index += 1
            if (col_index >= n):
                col_index = 0
                row_index+=1
        
        i += 1

    print("|||||||||||||||||||||||||")
    print_magic_square(magic_square)
    


gen = VariableGenerator()     # Create a generator for decision variables

n = int(input("Enter n: "))
Q_unary, constraints_added = create_Q_matrix(n)

n_squared = n*n
magic_square_len = n_squared

unary_matrix_len = magic_square_len * magic_square_len
Q_matrix_len = unary_matrix_len * unary_matrix_len

#Q unary is an n**4 by n**4 matrix, for the Q matrix representing unnary vars in xQx

print("Creating Q",unary_matrix_len, "x",unary_matrix_len, "matrix for amplify")
print("Creating ",unary_matrix_len * unary_matrix_len, "binary decision vars")


q = gen.array("Binary", unary_matrix_len * unary_matrix_len)    # Generate a variable array of n**8 binary decision variables: all the vars in the n**4 by n**4 Q matrix
print("binary var array:", q)
print(q)
print()

temp_matrix = [[None] * unary_matrix_len for i in range(unary_matrix_len)]

for r in range(0, unary_matrix_len):
    for c in range(0, unary_matrix_len):
        coefficient = Q_unary[r][c]

        temp_matrix[r][c] = q[r] * q[c] * coefficient


flattened = [item for row in temp_matrix for item in row]
print("flattened:")
print(flattened)


objective_function = sum(flattened)

print("objective_function sum:", objective_function)

from amplify import FixstarsClient
client = FixstarsClient()
client.token = "AE/uMA2OJDZC4Scvgu9wWMRLGmFDv6aOZmi" 
num_seconds = 1
client.parameters.timeout = num_seconds*1000    # Set run time to 10000 ms

from amplify import solve
result = solve(objective_function, client)

obj_function_value = result.best.objective   # Value of the objective function
result_binary_vars = result.best.values      # Values of the variables

print(f"Q matrix  = {q.evaluate(result.best.values)}")

display_amplify_solution(result_binary_vars, n)