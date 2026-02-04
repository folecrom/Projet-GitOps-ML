import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from joblib import dump
import argparse
import os
import json


def train_random_forest(train_path, test_path, out_model_path):
    # 1. Load datasets (CSV)
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)

    # 2. Split X/Y (target = dernière colonne)
    X_train = df_train.iloc[:, :-1]
    y_train = df_train.iloc[:, -1]

    X_test = df_test.iloc[:, :-1]
    y_test = df_test.iloc[:, -1]
    # 3. Train RandomForestClassifier
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=None,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 4. Evaluate model (F1-score)
    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred)

    # 5. Save model
    os.makedirs(os.path.dirname(out_model_path), exist_ok=True)
    dump(model, out_model_path)

    # 6. Save result JSON (utile pour le pipeline)
    result = {
        "model_path": out_model_path,
        "metric": "f1",
        "value": float(f1)
    }

    with open("train_result.json", "w") as f:
        json.dump(result, f, indent=2)

    print("Model trained!")
    print("F1-score:", f1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/train.csv")
    parser.add_argument("--test", default="data/test.csv")
    parser.add_argument("--out", default="models/model.joblib")
    args = parser.parse_args()

    train_random_forest(args.train, args.test, args.out)