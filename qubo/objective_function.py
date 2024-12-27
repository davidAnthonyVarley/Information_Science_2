print("#########################")
#from amplify import BinaryQuadraticModel, SymbolGenerator, Solver
from qubo_constraints import create_Q_matrix
from test_dwave import convert_matrix_for_dwave, get_quantum_simulating_machine

def create_objective_function(n):

    coefficient_matrix = create_Q_matrix(n)
    Q = convert_matrix_for_dwave(coefficient_matrix)

    quantum_simulator = get_quantum_simulating_machine()

    #testing
    #Q = {('x1', 'x1'): 1, ('x2', 'x2'): 1, ('x1', 'x2'): 2}

    
    response = quantum_simulator.sample_qubo(Q)

    # Get and print the solution
    solution = response.first.sample
    print("Solution:", solution)



create_objective_function(3)

print("#########################")
