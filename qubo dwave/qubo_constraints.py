#create Q matrix of xQx
import numpy as np
import sympy as sp

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
            print(int(col), end=" ")
        print()

        index+=1
    print()
    print("#########################")
    print()

def print_str_matrix(m):
    print("Printing matrix:")

    for row in range(0, len(m)):
        for col in range(0, len(m)):
            print((m[row][col]), end=" ")
        print()

    print()
    print("#########################")
    print()


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



def place_variables_in_unary_matrix(unary_matrix):
    n_squared = len(unary_matrix)

    for row in range(0, n_squared):
        for col in range(0, n_squared):
            label = f"u{row+1},{col+1}"
            #print(label)
            unary_matrix[row][col] = label
            #print("matrix entrry: ", unary_matrix[row, col])
    
    return unary_matrix

def place_coefficient_in_Q_matrix(component, Q_unary, n):

    coefficient = 1.0
    unary_var_1 = ''
    unary_var_2 = ''

    if (component.count('u') == 1):
        #ie, if it is u11**2, change to just u11
        one_unary_var_and_coefficient = component.replace('**2', '')
        separated = one_unary_var_and_coefficient.split('*')

        if ( not ('u' in separated[0])):
            coefficient = float(separated[0])
            unary_var_1 = separated[1]
        else:
            unary_var_1 = separated[0]
        
        unary_var_2 = unary_var_1
        
        #now, unary var looks like ui,j
    else: #else is c*ua,b*ud,e
        
        separated = component.split('*')
        
        coefficient = float(separated[0])
        unary_var_1 = separated[1]
        unary_var_2 = separated[2]
    
    
    #print("component:", component)
    #print("coefficient:", coefficient)
    #print("unary_var_1:", unary_var_1)
    #print("unary_var_2:", unary_var_2)
    #print('-')


    # Remove 'u' and split the indices (i,j)
    unary_var_1 = unary_var_1.replace('u', '')
    #now juust "i,j"
    str_unary_var_1_indices = unary_var_1.split(',')

    unary_var_2 = unary_var_2.replace('u', '')
    #now juust "i,j"
    str_unary_var_2_indices = unary_var_2.split(',')

    unary_var_1_indices = [-1] * 2
    unary_var_2_indices = [-1] * 2

    #cast string indices to ints
    for i in range(0, len(str_unary_var_1_indices)):
        unary_var_1_indices[i] = int(str_unary_var_1_indices[i]) - 1
        unary_var_2_indices[i] = int(str_unary_var_2_indices[i]) - 1

    #print("unary_var_1_indices:", unary_var_1_indices)
    #print("unary_var_2_indices:", unary_var_2_indices)
    #print()

    Q_row = unary_var_1_indices[0]*(n**2) + (unary_var_1_indices[1])
    Q_col = unary_var_2_indices[0]*(n**2) + (unary_var_2_indices[1])

    '''Q_row = unary_var_1_indices[0]*(n) + unary_var_1_indices[1]
    Q_col = unary_var_2_indices[0]*(n) + unary_var_2_indices[1]'''

    '''print("Q row:", Q_row)
    print("Q col:", Q_col)
    print()'''

    #if below diagonal, don't add

    #if (Q_col < Q_row):
    Q_unary[Q_row, Q_col] += coefficient

def add_expression_to_Q_matrix(Q_unary, expression, n):
    print("Fully worked out expression:")
    print(expression)
    print("---")
    for arg in expression.args:
        component = str(arg)
        if ('u' in component):
            #ie, we dont care about constants, like m^2
            #we only care about ui,j ** 2 or 4ua,b * uc,d
            place_coefficient_in_Q_matrix(component, Q_unary, n)

