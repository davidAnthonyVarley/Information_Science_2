print("#########################")
#from amplify import BinaryQuadraticModel, SymbolGenerator, Solver
from qubo_constraints import create_Q_matrix
from dwave_config import convert_matrix_for_dwave, get_quantum_simulating_machine
from dwave_config import print_dwave_solution

import time


def run_objective_function(m):


    print("Number of variables:", m)
    print("Using", m, "x", m, "unary encoding matrix")
    print("Creating Q", m*m, "x", m*m, "matrix")
    print()
    coefficient_matrix, constraints_added = create_Q_matrix(m)

    print("Converting Q unary matrix for dwave")
    Q = convert_matrix_for_dwave(coefficient_matrix)

    print("Getting quantum simulator")
    quantum_simulator = get_quantum_simulating_machine()
    print("Quantum simulator retrieved")
    #testing
    '''print("Testing that quanutm simulator still works")
    Q = {('x1', 'x1'): 1, ('x2', 'x2'): 1, ('x1', 'x2'): 2}
'''
    
    response = quantum_simulator.sample_qubo(Q)

    # Get and print the solution
    solution = response.first.sample
    print_dwave_solution(solution, n*n, constraints_added)


    #print("Solution:", solution)


#n = 2
n = int(input("Enter n:"))
start = time.time()
run_objective_function(n)
end = time.time()

print(f"Time elasped for n = {n}:")
print(end-start, "seconds")

print("#########################")
