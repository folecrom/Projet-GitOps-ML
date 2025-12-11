import json
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--candidate")
parser.add_argument("--production")
args = parser.parse_args()

candidate_path = args.candidate
production_path = args.production

# Helper pour créer un fichier metrics.json minimal
def create_default_metrics(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"f1": 0.0}, f, indent=2)
    print(f"Created default metrics file at {path}")


# 🔹 1) Vérifier fichier candidat
if not os.path.exists(candidate_path):
    print("⚠ Aucun modèle candidat trouvé — création automatique.")
    create_default_metrics(candidate_path)

# Charger les métriques candidat
with open(candidate_path) as f:
    cand = json.load(f)

cand_score = cand.get("f1", 0.0)


# 🔹 2) Vérifier fichier production
if not os.path.exists(production_path):
    print("⚠ Aucun modèle production trouvé — création automatique.")
    create_default_metrics(production_path)

# Charger métriques production
with open(production_path) as f:
    prod = json.load(f)

prod_score = prod.get("f1", 0.0)


# 🔹 3) Comparaison
print(f"Candidat: {cand_score}, Production: {prod_score}")
is_better = cand_score > prod_score
print("Promote:", is_better)


# 🔹 4) Output pour GitHub Actions
with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    fh.write(f"promote={str(is_better).lower()}\n")
