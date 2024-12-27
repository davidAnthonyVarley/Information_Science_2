#create Q matrix of xQx
import numpy as np

def print_matrix(m):
    print("   ", end="")
    for col in range(0, len(m)):
        print(str(col+1), end=" ")
    print()


    index = 1
    for row in m:
        print(index,row)
        index+=1
    print()
    print("#########################")
    print()

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


    #so now, in upper triangular form
    print_matrix(matrix)
    return matrix







#create_Q_matrix(3)




#create_Q_matrix(4)
#create_Q_matrix(5)