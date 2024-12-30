
from dwave.system import DWaveSampler, EmbeddingComposite
import dimod
import os

def print_dwave_matrix(Q):
    print("####################")
    print("DWAVE Q MATRIX:")
    print("")
    for obj in Q:
        print(obj, ":", Q[obj])
    print("####################")


def convert_matrix_for_dwave(matrix):
    #Q = {('x1', 'x1'): 1, ('x2', 'x2'): 1, ('x1', 'x2'): 2}
    Q = {}

    #in upper triangular form, so don't look at anything below diagonal
    for row in range(0, len(matrix)):
        for col in range(0, len(matrix)):
            r = "x" + str(row+1)
            c = "x" + str(col+1)

            Q[(r, c)] = matrix[row, col]
    
    #print_dwave_matrix(Q)
    return Q

def get_quantum_simulating_machine():

    dwave_token = "DEV-fc0d4fb3d4e5b9480999692a1cba611f0eb7c7e7"
    os.environ['DWAVE_API_TOKEN'] = dwave_token
# Create a QUBO problem


# Set up the D-Wave sampler (use a quantum system or simulator)
    sampler = EmbeddingComposite(DWaveSampler())



    return sampler

def print_magic_square(m):
    print(m)

    print("Printing matrix:")
    print("   ", end="")
    for col in range(0, len(m)):
        print(str(col+1), end=" ")
    print()


    index = 1
    for row in range(0, len(m)):
        print(index, end=" ")
        for col in range(0, len(m)):
            print(int(col), end=" ")
        print()

        index+=1
    print()
    print("#########################")
    print()


#magic square here has n * n integers in range [1, n*n]
def unit_tests(magic_square, m):
    row_errors = 0
    print("m:", m)

    print("----- All Rows = m -----")
    for r in range(0, len(magic_square)):
        row_sum = 0
        for c in range(0, len(magic_square)):
            row_sum += magic_square[r][c]
        if (row_sum != m):
            row_errors += 1
    
    print("----")
    print("Errors:", row_errors)
    print("#############")

def print_dwave_solution(solution, n_squared):

    n = int(n_squared ** (1/2))

    m = int( (n * (n_squared+1)) / 2)

    print("Solution:")
    for var, value in solution.items():
        print(f"Variable {var} = {value}")

    print("_________________________")

    ordered = {}
    for var, value in solution.items():
        ordered[var] = value
    
    

    magic_square = [[None] * n for i in range(n)]
    row_index = 0
    col_index = 0

    s = 0


    for i in range(1, len(solution.items()) + 1):
        #print("in pretty print")
        key = 'x' + str(i)
        print(ordered[key], ",", end="")
        s+= int(ordered[key])

        if (i % int(n_squared) == 0):
            print("   Sum == ", s)
            magic_square[row_index][col_index] = s

            s = 0

            col_index += 1
            if (col_index >= n):
                col_index = 0
                row_index+=1

    print("|||||||||||||||||||||||||")
    print_magic_square(magic_square)
    unit_tests(magic_square, m)
    
            
    





