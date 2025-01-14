from amplify import VariableGenerator
from qubo_constraints import create_Q_matrix, print_str_matrix
from dwave_config import print_magic_square, unit_tests

def display_amplify_solution(binary_vars, n, constraints_added, unary_matrix_len):
    magic_sqaure = [[None] * unary_matrix_len for i in range(unary_matrix_len)]

    print("result binary vars:")
    ordered = {}
    for var in binary_vars:
        #print(f"{var} == {value}")
        #print(f"{var} == {binary_vars[var]}")
        #print()
        ordered[str(var)] = binary_vars[var]
    
    #print("ordered:")
    #print(ordered)
    
    
    magic_square = [[-1000] * n for j in range(n)]

    row_index = 0
    col_index = 0
    s = 0

    n_squared = n**2

    i = 0
    for key in ordered:
        #print(f"{var} == {value}")
        #print(f"{var} == {binary_vars[var]}")
        print(ordered[key], ",", end="")
        s+= int(ordered[key])

        if ((i+1) % int(n_squared) == 0):
            print(f"   Variable {(i+1)/int(n_squared)} == ", s)
            #print(f"Setting MS[{row_index}][{col_index}] = {s}")
            magic_square[row_index][col_index] = s
            #print(f"MS[{row_index}][{col_index}] == {magic_square[row_index][col_index]}")

            s = 0

            col_index += 1
            if (col_index >= n):
                col_index = 0
                row_index+=1
        
        i += 1

    print("|||||||||||||||||||||||||")
    print_magic_square(magic_square)

    m = int((n * (n_squared+1) / 2))
    unit_tests(magic_square, n, m , constraints_added)
    

def amplify_AE(n, num_seconds):
    gen = VariableGenerator()     # Create a generator for decision variables

    Q_unary, constraints_added = create_Q_matrix(n)

    n_squared = n*n
    magic_square_len = n_squared

    unary_matrix_len = magic_square_len * magic_square_len
    Q_matrix_len = unary_matrix_len * unary_matrix_len

    #Q unary is an n**4 by n**4 matrix, for the Q matrix representing unnary vars in xQx

    print("Creating Q",unary_matrix_len, "x",unary_matrix_len, "matrix for amplify")
    print("Creating ",unary_matrix_len * unary_matrix_len, "binary decision vars")


    x = gen.array("Binary", unary_matrix_len * unary_matrix_len)    # Generate a variable array of n**8 binary decision variables: all the vars in the n**4 by n**4 x matrix
    #print("binary var array:", x)
    #print(x)
    print()

    temp_matrix = [[None] * unary_matrix_len for i in range(unary_matrix_len)]

    for r in range(0, unary_matrix_len):
        for c in range(0, unary_matrix_len):
            coefficient = Q_unary[r][c]

            temp_matrix[r][c] = x[r] * x[c] * coefficient

    #print("temp_matrix")
    #print(temp_matrix)


    flattened = [item for row in temp_matrix for item in row]


    objective_function = sum(flattened)

    #print("objective_function sum:", objective_function)

    from amplify import FixstarsClient
    from amplify import LeapHybridSamplerClient, Model, solve

    token = "AE/ElVGDGcyOwEywxvJqaUe9PzILy2IQuWp"

    '''hybrid_client = LeapHybridSamplerClient()
    hybrid_client.solver = "hybrid_binary_quadratic_model_version2"
    hybrid_client.token = token
    g = VariableGenerator()
    q = g.array("Binary", 2)
    f = q[0] * q[1] + q[0] - q[1] + 1

    hybrid_model = Model(f)
    #hybrid_model = Model(objective_function)
    hybrid_result = solve(hybrid_model, hybrid_client)
    '''
    
    pure_client = FixstarsClient() 
    pure_client.token = token

    #client.parameters.timeout = int(num_seconds*1000)    # Set run time to 10000 ms
    start = time.time()
    result = solve(objective_function, pure_client)
    end = time.time()

    obj_function_value = result.best.objective   # Value of the objective function
    result_binary_vars = result.best.values      # Values of the variables

    #print(f"Q matrix  = {q.evaluate(result.best.values)}")

    
    display_amplify_solution(result_binary_vars, n, constraints_added, unary_matrix_len)
    #display_amplify_solution(hybrid_result.best.values, n, constraints_added, unary_matrix_len)
    print(f"Time elasped for amplify pure for n = {n}:")
    print(end-start, "seconds")

    print("#########################")


import time
n = int(input("Enter n: "))

amplify_AE(n, 0)

