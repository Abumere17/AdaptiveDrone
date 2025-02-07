"""
    Himadri Saha
    TrainModel2.py

    Script for training model using RandomForestClassifier() based on preloaded data.
    Used to predict users face during live phase
    This is the second interation for testing

    Adapted from:
    https://github.com/computervisioneng/emotion-recognition-python-scikit-learn-mediapipe/tree/main

    TODO:
    - Find places to make adjusetments 
    - Test to see if this works

"""

import pickle
import os
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
 
# File path
file_path = 'FaceDectetionModule\ScikitLearn\SetupData\SetupData.txt'
 
# 1. Ensure file exists and is not empty
if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' does not exist.")
    exit()
 
if os.stat(file_path).st_size == 0:
    print(f"Error: File '{file_path}' is empty.")
    exit()
 
# 2. Load dataset safely
try:
    data = np.loadtxt(file_path, delimiter=" ", encoding="utf-8-sig")
except ValueError:
    print("Error: Unable to parse the dataset. Ensure the file contains only numerical values.")
    exit()
 
# ✅ 3. Ensure data is not empty
if data.size == 0:
    print("Error: The dataset contains no valid data.")
    exit()
 
# ✅ 4. Ensure data is 2D
if data.ndim == 1:
    data = data.reshape(-1, 1)
 
# ✅ 5. Ensure we have at least two columns (features + labels)
if data.shape[1] < 2:
    print("Error: Dataset must have at least one feature and one label.")
    exit()
 
# Split into features (X) and labels (y)
X = data[:, :-1]  # Features (all columns except last)
y = data[:, -1]   # Labels (last column)
 
# ✅ 6. Check class distribution
class_counts = Counter(y)
print("Class distribution:", class_counts)
 
# ✅ 7. Ensure no class has fewer than 2 samples when using stratification
if any(count < 2 for count in class_counts.values()):
    print("⚠️ Warning: At least one class has fewer than 2 samples. Disabling stratification.")
    stratify_option = None
else:
    stratify_option = y  # Enable stratification only if valid
 
# ✅ 8. Split data safely
try:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=True, stratify=stratify_option
    )
except ValueError as e:
    print(f"Error during train-test split: {e}")
    exit()
 
# ✅ 9. Initialize and train the Random Forest model
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)
 
# ✅ 10. Make predictions
y_pred = rf_classifier.predict(X_test)
 
# ✅ 11. Evaluate performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
 
# ✅ 12. Save trained model
model_path = 'trained_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(rf_classifier, f)
 
print(f"✅ Model saved as {model_path}")