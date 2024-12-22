from constraint_programming import run_constraint_programming_model
import time

inputs = [100, 1000]#[i for i in range(10)]
start_times = [-1] * len(inputs)
end_times = [-1] * len(inputs)




#-----------------------------------
for i in range(0, len(inputs)):
    start_times[i] = time.time()
    run_constraint_programming_model(inputs[i])
    end_times[i] = time.time()

#-----------------------------------

for i in range(0, len(inputs)):
    elapsed_time =  end_times[i] - start_times[i]
    print(f"n = {inputs[i]}")
    print(f"Runtime: {elapsed_time} seconds")
    print()