import pandas as pd
from sklearn.model_selection import train_test_split
import os

# Define the relative path to the dataset
file_dir = os.path.dirname(__file__)  # Directory of the current Python file
txt_path = os.path.join(file_dir, '..', '..', 'Datasets', 'csv', 'winequality-red.csv')  # Go up and locate Datasets

# Loading data
data = pd.read_csv(txt_path, sep=';')

# Display the first few rows of the dataset
print(data.tail())
# Display more information about the dataset
print(data.describe())
print(data.info())

# # Separate features and labels
# X = data.iloc[:, :-1]   # All columns except the last one
# y = data.iloc[:, -1]    # The last column is the label

# # Split the data (80% train, 20% test)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Combine X and y back together for saving
# train_data = pd.concat([X_train, y_train], axis=1)
# test_data = pd.concat([X_test, y_test], axis=1)

# train_path = os.path.join(file_dir, '..', '..', 'Datasets', 'csv', 'banknote_train.csv') 
# test_path = os.path.join(file_dir, '..', '..', 'Datasets', 'csv', 'banknote_test.csv') 

# # Save to separate files
# train_data.to_csv(train_path, index=False, header=False)
# test_data.to_csv(test_path, index=False, header=False)

# print("Training and testing data have been saved.")
