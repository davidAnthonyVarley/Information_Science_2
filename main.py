from constraint_programming.constraint_programming import run_constraint_programming_model
import time

inputs = [ 2,4,8,16,32, 64, 128]#[i for i in range(10)]
start_times = [-1] * len(inputs)
end_times = [-1] * len(inputs)




#-----------------------------------
for i in range(0, len(inputs)):
    start = time.time()
    start_times[i] = start
    run_constraint_programming_model(inputs[i])
    end = time.time()
    end_times[i] = end

    elapsed_time =  end_times[i] - start_times[i]
    print(f"n = {inputs[i]}")
    print(f"Runtime: {elapsed_time} seconds")
    print()

#-----------------------------------
