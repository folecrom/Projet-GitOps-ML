import json
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--candidate")
parser.add_argument("--production")
args = parser.parse_args()

with open(args.candidate) as f:
    cand = json.load(f)

with open(args.production) as f:
    prod = json.load(f)

cand_score = cand["f1"]
prod_score = prod["f1"]

is_better = cand_score > prod_score

print(f"Candidat: {cand_score}, Production: {prod_score}")
print("Promote:", is_better)

# GitHub Actions moderne
with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    fh.write(f"promote={str(is_better).lower()}\n")