def add_row_constraints(unary_symbols, Q_unary, m, n):

    for ms_row in range(0, n):
        first_num_in_row = (ms_row) * n
        last_num_in_row = (ms_row+1) * n

        #all the unary variables that make up the sum of the row in the magic sqaure
        row_in_magic_square = unary_symbols[first_num_in_row : last_num_in_row]

        #print(row_in_magic_square)

        #all unary vars in one (n^2 * n) length list
        flattened = [item for sublist in row_in_magic_square for item in sublist]

        sum_of_ms_row = sum(flattened)
        print("Sum_of_ms_row")
        print(sum_of_ms_row)
        print(".")

        penalty = sp.symbols('penalty')
        # Define an expression

        # Substitute p = 2 into the expression
        
        print()
        expression = penalty*((sum_of_ms_row - m)**2)
        expression = expression.subs(penalty, 1)

        simplified = sp.expand(expression)

        add_expression_to_Q_matrix(Q_unary, simplified, n)
                
def add_column_constraints(unary_symbols, Q_unary, m, n):

    for magic_square_column in range(0, n):

        #all the unary variables that make up the sum of the col in the magic sqaure
        col_in_magic_square = [[None for _ in range(n)] for _ in range(n)]

        for r in range(n):
            ms_var = [] * n**2
            for unary_var_index in range(0, n**2):
                ms_var.append(unary_symbols[(r * n) + magic_square_column][unary_var_index])
            
            col_in_magic_square[r] = ms_var

        #'flattened' represents
        #all unary vars in one (n^2 * n) length list, which are
        #representing a column in the n*n magic square
        flattened = [val for row in col_in_magic_square for val in row]

        sum_of_ms_col = sum(flattened)
        penalty = sp.symbols('penalty')
        
        expression = penalty*((sum_of_ms_col - m)**2)
        # substitute p = (any real num) into the expression
        expression = expression.subs(penalty, 1)

        simplified = sp.expand(expression)
        #print(f"Mathematical equation of ((sum of col {magic_square_column}) - m)^2")
        #print(simplified)

        for arg in simplified.args:
            component = str(arg)

            if ('u' in component):
                #ie, we dont care about constants, like m^2
                place_coefficient_in_Q_matrix(component, Q_unary, n)

def add_diagonal_constraints(unary_symbols, Q_unary, m, n):

    #ltr = left to right
    #rtl = right to left

    ltr = 0
    rtl = (n - 1)

    ltr_increment = n+1
    rtl_increment = n-1

    ltr_diagonal = [[None for _ in range(n)] for _ in range(n)]
    rtl_diagonal = [[None for _ in range(n)] for _ in range(n)]


    #all the unary variables that make up the sum of the diagonals in the magic sqaure
    for r in range(n):
        ltr_var = [] * n**2
        rtl_var = [] * n**2
        for unary_var_index in range(0, n**2):
            ltr_var.append(unary_symbols[ltr][unary_var_index])
            rtl_var.append(unary_symbols[rtl][unary_var_index])
        
        ltr_diagonal[r] = ltr_var
        rtl_diagonal[r] = rtl_var

        ltr += ltr_increment
        rtl += rtl_increment
    
    #'flattened' represents
    #all unary vars in one (n^2 * n) length list, which are
    #representing a column in the n*n magic square
    ltr_flattened = [val for row in ltr_diagonal for val in row]
    rtl_flattened = [val for row in rtl_diagonal for val in row]
    
    print("ltr_flattened:")
    print(ltr_flattened)
    print("rtl_flattened:")
    print(rtl_flattened)
    
    sum_of_ltr_diag = sum(ltr_flattened)
    sum_of_rtl_diag = sum(rtl_flattened)
    penalty = sp.symbols('penalty')
    
    ltr_expression = penalty*((sum_of_ltr_diag - m)**2)
    rtl_expression = penalty*((sum_of_rtl_diag - m)**2)
    # substitute p = (any real num) into the expression
    ltr_expression = ltr_expression.subs(penalty, 1)
    rtl_expression = rtl_expression.subs(penalty, 1)
    
    ltr_simplified = sp.expand(ltr_expression)
    rtl_simplified = sp.expand(rtl_expression)
    #print(f"Mathematical equation of ((sum of col {magic_square_column}) - m)^2")
    #print(simplified)
    add_expression_to_Q_matrix(Q_unary, ltr_simplified, n)
    add_expression_to_Q_matrix(Q_unary, rtl_simplified, n)

