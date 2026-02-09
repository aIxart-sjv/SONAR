from sklearn.ensemble import IsolationForest
import joblib

def train_model(X):
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    model.fit(X)
    return model

def predict_anomalies(model, X):
    scores = model.decision_function(X)
    predictions = model.predict(X)
    return scores, predictions

def save_model(model, path="models/iso_model.pkl"):
    joblib.dump(model, path)