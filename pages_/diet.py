import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from model import get_diet, get_precautions, get_description

DISEASES = [
    "Fungal infection", "Allergy", "GERD", "Chronic cholestasis", "Drug Reaction",
    "Peptic ulcer diseae", "AIDS", "Diabetes", "Gastroenteritis", "Bronchial Asthma",
    "Hypertension", "Migraine", "Cervical spondylosis", "Paralysis (brain hemorrhage)",
    "Jaundice", "Malaria", "Chicken pox", "Dengue", "Typhoid", "hepatitis A",
    "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E", "Alcoholic hepatitis",
    "Tuberculosis", "Common Cold", "Pneumonia", "Dimorphic hemmorhoids(piles)",
    "Heart attack", "Varicose veins", "Hypothyroidism", "Hyperthyroidism",
    "Hypoglycemia", "Osteoarthristis", "Arthritis",
    "(vertigo) Paroymsal Positional Vertigo", "Acne", "Urinary tract infection",
    "Psoriasis", "Impetigo",
]

DISEASE_ICONS = {
    "Fungal infection": "🍄", "Allergy": "🤧", "Diabetes": "💉",
    "Hypertension": "❤️", "Migraine": "🧠", "Typhoid": "🤒", "Malaria": "🦟",
    "Dengue": "🌡️", "Jaundice": "😷", "Pneumonia": "🫁", "Common Cold": "🤧",
    "Heart attack": "💔", "Acne": "🧴", "Arthritis": "🦴", "Chicken pox": "🔴",
}

def show():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.diet-card { animation: fadeInUp 0.4s ease; }
</style>
""", unsafe_allow_html=True)

    if "diet_condition" not in st.session_state:
        st.session_state.diet_condition = None

    if st.session_state.get("prediction_result") and not st.session_state.diet_condition:
        if st.session_state.prediction_result in DISEASES:
            st.session_state.diet_condition = st.session_state.prediction_result

    st.markdown("""
<div style="background:linear-gradient(135deg,#0B7285 0%,#1aabbd 100%);
            border-radius:16px;padding:32px 36px;margin-bottom:24px;
            display:flex;align-items:center;gap:20px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:-30px;right:-30px;width:140px;height:140px;
              background:rgba(255,255,255,0.06);border-radius:50%;"></div>
  <div style="font-size:48px;">🥗</div>
  <div>
    <div style="font-size:22px;font-weight:700;color:#fff;">Diet Recommendation</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.75);margin-top:4px;">
      Personalised nutrition plans based on real medical data
    </div>
  </div>
  <div style="margin-left:auto;background:rgba(255,255,255,0.15);border-radius:12px;padding:12px 20px;text-align:center;">
    <div style="font-size:22px;font-weight:700;color:#fff;">41</div>
    <div style="font-size:10px;color:rgba(255,255,255,0.6);">Diet Plans</div>
  </div>
</div>
""", unsafe_allow_html=True)

    if st.session_state.get("prediction_result") and \
       st.session_state.diet_condition == st.session_state.prediction_result:
        st.markdown(
            f'<div style="background:#E1F5EE;border:1px solid #b2dfdb;border-radius:10px;'
            f'padding:10px 16px;margin-bottom:18px;font-size:12px;color:#0B7285;">'
            f'✨ Auto-filled from your recent prediction: <b>{st.session_state.prediction_result}</b></div>',
            unsafe_allow_html=True,
        )

    left_col, right_col = st.columns([1, 1.4], gap="large")

    with left_col:
        st.markdown('<div style="font-size:15px;font-weight:600;color:#1a1a1a;margin-bottom:12px;">🩺 Select a Condition</div>', unsafe_allow_html=True)

        search_cond = st.text_input("", placeholder="Search condition...", key="diet_search", label_visibility="collapsed")
        filtered_diseases = [d for d in DISEASES if search_cond.lower() in d.lower()] if search_cond else DISEASES

        for cond in filtered_diseases:
            icon = DISEASE_ICONS.get(cond, "🏥")
            is_selected = st.session_state.diet_condition == cond
            border = "2px solid #0B7285" if is_selected else "1px solid #eee"
            bg = "#E1F5EE" if is_selected else "#fff"
            st.markdown(
                f'<div style="background:{bg};border:{border};border-radius:12px;'
                f'padding:10px 14px;margin-bottom:6px;display:flex;align-items:center;gap:10px;">'
                f'<span style="font-size:20px;">{icon}</span>'
                f'<span style="font-size:13px;font-weight:600;color:#1a1a1a;">{cond}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button("View Plan" if not is_selected else "✓ Viewing", key=f"diet_cond_{cond}", use_container_width=True):
                st.session_state.diet_condition = cond
                st.rerun()

    with right_col:
        if st.session_state.diet_condition:
            cond = st.session_state.diet_condition
            diet_items = get_diet(cond)
            icon = DISEASE_ICONS.get(cond, "🏥")

            st.markdown(f"""
<div class="diet-card" style="display:flex;align-items:center;gap:14px;margin-bottom:18px;">
  <div style="font-size:36px;">{icon}</div>
  <div>
    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px;">Diet Plan for</div>
    <div style="font-size:20px;font-weight:700;color:#1a1a1a;">{cond}</div>
  </div>
</div>
""", unsafe_allow_html=True)

            pills = "".join(
                f'<span style="display:inline-flex;align-items:center;background:#E1F5EE;color:#0B7285;'
                f'border-radius:20px;padding:7px 14px;font-size:12px;font-weight:500;margin:4px 6px 4px 0;">'
                f'✅ {item}</span>'
                for item in diet_items
            )
            st.markdown(f"""
<div class="diet-card" style="background:#fff;border:1px solid #eee;border-radius:14px;padding:18px;margin-bottom:14px;
            box-shadow:0 2px 8px rgba(0,0,0,0.03);">
  <div style="font-size:13px;font-weight:700;color:#0B7285;margin-bottom:12px;">🥦 Recommended Foods</div>
  <div>{pills}</div>
</div>
""", unsafe_allow_html=True)

            st.markdown("""
<div style="background:#FFF9E6;border:1px solid #F7DC6F;border-radius:10px;padding:12px 14px;margin-top:8px;">
  <div style="font-size:11px;color:#856404;">
    ⚠️ <b>Disclaimer:</b> This diet plan is a general guideline. Please consult a registered
    dietitian or your doctor for a plan tailored to your specific medical needs.
  </div>
</div>
""", unsafe_allow_html=True)

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💊  View Medicines", use_container_width=True, key="diet_goto_med"):
                    st.session_state.page = "medicine"
                    st.rerun()
            with c2:
                if st.button("📥  Download Report", use_container_width=True, key="diet_goto_report"):
                    st.session_state.page = "report"
                    st.rerun()
        else:
            st.markdown("""
<div style="background:#f9f9f9;border:1px dashed #ddd;border-radius:16px;padding:48px 24px;text-align:center;">
  <div style="font-size:48px;margin-bottom:16px;">🥗</div>
  <div style="font-size:15px;font-weight:600;color:#888;">No Condition Selected</div>
  <div style="font-size:12px;color:#bbb;line-height:1.7;margin-top:8px;">
    Choose a condition from the left panel<br>to view your personalised diet plan.
  </div>
</div>
""", unsafe_allow_html=True)