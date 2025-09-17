import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

ds = pd.read_csv('/workspaces/AI-Health-Bot-Medical-NFTs-on-Aptos-/dataset/dataset10.csv')
df = ds.head(10000)
train=df.drop('diseases', axis=1)

x_train, x_test, y_train, y_test = train_test_split(train, df['diseases'], test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(x_train, y_train)

with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Load model
with open('model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Predict using loaded model
predictions = loaded_model.predict(x_test)
print(predictions)

acc = accuracy_score(y_test,predictions)
print(acc)