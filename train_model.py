from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

data = pd.read_csv(Path(__file__).resolve().parent / "data" / "sms_dataset.csv").dropna()
X, y = data["message"].astype(str), data["label"].astype(str).str.lower()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.25, random_state=42, stratify=y)
model = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=12000)),
                  ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))])
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("SAMPLE SMS MODEL EVALUATION")
print(f"Rows: {len(data)} | Train: {len(X_train)} | Test: {len(X_test)}")
print(f"Accuracy : {accuracy_score(y_test,pred):.3f}")
print(f"Precision: {precision_score(y_test,pred,pos_label='spam',zero_division=0):.3f}")
print(f"Recall   : {recall_score(y_test,pred,pos_label='spam',zero_division=0):.3f}")
print(f"F1-score : {f1_score(y_test,pred,pos_label='spam',zero_division=0):.3f}")
print(classification_report(y_test,pred,zero_division=0))
print("Educational sample metrics are not a real-world security guarantee.")
