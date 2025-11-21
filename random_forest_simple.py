import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from joblib import dump
import os

# --- Chemins des fichiers ---
train_csv = "data/train.csv"  # remplace par ton fichier de training
test_csv = "data/test.csv"    # remplace par ton fichier de test
model_path = "models/model.joblib"

# --- Chargement des données ---
train = pd.read_csv(train_csv)
test = pd.read_csv(test_csv)

# On suppose que la dernière colonne est la cible
X_train = train.iloc[:, :-1]
y_train = train.iloc[:, -1]

X_test = test.iloc[:, :-1]
y_test = test.iloc[:, -1]

# --- Entraînement Random Forest ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Prédiction & évaluation ---
y_pred = model.predict(X_test)
f1 = f1_score(y_test, y_pred)

print("F1-score sur le jeu de test :", f1)

# --- Sauvegarde du modèle ---
os.makedirs(os.path.dirname(model_path), exist_ok=True)
dump(model, model_path)
print(f"Modèle sauvegardé dans {model_path}")
