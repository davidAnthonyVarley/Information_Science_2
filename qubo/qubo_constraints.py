#create Q matrix of xQx
import numpy as np

def print_matrix(m):
    print("Printing matrix:")
    print("   ", end="")
    for col in range(0, len(m)):
        print(str(col+1), end=" ")
    print()


    index = 1
    for row in m:
        print(index, end=" ")
        for col in row:
            print(col, end=" ")
        print()

        index+=1
    print()
    print("#########################")
    print()

def add_all_different_constraint_mine(Q_unary, unary_matrix_num_rows):

    m = unary_matrix_num_rows #same as num of columns

    #firstly, every cell in the first column multiplied by
    # for i in 1 -> m for r in 1 -> m, Ui,j * (U r,c - Ur,c+1)

    #and vice versa,
    # for i in 1 -> m for r in 1 -> m, -Ui,j+1 * (U r,c - Ur,c+1)
    
    #go through all columns
    '''for j in range(0, m-1):

        first_col = j
        second_col = j+1

        for i in range(0, m):
            Q_row_index = (i * m) + first_col

            for r in range(0, m):
                #Ui,j * (U r,c - Ur,c+1)
                Q_first_col_index = (r * m) + first_col
                Q_second_col_index = (r * m) + second_col

                Q_unary[Q_row_index][Q_first_col_index] += 1
                Q_unary[Q_row_index][Q_second_col_index] -= 1
            
            for r in range(0, m):
                #-Ui,j+1 * (U r,c - Ur,c+1)
                Q_second_col_index = (r * m) + second_col
                Q_first_col_index = (r * m) + first_col

                Q_unary[Q_row_index][Q_second_col_index] += 1
                Q_unary[Q_row_index][Q_first_col_index] -= 1
'''
    
    #please god let this work
    for j in range(0, m-1):

        for i in range(j, m):
            row_index = (i*m) + i

            Q_unary[row_index, row_index] += 1

            for r in range(i+1, m, 2):
                print("At row", i, ",", "col", r)
                Q_unary[row_index][(r*m) + i] += 2
                #Q_unary[row_index][(r*m) + i +1] -= 2
        



def add_all_different_constraint_from_notes(Q_unary, unary_matrix_num_rows):
    #only works for the Q matrix for the unary encoding
    m = unary_matrix_num_rows #same as num of columns

    #print("m (in m x m unary matrix):", m)
    #print("q unary:", len(Q_unary), "x", len(Q_unary))

    #add diagonals
    for j in range(0, m):
        '''print("j:", j)'''
        penalty = 1
        coefficient = 2 * (j-m) * 3 * penalty
        print("Coefficient:", coefficient)

        for i in range(0, m):
            '''print("\ti:", i)'''
            #apply coefficient to seemingly every variable
            # x i,j corresponds to Q_unary[i*m + j, i*m + j]
            # a diagonal
            diagonal_index = (i*m) + j
            Q_unary[diagonal_index, diagonal_index] += coefficient
        
        #now separately
        print("________________")
        for i in range(0, m):
            '''print("\ti:", i)'''
            for k in range(i+1, m):
                '''print("\t\tk:", k)'''
                row = (i * m) + j
                col = (k * m) + j

                Q_unary[row, col] += 2

    return Q_unary


def apply_Q_old_cell_to_Q_unary(Q_old, row, col, Q_unary):
    m = len(Q_old)

    #this represents coefficient of x1 * x2,
    #where x is sum of row unary variables
    coefficient = Q_old[row][col]

    #will now apply this coefficient to appropriate coefficients
    #in m^2 by m^2 uunary encoding Q matri
    '''print("Applying Q_old", row+1, col+1, "to new Q unary matrix")
    print("Unary matrix is", m, "by", m)
    print("Q_unary matrix is", m*m, "by", m*m)
    print("Coefficient:", coefficient)
    print("------------------------")'''
    for i in range((row)*m, (row+1)*m ):
        for j in range(col*m, (col+1)*m ):
            Q_unary[i][j] += coefficient
            '''print("Adding coeff to Q_u", i+1, j+1)
    print()'''



def convert_to_unary_encoding(Q_old):
    m = len(Q_old)

    m_squared = m*m
    Q_unary = np.zeros((m_squared, m_squared), dtype=int)

    for row in range(0, m):
        for col in range(row, m):

            apply_Q_old_cell_to_Q_unary(Q_old, row, col, Q_unary)

    
    return Q_unary

            


def create_Q_matrix(n):
    #will return a list of rows, 2D matrix
    #matrix = [([0] * n) for _ in range(n)]
    n_squared = n*n
    matrix = np.zeros((n_squared, n_squared), dtype=int)

    #account for sums of rows
    barrier = n

    for row in range(0, n_squared):
        if (barrier <= row):
            barrier += n

        #print("barrier <= row: ", barrier, "<=", row)
        for col in range(row, barrier):

            if (row == col):
                matrix[row, col] += 1
            else:
                matrix[row, col] += 2
    
    #account for sums of columns

    for row in range(0, n_squared):

        for col in range(row, n_squared, n):

            if (row == col):
                matrix[row, col] += 1
            else:
                matrix[row, col] += 2

    #account for sum of left to right diagonal

    for row in range(0, n_squared, n+1):

        for col in range(row, n_squared, n+1):

            if (row == col):
                matrix[row, col] += 1
            else:
                matrix[row, col] += 2

    #account for sum of right to left diagonal
    
    for row in range(n-1, n_squared, n-1):

        for col in range(row, n_squared-1, n-1):

            if (row == col):
                matrix[row, col] += 1
            else:
                matrix[row, col] += 2


    #add objective function
    

    m = (n * (n*1)) / 2
    for d in range(0, len((matrix))):
        matrix[ d][ d] += -2*m



    #so now, in upper triangular form
    print("before unary and all diff")
    print_matrix(matrix)
    print()
    print()
    print()
    

    '''test_matrix = np.zeros((n_squared, n_squared), dtype=int)
    m = (n * (n*1)) / 2
    for d in range(0, len((test_matrix))):
        test_matrix[ d][ d] += -2*m
    q_unary = convert_to_unary_encoding(test_matrix)'''
    
    q_unary = convert_to_unary_encoding(matrix)
    add_all_different_constraint_from_notes(q_unary, n*n)

    print_matrix("after q unary and all diff")
    print_matrix(q_unary)
    print()
    print()
    print()

    #add_all_different_constraint_mine(q_unary, n*n)
    
    #print("after all different added")
    #print_matrix(q_unary)
    #print()
    #print()
    #print()
    return q_unary







#create_Q_matrix(2)
'''m = 2
#matrix = np.array([[1, 2], [0, 1]])
#q_old = np.zeros((m, m), dtype=int)

#the Q in xQx, for an unary encoding matrix
q_unary = create_Q_matrix(m)'''


'''print("unary encoding matrix")
print_matrix(np.zeros((m, m), dtype=int))
'''

'''print("q_unary")
    print_matrix(q_unary)'''
