from ortools.sat.python import cp_model

def get_rows(square):
    n = int(len(square) ** (1/2))
    rows = [([None] * n) for _ in range(n)]

    for row in range(0, n):
        #current_row_sum = 0

        #index in using row major order
        for col in range(0, n):
            index = (row*n) + col
            #print("Add variable "+ str(index) + " into row " + str(row))
            rows[row][col] = square[index]
            #current_row_sum += square[index]

        #row_sums[row] = current_row_sum

    '''print("Rows collected: ")
    for i in range(0, n):
        print(rows[i])'''

    return rows

def get_columns(square):
    n = int(len(square) ** (1/2))
    columns = [([None] * n) for _ in range(n)]

    for col in range(0, n):
        #current_row_sum = 0

        #index in using row major order
        for row in range(0, n):
            index = (col*n) + row
            #print("Add variable "+ str(index) + " into col " + str(col))
            columns[row][col] = square[index]
            #current_row_sum += square[index]

        #row_sums[row] = current_row_sum

    '''print("Columns collected: ")
    for i in range(0, n):
        print(columns[i])'''

    return columns

def get_diagonals(square):
    n = int(len(square) ** (1/2))
    diagonals = [([None] * n) for _ in range(2)]

    left_to_right_diagonal = diagonals[0]
    right_to_left_diagonal = diagonals[1]

    l_to_r_col_index = 0
    r_to_l_col_index = n - 1

    for row in range(0, n):
        #index in using row major order
        l_t_r = (row * n) + l_to_r_col_index
        r_t_l = (row * n) + r_to_l_col_index

        left_to_right_diagonal[row] = square[ l_t_r]
        right_to_left_diagonal[row] = square[r_t_l]

        l_to_r_col_index += 1
        r_to_l_col_index -= 1

        
    '''print("Diagonals collected: ")
    for i in range(0, n):
        print(left_to_right_diagonal[i], ",", end="")
    print()
    for i in range(0, n):
        print(right_to_left_diagonal[i], ",", end="")
    print()'''
    return [left_to_right_diagonal, right_to_left_diagonal]

def run_constraint_programming_model(n):
    # initiate, get n
    model = cp_model.CpModel()
    '''print()
    print("n =", n)
    print()'''
    n_squared = n*n
    m = int((n/2) * (n_squared +1)) #m = (𝑛/2) * (𝑛^2 +1) 

    square = [None] * (n_squared) #create variable vector

    #create variables, x1 to xn
    for i in range(0, n*n):
        label = "x" + str(i+1)
        square[i] = model.NewIntVar(1, n_squared, label)



    #CREATING CONSTRAINTS
    #print("#################")
    #print("Constraint: All vars are different")
    # add the all_different constraint
    model.AddAllDifferent(square)

    '''#print("m:", m)
    #print("if all vars = n*n:", n*n*n)
    model.Add(sum(square) == m)'''


    #print("#################")
    #print("Constraint: All rows are equal")
    #all rows have same value
    rows = get_rows(square)

    for i in range(0, len(rows) - 1):
        model.Add(sum(rows[i]) == m)


    #all columns are equal
    #print("#################")
    #print("Constraint: All cols are equal")

    columns = get_columns(square)

    for i in range(0, len(columns) - 1):
        model.Add(sum(columns[i]) == m)


    #print("#################")
    #print("Constraint: Both diagonals are equal")

    diagonals = get_diagonals(square)
    model.Add(sum(diagonals[0]) == m)
    model.Add(sum(diagonals[1]) == m)


    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    #print("m = ", m)
    #print("Declare decision variable values:")

    if status == cp_model.OPTIMAL:
        for i in range(0, n):
            row = square[i*n: (i+1) * n]
            #for c in row:
                #print(f"{c.Name()} = {solver.Value(c)}", ",", end="")
            #print()
    #else:
        #print("Not optimal decision:")
        #for var_proto in model.Proto().variables:
        #    #print(var_proto)
        #print("")
        #print("square: ", square)
        #print()


        '''for i in range(0, n):
            row = i * n
            for ii in range(row, row+n):
                print(f"{solver.Value(square[row + ii])}" + ",", end="")'''