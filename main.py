import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("spam.csv", encoding='latin-1')

# Keep only required columns
data = data[['v1', 'v2']]

# Rename columns
data.columns = ['label', 'message']

# Convert labels to numbers
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# Convert text to numbers (TF-IDF)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['message'])
y = data['label']

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create and train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Check accuracy
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# 🔥 Test with your own message
while True:
    user_input = input("\nEnter a message (or type 'exit'): ")

    if user_input.lower() == "exit":
        break

    # Transform input
    input_data = vectorizer.transform([user_input])

    # Predict
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        print("⚠ This is a SPAM message")
    else:
        print("✅ This is NOT spam")