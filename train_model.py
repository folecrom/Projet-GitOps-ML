import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from joblib import dump
import argparse
import os
import json


def train_random_forest(train_path, test_path, out_model_path):
    # 1️⃣ Charger les datasets (CSV)
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)

    # 2️⃣ Séparer X/Y (target = dernière colonne)
    X_train = df_train.iloc[:, :-1]
    y_train = df_train.iloc[:, -1]

    X_test = df_test.iloc[:, :-1]
    y_test = df_test.iloc[:, -1]

    # 3️⃣ Entraîner le RandomForestClassifier
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=None,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 4️⃣ Évaluer le modèle (F1-score)
    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred)

    # 5️⃣ Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(out_model_path), exist_ok=True)

    # 6️⃣ Sauvegarder le modèle
    dump(model, out_model_path)
    print(f"Model saved to {out_model_path}")

    # 7️⃣ Sauvegarder les métriques dans le même dossier
    metrics_path = os.path.join(os.path.dirname(out_model_path), "metrics.json")
    result = {
        "model_path": out_model_path,
        "metric": "f1",
        "value": float(f1)
    }
    with open(metrics_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Metrics saved to {metrics_path}")

    print("Model trained!")
    print("F1-score:", f1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/train.csv", help="Chemin du fichier train.csv")
    parser.add_argument("--test", default="data/test.csv", help="Chemin du fichier test.csv")
    parser.add_argument("--out", default="models/candidate/model.joblib", help="Chemin de sortie du modèle")
    args = parser.parse_args()

    train_random_forest(args.train, args.test, args.out)
