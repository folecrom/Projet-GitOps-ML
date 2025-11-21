from sklearn.datasets import make_classification
import pandas as pd
import os

# Générer dataset de classification
X, y = make_classification(
    n_samples=1000,   # nombre d'exemples
    n_features=10,    # nombre de variables
    n_informative=5,
    n_redundant=2,
    n_classes=2,
    random_state=42
)

# Mettre les données dans un DataFrame
df = pd.DataFrame(X, columns=[f"feat_{i}" for i in range(X.shape[1])])
df['target'] = y

# Créer dossier data si nécessaire
os.makedirs("data", exist_ok=True)

# Split train/test (80% train, 20% test)
train_df = df.sample(frac=0.8, random_state=42)
test_df = df.drop(train_df.index)

# Sauvegarder en CSV
train_df.to_csv("data/train.csv", index=False)
test_df.to_csv("data/test.csv", index=False)

print("Fichiers train.csv et test.csv créés dans data/")
