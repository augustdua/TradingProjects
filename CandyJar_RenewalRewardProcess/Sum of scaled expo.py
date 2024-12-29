import numpy as np
import sys

def calculate_mean_Y(a, b, lambda_param, n_simulations):
    # Generate exponential random variables
    X = np.random.poisson(a * lambda_param, size=n_simulations)

    # Apply the transformation to get Y
    Y = np.floor(X / b)

    # Calculate the sample mean of Y
    mean_Y = np.mean(Y)

    return mean_Y

calculate_mean_Y(12,2,0.2,100000)

if __name__ == "__main__":
    # Convert command line arguments to the appropriate types
    a = float(sys.argv[1])
    b = float(sys.argv[2])
    lambda_param = float(sys.argv[3])
    n_simulations = int(sys.argv[4])

    # Call the function and print the result
    result = calculate_mean_Y(a, b, lambda_param, n_simulations)
    print(result)

