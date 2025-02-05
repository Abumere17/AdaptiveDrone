"""
    Himadri Saha
    TrainModel.py

    Script for training model using RandomForestClassifier() based on preloaded data.
    Used to predict users face during live phase

    Adapted from:
    https://github.com/computervisioneng/emotion-recognition-python-scikit-learn-mediapipe/tree/main

    TODO:
    - Find places to make adjusetments 
    - Test to see if this works

"""

# Imports 
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

# Load data from the text file
data_file = 'FaceDectetionModule\Scikit-learn\SetupData\SetupData.txt'
data = np.loadtxt(data_file)

# Split data into features (X) and labels (y)
X = data[:, :-1]  # Features are all columns except the last one
y = data[:, -1]   # Labels are the last column

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42,
                                                    shuffle=True,
                                                    stratify=y)

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier()

# Train the classifier on the training data
rf_classifier.fit(X_train, y_train)

# Make predictions on the test data
y_pred = rf_classifier.predict(X_test)

# Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print(confusion_matrix(y_test, y_pred))

with open('./model', 'wb') as f: # Verify path
    pickle.dump(rf_classifier, f)