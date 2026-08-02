
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import ast
import os

# ── Load all datasets ────────────────────────────────────────────────────────
BASE = os.path.join(os.path.dirname(__file__), "Dataset")

training_df     = pd.read_csv(os.path.join(BASE, "Training.csv"))
medications_df  = pd.read_csv(os.path.join(BASE, "medications.csv"))
diets_df        = pd.read_csv(os.path.join(BASE, "diets.csv"))
precautions_df  = pd.read_csv(os.path.join(BASE, "precautions_df.csv"))
description_df  = pd.read_csv(os.path.join(BASE, "description.csv"))
severity_df     = pd.read_csv(os.path.join(BASE, "Symptom-severity.csv"))
workout_df      = pd.read_csv(os.path.join(BASE, "workout_df.csv"))

# ── Train ML Model ───────────────────────────────────────────────────────────
X = training_df.drop("prognosis", axis=1)
y = training_df["prognosis"]

SYMPTOMS = list(X.columns)   # all 132 symptom column names

le = LabelEncoder()
y_encoded = le.fit_transform(y)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y_encoded)

# ── Helper: parse string lists from CSV ──────────────────────────────────────
def parse_list(val):
    try:
        return ast.literal_eval(val)
    except Exception:
        return [str(val)]

# ── Lookup dictionaries ───────────────────────────────────────────────────────
medications_dict = {
    row["Disease"]: parse_list(row["Medication"])
    for _, row in medications_df.iterrows()
}

diets_dict = {
    row["Disease"]: parse_list(row["Diet"])
    for _, row in diets_df.iterrows()
}

description_dict = {
    row["Disease"]: row["Description"]
    for _, row in description_df.iterrows()
}

precautions_dict = {}
for _, row in precautions_df.iterrows():
    precs = [row.get(f"Precaution_{i}", "") for i in range(1, 5)]
    precautions_dict[row["Disease"]] = [p for p in precs if pd.notna(p) and str(p).strip()]

workout_dict = {}
for _, row in workout_df.iterrows():
    disease = row["disease"]
    workout_dict.setdefault(disease, []).append(row["workout"])

severity_dict = dict(zip(severity_df["Symptom"].str.strip(), severity_df["weight"]))

# ── Main prediction function ─────────────────────────────────────────────────
def predict_disease(selected_symptoms):
    """
    Takes a list of symptom strings,
    returns (disease_name, confidence_percent).
    """
    input_vector = [1 if s in selected_symptoms else 0 for s in SYMPTOMS]
    input_array = np.array(input_vector).reshape(1, -1)

    proba = model.predict_proba(input_array)[0]
    top_idx = np.argmax(proba)
    confidence = int(proba[top_idx] * 100)
    disease = le.inverse_transform([top_idx])[0]
    return disease, confidence

# ── Accessors ────────────────────────────────────────────────────────────────
def get_medications(disease):
    return medications_dict.get(disease, ["Consult a doctor for medication advice."])

def get_diet(disease):
    return diets_dict.get(disease, ["Maintain a balanced diet."])

def get_precautions(disease):
    return precautions_dict.get(disease, ["Consult a healthcare professional."])

def get_description(disease):
    return description_dict.get(disease, "")

def get_workout(disease):
    return workout_dict.get(disease, [])

def get_all_symptoms():
    return SYMPTOMS