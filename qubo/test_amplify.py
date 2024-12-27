from amplify import BinaryMatrix, Solver
from amplify import BinaryPoly
from objective_function import configure_client

# Initialize the Fixstars Amplify client
client = configure_client()

# Define a binary variable for the optimization problem
# Define a binary matrix of size 3x3
binary_matrix = BinaryPoly('x', shape=(3, 3))

# Print the binary matrix variables (this is just symbolic, not actual matrix values)
print(binary_matrix)