
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

def print_dwave_solution(solution, n_squared):

    print("Solution:")
    for var, value in solution.items():
        print(f"Variable {var} = {value}")

    print("_________________________")

    ordered = {}
    for var, value in solution.items():
        ordered[var] = value
    
    for i in range(1, len(solution.items())):
        key = 'x' + str(i)
        print(str(key), ",", ordered[key])

        if (i % n_squared == 0):
            print() 
    





