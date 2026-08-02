# 🩺 MedCare AI — Healthcare Recommendation System

An ML-powered web app that predicts diseases from symptoms and provides personalised medicine, diet, and precaution recommendations.

<img width="946" height="491" alt="Screenshot 2026-08-02 212630" src="https://github.com/user-attachments/assets/c3e0fc01-0fe2-4c3c-a523-51eb43c1d62e" />

👉 **[Live Demo](https://your-app-link.streamlit.app)** &nbsp;|&nbsp; 📁 **[Dataset](github.com/somyashree09/MedCare-AI-Healthcare-Recommendation-System/tree/main/Dataset)**

---

## 📌 About the Project

MedCare AI helps users identify potential health conditions by selecting their symptoms. It then recommends medicines, diet plans, and precautions — all powered by a trained Random Forest model and real medical data.

Built as part of a **Personalised Recommendation System**

---

## ✨ Features

| Page | Description |
|------|-------------|
| 🩺 Disease Prediction | Select symptoms → get AI-predicted disease + confidence score |
| 💊 Medicine Recommendation | Condition-based medicine suggestions from real dataset |
| 🥗 Diet Recommendation | Personalised nutrition plans per condition |
| 📊 Dashboard | Interactive charts — weekly activity, health score gauge |
| 🕑 History | Timeline of all past predictions and activity |
| 📥 Download Report | One-click PDF report with full health summary |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)

- **ML Model:** Random Forest Classifier (~92% accuracy)
- **Dataset:** 4,920 samples · 132 symptoms · 41 diseases
- **PDF Generation:** ReportLab

---

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/somyashree09/HealthCare-Recommendation-System.git
cd HealthCare-Recommendation-System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 📂 Project Structure

```
HealthCare_Recommendation_System/
├── app.py              # Main entry point
├── model.py            # ML model + data accessors
├── requirements.txt
├── Dataset/            # CSV files (symptoms, medicines, diets, etc.)
├── pages_/             # Individual page modules
└── .streamlit/         # Theme config
```

---

## 📸 Screenshots


---<img width="451" height="243" alt="Screenshot 2026-08-02 212732" src="https://github.com/user-attachments/assets/3d0e6f38-c244-4e9d-a9de-1f903d8a7c57" />

<img width="779" height="386" alt="Screenshot 2026-08-02 212744" src="https://github.com/user-attachments/assets/0265c2c7-ffe0-4160-a297-c4cc65b507d7" />

<img width="935" height="500" alt="Screenshot 2026-08-02 212807" src="https://github.com/user-attachments/assets/ac75242d-a669-409f-93a6-af2d1e051a3f" />


## ⚠️ Disclaimer

This app is for **educational purposes only** and is not a substitute for professional medical advice.

---

<p align="center">Built with ❤️ by <b>Somyashree Nayak</b> · Gandhi Engineering College, Bhubaneswar</p>
