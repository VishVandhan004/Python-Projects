import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

# Load your CSV
train_df = pd.read_csv(r'C:\Vish Projects\Python_Projects\SmartHealth\data\symptom_disease_train.csv')
test_df = pd.read_csv(r'C:\Vish Projects\Python_Projects\SmartHealth\data\symptom_disease_test.csv')
# Train the model
X_train = train_df['text']
y_train = train_df['label']
model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(X_train, y_train)

# Save as pickle
joblib.dump(model, "symptom_disease_model.pkl")
print("Model saved as symptom_disease_model.pkl")
