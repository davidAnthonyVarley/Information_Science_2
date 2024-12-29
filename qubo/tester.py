n = 2
n_squared = n * n

matrix = [[0 for _ in range(n_squared)] for _ in range(n_squared)]

index = 1
'''for row in matrix:
    print(index, row)
    index += 1'''
#print(matrix)

for r in range (1, n+1):
    print("Summing vars", (r-1)*n, "to", ((r)*n) - 1)
    for i in range( (r-1)*n, r * n):
        print("\tSumming bools", (i)*n_squared, "to", ((i+1)*n_squared) -1 , "to make var", i)
        for j in range( (i-1)*n_squared, i*n_squared):
            var = 1