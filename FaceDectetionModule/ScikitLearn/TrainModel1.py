"""
TrainModel1.py - Train RandomForestClassifier for face emotion prediction.

Author: Himadri Saha

Updates:
- Ensures test_size is always at least 10 samples.
- Prevents stratification errors when dataset is too small.
- Uses dynamic test size calculation based on dataset size.

"""

# Imports 
import pickle
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

# Load data from the text file
data_file = 'FaceDectetionModule/ScikitLearn/SetupData/SetupData.txt'
data = np.loadtxt(data_file)

# Split data into features (X) and labels (y)
X = data[:, :-1]  # Features are all columns except the last one
y = data[:, -1]   # Labels are the last column

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Determine the test size dynamically
num_classes = len(np.unique(y))
min_test_samples = max(10, num_classes)  # Ensure at least 10 test samples
test_size = max(min_test_samples / len(y), 0.2)  # Ensure test_size is at least 10 samples

# Ensure test_size is between 10 samples and 20% of the dataset
test_size = min(0.2, max(test_size, min_test_samples / len(y)))  

# Perform stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42, stratify=y, shuffle=True
)

# Apply SMOTE only to the training set (not the test set)
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Define StratifiedKFold for better class balancing
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

# Hyperparameter tuning with GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],   # Number of trees
    'max_depth': [None, 10, 20, 30],   # Maximum depth
    'min_samples_split': [2, 5, 10]    # Minimum samples per split
}

grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=cv, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Get the best model
best_rf_classifier = grid_search.best_estimator_

# Train the best classifier
best_rf_classifier.fit(X_train, y_train)

# Make predictions
y_pred = best_rf_classifier.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"Improved Accuracy: {accuracy * 100:.2f}%")
print(confusion_matrix(y_test, y_pred))

# Save trained model
with open('FaceDectetionModule/ScikitLearn/model', 'wb') as f:
    pickle.dump(best_rf_classifier, f)

# Save the scaler (Needed for live prediction)
with open('FaceDectetionModule/ScikitLearn/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
