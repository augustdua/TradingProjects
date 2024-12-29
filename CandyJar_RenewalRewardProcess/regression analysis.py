import numpy as np
import pandas as pd
from scipy.stats import poisson
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline

# Generate data with random values for n, lambda, and b
def generate_data(num_samples):
    data = []
    np.random.seed(42)  # Ensure reproducibility

    for _ in range(num_samples):
        n = np.random.randint(10, 101)
        lambda_ = np.random.uniform(0.1, 3.5)  # Adjusted for smaller lambda values
        b = np.random.randint(1, 11)
        samples = poisson.rvs(mu=n * lambda_, size=1000)
        expected_value = np.mean(np.floor(samples / b))
        theoretical_value = n * lambda_ / b
        error = theoretical_value - expected_value
        data.append([n, lambda_, b, error])

    return pd.DataFrame(data, columns=['n', 'lambda', 'b', 'error'])

# Generate a dataset with 5000 samples
df = generate_data(5000)

# Prepare data for regression
X = df[['n', 'lambda', 'b']]
y = df['error']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create polynomial features
degree = 3  # Degree of polynomial features
poly_features = PolynomialFeatures(degree)
X_train_poly = poly_features.fit_transform(X_train)
X_test_poly = poly_features.transform(X_test)

# Train the model
model = LinearRegression()
model.fit(X_train_poly, y_train)

# Predict and evaluate
predictions = model.predict(X_test_poly)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Display the model's intercept and coefficients
print(f'Intercept: {model.intercept_}')
print('Coefficients:', model.coef_)

# Example prediction
n_new, lambda_new, b_new = 25, 1.2, 5
example_input = poly_features.transform([[n_new, lambda_new, b_new]])
error_predicted = model.predict(example_input)[0]
print(f'Predicted Error for n={n_new}, lambda={lambda_new}, b={b_new}: {error_predicted}')
