import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---------------- STEP 1: LOAD + CLEAN DATA ----------------
df = pd.read_csv("span.csv", encoding="latin-1")

df = df.iloc[:, :2]   # keep only label + message
df.columns = ["label", "message"]
df = df.dropna()

df["label"] = df["label"].map({"ham": 0, "spam": 1})

# ---------------- STEP 2: SPLIT DATA ----------------
X_train, X_test, y_train, y_test = train_test_split(
    df["message"], df["label"], test_size=0.2, random_state=42
)

# ---------------- STEP 3: TEXT TO NUMBERS ----------------
vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True,
    max_features=5000
)

X_train_vec = vectorizer.fit_transform(X_train)

# ---------------- STEP 4: TRAIN MODEL ----------------
model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train_vec, y_train)

# ---------------- STEP 5: SAVE MODEL ----------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model trained successfully")