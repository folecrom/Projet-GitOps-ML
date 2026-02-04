# Projet-GitOps-ML

Ce projet implémente une plateforme **MLOps** complète basée sur les principes du **GitOps**. L'objectif est d'automatiser le cycle de vie d'un modèle de Machine Learning, de la gestion des données à la mise en production.

---

## Architecture du Projet

Le workflow repose sur trois piliers technologiques :

* **DVC (Data Version Control) :** Gère le versionnement des datasets et des modèles volumineux.
* **Google Cloud Storage (GCS) :** Sert de stockage distant (Remote Storage) pour les fichiers physiques.
* **GitHub Actions :** Orchestre le pipeline CI/CD (Entraînement, Évaluation, Promotion).

### Le Workflow GitOps
1. Un `push` sur la branche `main` déclenche le pipeline.
2. Le runner GitHub récupère les données depuis **GCS** via `dvc pull`.
3. Un nouveau modèle (**Candidat**) est entraîné via `train_model.py`.
4. Le modèle Candidat est comparé au modèle de **Production** actuel via `evaluate.py`.
5. Si les performances sont meilleures, le modèle est automatiquement promu (mise à jour des pointeurs `.dvc` et push vers GCS).

---

## Installation & Configuration

### 1. Prérequis
* Python 3.10+
* Un compte Google Cloud avec un Bucket GCS actif.
* DVC installé avec le support GCS : `pip install dvc dvc-gs`.

### 2. Configuration locale
Clonez le dépôt et installez les dépendances :
```bash
git clone [https://github.com/ton-username/Projet-GitOps-ML.git](https://github.com/ton-username/Projet-GitOps-ML.git)
cd Projet-GitOps-ML
pip install -r requirements.txt