def second_all_diff_constraint(unary_symbols, Q_unary, m, n):
    for c in range(0, (n**2) - 1):
        first_unary_col = [None for _ in range(n**2)]
        second_unary_col = [None for _ in range(n**2)]
        for r in range(0, n**2):
            first_unary_col[r] = unary_symbols[r][c]
            second_unary_col[r] = unary_symbols[r][c+1]
        
        expression = 2 * (( sum(first_unary_col) - sum(second_unary_col) - 1 )**2)

        # substitute p = (any real num) into the expression
        #penalty.subs(penalty, 1)
        #expression = penalty*expression
        
        simplified = sp.expand(expression)
        add_expression_to_Q_matrix(Q_unary, simplified, n)

def add_all_different_constraint(unary_symbols, Q_unary, m, n):
    
    
    # -0, -0 doesn't work
    # -0, -1 doesn't work
    # -0, -2 doesn't work
    # -1, -0 doesn't work
    # -1, -1 doesn't work   very close though
    # -1, -2 doesn't work
    # -2, -0 doesn't work
    # -2, -1 doesn't work
    # -2, -2 doesn't work

    #\2, -1, like in notes, is the only one that works, sometimes
    
    

    for c in range(0, (n**2)):
        unary_col = [None for _ in range(n**2)]
        for r in range(0, n**2):
            unary_col[r] = unary_symbols[r][c]
        
        #now, all unary variables in column c in unary_col

        penalty = sp.symbols('penalty')
        #print("unary_col:", unary_col)
        expression = (( sum(unary_col)  - (n**2  - (c) ) )**2)

        # substitute p = (any real num) into the expression
        #penalty.subs(penalty, 1)
        #expression = penalty*expression
        
        simplified = sp.expand(expression)
        add_expression_to_Q_matrix(Q_unary, simplified, n)


def add_all_constraints(unary_symbols, Q_unary, m, n):
    #for testing purposes, i only want to try one constraint at a time

    constrain_rows = True
    #constrain_rows = False
    constrain_columns = True
    #constrain_columns = False
    constrain_diagonals = True
    #constrain_diagonals = False

    #all_different = True
    all_different = False
    
    if (constrain_rows): 
        add_row_constraints(unary_symbols, Q_unary, m, n)
    if (constrain_columns):
        add_column_constraints(unary_symbols, Q_unary, m, n)
    if (constrain_diagonals):
        add_diagonal_constraints(unary_symbols, Q_unary, m, n)
    if (all_different):
        add_all_different_constraint_from_notes(Q_unary, n*n)
        #add_all_different_constraint(unary_symbols, Q_unary, m, n)
    
    constraints_added = [constrain_rows, constrain_columns, constrain_diagonals, all_different]

    return constraints_added


def create_Q_matrix(n):
    #will return a list of rows, 2D matrix
    #matrix = [([0] * n) for _ in range(n)]
    n_squared = n*n
    m = int((n * (n_squared+1) / 2))

    print("m:", m)
    print("n:", n)
    print("n**2:", n**2)
    print("n**4:", n**4)


    unary_matrix = [[None] * n_squared for i in range(n_squared)]
    Q_unary = np.zeros((n**4, n**4), dtype=float)

    place_variables_in_unary_matrix(unary_matrix)

    # Print the result to verify
    #print_str_matrix(unary_matrix)

    #for algebra
    unary_symbols = [[sp.Symbol(cell) for cell in row] for row in unary_matrix]

    #add constraints
    constraints_added = add_all_constraints(unary_symbols, Q_unary, m, n)
    
    print_matrix(Q_unary)

    return Q_unary, constraints_added

    









#create_Q_matrix(2)
'''n = 2
#matrix = np.array([[1, 2], [0, 1]])
#q_old = np.zeros((m, m), dtype=int)

#the Q in xQx, for an unary encoding matrix
q_unary = create_Q_matrix(n)'''


'''print("unary encoding matrix")
print_matrix(np.zeros((m, m), dtype=int))
'''

'''print("q_unary")
    print_matrix(q_unary)'''
