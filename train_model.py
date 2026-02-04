import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import GridSearchCV
from joblib import dump
import argparse
import os
import json


def train_random_forest(train_path, test_path, out_model_path, out_metrics_path):
    # 1. Load datasets
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)

    # 2. Split X/Y (target = dernière colonne)
    X_train = df_train.iloc[:, :-1]
    y_train = df_train.iloc[:, -1]

    X_test = df_test.iloc[:, :-1]
    y_test = df_test.iloc[:, -1]

    # 3. Define model + hyperparameter search
    rf = RandomForestClassifier(
        random_state=42,
        class_weight="balanced",  # utile si classes déséquilibrées
        n_jobs=-1
    )

    param_grid = {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4]
    }

    grid = GridSearchCV(
        rf,
        param_grid,
        scoring="f1",
        cv=5,
        n_jobs=-1,
        verbose=1
    )

    grid.fit(X_train, y_train)
    best_model = grid.best_estimator_

    print("✅ Best parameters:", grid.best_params_)

    # 4. Evaluate model
    y_pred = best_model.predict(X_test)
    f1 = f1_score(y_test, y_pred)

    print("📊 Test F1-score:", f1)
    print("\nClassification report:\n", classification_report(y_test, y_pred))

    # 5. Save model
    os.makedirs(os.path.dirname(out_model_path), exist_ok=True)
    dump(best_model, out_model_path)

    # 6. Save metrics JSON (compatible avec ton pipeline)
    os.makedirs(os.path.dirname(out_metrics_path), exist_ok=True)
    metrics = {
        "f1": float(f1)
    }

    with open(out_metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"📁 Model saved to {out_model_path}")
    print(f"📁 Metrics saved to {out_metrics_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/train.csv")
    parser.add_argument("--test", default="data/test.csv")
    parser.add_argument("--out-model", default="models/candidate/model.joblib")
    parser.add_argument("--out-metrics", default="models/candidate/metrics.json")
    args = parser.parse_args()

    train_random_forest(args.train, args.test, args.out_model, args.out_metrics)
