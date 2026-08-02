import streamlit as st
import time
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from model import get_medications, get_precautions, get_description

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
    "Fungal infection": "🍄", "Allergy": "🤧", "GERD": "🔥", "Diabetes": "💉",
    "Hypertension": "❤️", "Migraine": "🧠", "Typhoid": "🤒", "Malaria": "🦟",
    "Dengue": "🌡️", "Jaundice": "😷", "Pneumonia": "🫁", "Common Cold": "🤧",
    "Tuberculosis": "🫁", "Heart attack": "💔", "Acne": "🧴",
    "Urinary tract infection": "🔬", "Psoriasis": "🩹", "Arthritis": "🦴",
    "Chicken pox": "🔴", "AIDS": "🎗️",
}

def show():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
</style>
""", unsafe_allow_html=True)

    if "my_medicine_list" not in st.session_state:
        st.session_state.my_medicine_list = []
    if "selected_condition" not in st.session_state:
        st.session_state.selected_condition = None

    if st.session_state.get("prediction_result") and not st.session_state.selected_condition:
        if st.session_state.prediction_result in DISEASES:
            st.session_state.selected_condition = st.session_state.prediction_result

    # ── HEADER ────────────────────────────────────────────────────────────
    st.markdown("""
<div style="background:linear-gradient(135deg,#0B7285 0%,#1aabbd 100%);
            border-radius:16px;padding:32px 36px;margin-bottom:24px;
            display:flex;align-items:center;gap:20px;">
  <div style="font-size:48px;">💊</div>
  <div>
    <div style="font-size:22px;font-weight:700;color:#fff;">Medicine Recommendation</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.75);margin-top:4px;">
      Select a condition to get personalised medicine suggestions
    </div>
  </div>
  <div style="margin-left:auto;background:rgba(255,255,255,0.15);border-radius:12px;padding:12px 20px;text-align:center;">
    <div style="font-size:22px;font-weight:700;color:#fff;">41</div>
    <div style="font-size:10px;color:rgba(255,255,255,0.6);">Conditions</div>
  </div>
</div>
""", unsafe_allow_html=True)

    if st.session_state.get("prediction_result") and \
       st.session_state.selected_condition == st.session_state.prediction_result:
        st.markdown(
            f'<div style="background:#E1F5EE;border:1px solid #b2dfdb;border-radius:10px;'
            f'padding:10px 16px;margin-bottom:18px;font-size:12px;color:#0B7285;">'
            f'✨ Auto-filled from your recent prediction: <b>{st.session_state.prediction_result}</b></div>',
            unsafe_allow_html=True,
        )

    left_col, right_col = st.columns([1, 1.3], gap="large")

    with left_col:
        st.markdown('<div style="font-size:15px;font-weight:600;color:#1a1a1a;margin-bottom:12px;">Select a Condition</div>', unsafe_allow_html=True)

        search_cond = st.text_input("", placeholder="Search condition...", key="med_search", label_visibility="collapsed")
        filtered_diseases = [d for d in DISEASES if search_cond.lower() in d.lower()] if search_cond else DISEASES

        for cond in filtered_diseases:
            icon = DISEASE_ICONS.get(cond, "🏥")
            is_selected = st.session_state.selected_condition == cond
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
            if st.button("View" if not is_selected else "✓ Viewing", key=f"med_cond_{cond}", use_container_width=True):
                st.session_state.selected_condition = cond
                st.rerun()

        if st.session_state.my_medicine_list:
            st.markdown('<div style="font-size:14px;font-weight:600;color:#1a1a1a;margin-top:20px;margin-bottom:10px;">📋 My Medicine List</div>', unsafe_allow_html=True)
            st.markdown('<div style="background:#fff;border:1px solid #eee;border-radius:12px;padding:14px;">', unsafe_allow_html=True)
            for i, med in enumerate(st.session_state.my_medicine_list):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(f'<div style="font-size:12px;color:#333;padding:6px 0;">💊 {med}</div>', unsafe_allow_html=True)
                with col_b:
                    if st.button("✕", key=f"remove_med_{i}"):
                        st.session_state.my_medicine_list.pop(i)
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        if st.session_state.selected_condition:
            cond = st.session_state.selected_condition
            medicines = get_medications(cond)
            description = get_description(cond)
            icon = DISEASE_ICONS.get(cond, "🏥")

            st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
  <div style="font-size:36px;">{icon}</div>
  <div>
    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:1px;">Recommended for</div>
    <div style="font-size:20px;font-weight:700;color:#1a1a1a;">{cond}</div>
  </div>
</div>
""", unsafe_allow_html=True)

            if description:
                st.markdown(f'<div style="background:#f9f9f9;border-radius:10px;padding:12px 14px;font-size:12px;color:#555;margin-bottom:16px;line-height:1.6;">{description}</div>', unsafe_allow_html=True)

            for med in medicines:
                st.markdown(f"""
<div style="background:#fff;border:1px solid #eee;border-radius:14px;padding:18px;margin-bottom:12px;
            box-shadow:0 2px 8px rgba(0,0,0,0.03);">
  <div style="font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:4px;">💊 {med}</div>
  <div style="font-size:11px;color:#999;">Consult your doctor for correct dosage and usage.</div>
</div>
""", unsafe_allow_html=True)
                if st.button(f"➕ Add {med} to My List", key=f"add_{med}", use_container_width=True):
                    if med not in st.session_state.my_medicine_list:
                        st.session_state.my_medicine_list.append(med)
                        st.success(f"Added {med} to your list!")
                        time.sleep(0.4)
                        st.rerun()

            st.markdown("""
<div style="background:#FFF9E6;border:1px solid #F7DC6F;border-radius:10px;padding:12px 14px;margin-top:8px;">
  <div style="font-size:11px;color:#856404;">
    ⚠️ <b>Disclaimer:</b> Always consult a licensed physician or pharmacist before taking any medication.
  </div>
</div>
""", unsafe_allow_html=True)
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🥗  Get Diet Plan", use_container_width=True, key="med_goto_diet"):
                    st.session_state.page = "diet"
                    st.rerun()
            with c2:
                if st.button("📥  Download Report", use_container_width=True, key="med_goto_report"):
                    st.session_state.page = "report"
                    st.rerun()
        else:
            st.markdown("""
<div style="background:#f9f9f9;border:1px dashed #ddd;border-radius:16px;padding:48px 24px;text-align:center;">
  <div style="font-size:48px;margin-bottom:16px;">💊</div>
  <div style="font-size:15px;font-weight:600;color:#888;">No Condition Selected</div>
  <div style="font-size:12px;color:#bbb;line-height:1.7;margin-top:8px;">
    Choose a condition from the left panel<br>to view recommended medicines.
  </div>
</div>
""", unsafe_allow_html=True)