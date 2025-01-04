
from dwave.system import DWaveSampler, EmbeddingComposite, LeapHybridSampler
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
    #sampler = EmbeddingComposite(DWaveSampler())
    sampler = LeapHybridSampler()

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
            print(m[row][col], end=" ")
        print()

        index+=1
    print()
    print("#########################")
    print()


#magic square here has n * n integers in range [1, n*n]
def unit_tests(magic_square, m, constraints_added):

    test_rows = constraints_added[0]
    test_cols = constraints_added[1]
    test_diagonals = constraints_added[2]
    test_all_different = constraints_added[3]



    total_errors = 0
    total_tests = 0
    n = len(magic_square)

    print("m:", m)
    print("n:", n)
    print("n**2:", n**2)
    print("n**4:", n**4)

    if (test_rows):
        total_tests += n
        row_errors = 0
        print("----- All Rows = m -----")
        for r in range(0, len(magic_square)):
            row_sum = 0
            for c in range(0, len(magic_square)):
                row_sum += magic_square[r][c]

            print("if (",row_sum," != ", m,")")
            if (row_sum != m):
                row_errors += 1

        total_errors +=  row_errors
        print("----")
        print("Errors:", row_errors)
        print("#############")
    
    
    if (test_cols):
        total_tests += n
        col_errors = 0
        print("----- All Columns = m -----")
        for c in range(0, len(magic_square)):
            col_sum = 0
            for r in range(0, len(magic_square)):
                col_sum += magic_square[r][c]

            print("if (",col_sum," != ", m,")")
            if (col_sum != m):
                col_errors += 1

        total_errors +=  col_errors
        print("----")
        print("Errors:", col_errors)
        print("#############")

    if (test_diagonals):
        total_tests += 2
        diag_errors = 0
        print("----- Both diagonals = m -----")
        ltr_sum = 0
        rtl_sum = 0

        for d in range(0, len(magic_square)):
                ltr_sum += magic_square[d][d]
                rtl_sum += magic_square[d][n - 1 - d]

        print("if (",ltr_sum," != ", m,")")
        if (ltr_sum != m):
            diag_errors += 1
        print("if (",rtl_sum," != ", m,")")
        if (rtl_sum != m):
            diag_errors += 1

        total_errors +=  diag_errors
        print("----")
        print("diag_errors:", diag_errors)
        print("#############")

    if(test_all_different):
        total_tests += 1
        print("----- All different -----")
        correct_sum = 0
        ms_sum = 0
        for r in range(0, n):
            for c in range(0, n):
                ms_sum += magic_square[r][c]
                correct_sum += (r*n) + c +1
        
        #should be 0
        regular_difference = correct_sum - ms_sum
        print("correct_sum:", correct_sum)
        print("ms_sum:", ms_sum)
        print("regular_difference:", regular_difference)

        squared_correct_sum = 0
        squared_ms_sum = 0
        for r in range(0, n):
            for c in range(0, n):
                squared_ms_sum += (magic_square[r][c])**2
                squared_correct_sum += ((r*n) + c + 1)**2

        squared_difference = squared_correct_sum - squared_ms_sum
        
        print()
        print("squared_correct_sum:", squared_correct_sum)
        print("squared_ms_sum:", squared_ms_sum)
        print("squared_difference:", squared_difference)

        #if magic square contains [1 .. n**2]
        #both should be zero
        print("if (",regular_difference," != ", 0,")")
        print("or")
        print("if (",squared_difference," != ", 0,")")
        
        if ((regular_difference != 0) or (squared_difference != 0)):
            total_errors += 1
            print("Not all different")
            
        print("#######################")
    
    print("*************")
    print("Constraints satisfied: ", total_tests - total_errors, "/", total_tests)
    print("Success ratio: ", str((((total_tests - total_errors) / total_tests) * 100)) + "%")




def print_dwave_solution(solution, n_squared, constraints_added):

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
            print(f"   Variable {i/int(n_squared)} == ", s)
            magic_square[row_index][col_index] = s

            s = 0

            col_index += 1
            if (col_index >= n):
                col_index = 0
                row_index+=1

    print("|||||||||||||||||||||||||")
    print_magic_square(magic_square)
    unit_tests(magic_square, m, constraints_added)
    
            
    





