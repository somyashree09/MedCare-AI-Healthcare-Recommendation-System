import streamlit as st
import time
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from model import predict_disease, get_precautions, get_description, get_all_symptoms

def show():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
div[data-testid="stTextInput"] > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #e0e0e0 !important;
    padding: 10px 14px !important;
    font-size: 13px !important;
}
div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #0B7285 !important;
    box-shadow: 0 0 0 3px rgba(11,114,133,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

    if "selected_symptoms" not in st.session_state:
        st.session_state.selected_symptoms = []
    if "prediction_result" not in st.session_state:
        st.session_state.prediction_result = None
    if "prediction_confidence" not in st.session_state:
        st.session_state.prediction_confidence = 0

    ALL_SYMPTOMS = get_all_symptoms()

    # ── HEADER ────────────────────────────────────────────────────────────
    st.markdown("""
<div style="background:linear-gradient(135deg,#0B7285 0%,#1aabbd 100%);
            border-radius:16px;padding:32px 36px;margin-bottom:24px;
            display:flex;align-items:center;gap:20px;">
  <div style="font-size:48px;">🩺</div>
  <div>
    <div style="font-size:22px;font-weight:700;color:#fff;">Disease Prediction</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.75);margin-top:4px;">
      Select your symptoms and let our ML model predict the most likely condition
    </div>
  </div>
  <div style="margin-left:auto;background:rgba(255,255,255,0.12);border-radius:12px;padding:12px 20px;text-align:center;">
    <div style="font-size:22px;font-weight:700;color:#fff;">41</div>
    <div style="font-size:10px;color:rgba(255,255,255,0.6);">Diseases</div>
  </div>
</div>
""", unsafe_allow_html=True)

    left_col, right_col = st.columns([1.2, 1], gap="large")

    with left_col:
        st.markdown('<div style="font-size:15px;font-weight:600;color:#1a1a1a;margin-bottom:12px;">🔍 Search & Select Symptoms</div>', unsafe_allow_html=True)

        search = st.text_input("", placeholder="Type a symptom e.g. headache, fever, cough...",
                               key="symptom_search", label_visibility="collapsed")

        filtered = [s for s in ALL_SYMPTOMS
                    if search.lower().replace(" ", "_") in s.lower()] if search else ALL_SYMPTOMS[:60]

        st.markdown('<div style="font-size:11px;color:#999;margin-bottom:8px;">Click a symptom to select it:</div>', unsafe_allow_html=True)
        st.markdown('<div style="background:#f9f9f9;border-radius:12px;padding:14px;border:1px solid #eee;">', unsafe_allow_html=True)

        symptoms_to_show = filtered[:30]
        rows = [symptoms_to_show[i:i+3] for i in range(0, len(symptoms_to_show), 3)]
        for row in rows:
            cols = st.columns(3)
            for col, symptom in zip(cols, row):
                with col:
                    label = symptom.replace("_", " ").title()
                    is_selected = symptom in st.session_state.selected_symptoms
                    btn_label = f"✅ {label}" if is_selected else label
                    if st.button(btn_label, key=f"sym_{symptom}", use_container_width=True):
                        if symptom in st.session_state.selected_symptoms:
                            st.session_state.selected_symptoms.remove(symptom)
                        else:
                            st.session_state.selected_symptoms.append(symptom)
                        st.session_state.prediction_result = None
                        st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:16px;font-size:13px;font-weight:600;color:#1a1a1a;">Selected Symptoms:</div>', unsafe_allow_html=True)

        if st.session_state.selected_symptoms:
            chips_html = "".join(
                f'<span style="display:inline-block;background:#0B7285;color:white;'
                f'border-radius:20px;padding:4px 12px;font-size:12px;font-weight:500;margin:3px;">'
                f'{s.replace("_"," ").title()} ✕</span>'
                for s in st.session_state.selected_symptoms
            )
            st.markdown(f'<div style="margin-top:8px;padding:12px;background:#fff;border-radius:10px;border:1px solid #eee;">{chips_html}</div>', unsafe_allow_html=True)

            col_predict, col_clear = st.columns([2, 1])
            with col_predict:
                if st.button("🔍  Predict Disease", use_container_width=True, key="predict_btn"):
                    with st.spinner("Analyzing your symptoms..."):
                        time.sleep(1)
                    disease, confidence = predict_disease(st.session_state.selected_symptoms)
                    st.session_state.prediction_result = disease
                    st.session_state.prediction_confidence = confidence
                    st.rerun()
            with col_clear:
                if st.button("🗑️  Clear All", use_container_width=True, key="clear_btn"):
                    st.session_state.selected_symptoms = []
                    st.session_state.prediction_result = None
                    st.rerun()
        else:
            st.markdown(
                '<div style="margin-top:8px;padding:16px;background:#f9f9f9;border-radius:10px;'
                'border:1px dashed #ddd;text-align:center;color:#aaa;font-size:12px;">'
                'No symptoms selected yet. Click symptoms above to add them.</div>',
                unsafe_allow_html=True,
            )

    with right_col:
        st.markdown('<div style="font-size:15px;font-weight:600;color:#1a1a1a;margin-bottom:12px;">📊 Prediction Result</div>', unsafe_allow_html=True)

        if st.session_state.prediction_result:
            disease    = st.session_state.prediction_result
            confidence = st.session_state.prediction_confidence
            precautions = get_precautions(disease)
            description = get_description(disease)

            st.markdown(f"""
<div style="background:linear-gradient(135deg,#E1F5EE,#f0fbf8);
            border:2px solid #0B728544;border-radius:16px;padding:24px;margin-bottom:16px;">
  <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
    <div style="font-size:44px;">🩺</div>
    <div>
      <div style="font-size:11px;color:#888;font-weight:500;text-transform:uppercase;letter-spacing:1px;">Predicted Condition</div>
      <div style="font-size:22px;font-weight:700;color:#1a1a1a;margin-top:2px;">{disease}</div>
    </div>
  </div>
  <div style="font-size:12px;color:#666;margin-bottom:8px;font-weight:500;">Confidence Score</div>
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="flex:1;background:#e0e0e0;border-radius:6px;height:8px;">
      <div style="background:#0B7285;width:{confidence}%;height:8px;border-radius:6px;"></div>
    </div>
    <div style="font-size:16px;font-weight:700;color:#0B7285;">{confidence}%</div>
  </div>
</div>
""", unsafe_allow_html=True)

            if description:
                st.markdown(f"""
<div style="background:#fff;border:1px solid #eee;border-radius:12px;padding:16px;margin-bottom:16px;">
  <div style="font-size:13px;font-weight:600;color:#1a1a1a;margin-bottom:8px;">📋 About this condition</div>
  <div style="font-size:12px;color:#555;line-height:1.7;">{description}</div>
</div>
""", unsafe_allow_html=True)

            if precautions:
                st.markdown('<div style="background:#fff;border:1px solid #eee;border-radius:12px;padding:16px;margin-bottom:16px;">', unsafe_allow_html=True)
                st.markdown('<div style="font-size:13px;font-weight:600;color:#1a1a1a;margin-bottom:12px;">⚠️ Recommended Precautions</div>', unsafe_allow_html=True)
                for i, p in enumerate(precautions, 1):
                    st.markdown(
                        f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;">'
                        f'<div style="width:22px;height:22px;background:#E1F5EE;border-radius:50%;'
                        f'display:flex;align-items:center;justify-content:center;'
                        f'font-size:11px;font-weight:700;color:#0B7285;flex-shrink:0;">{i}</div>'
                        f'<div style="font-size:12px;color:#555;padding-top:3px;">{p}</div></div>',
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("""
<div style="background:#FFF9E6;border:1px solid #F7DC6F;border-radius:10px;padding:12px 14px;">
  <div style="font-size:11px;color:#856404;">
    ⚠️ <b>Disclaimer:</b> This prediction is AI-generated for informational purposes only.
    Please consult a qualified medical professional for proper diagnosis and treatment.
  </div>
</div>
""", unsafe_allow_html=True)

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💊  Get Medicines", use_container_width=True, key="goto_medicine"):
                    st.session_state.page = "medicine"
                    st.rerun()
            with c2:
                if st.button("🥗  Get Diet Plan", use_container_width=True, key="goto_diet"):
                    st.session_state.page = "diet"
                    st.rerun()
        else:
            st.markdown("""
<div style="background:#f9f9f9;border:1px dashed #ddd;border-radius:16px;padding:48px 24px;text-align:center;">
  <div style="font-size:48px;margin-bottom:16px;">🔬</div>
  <div style="font-size:15px;font-weight:600;color:#888;margin-bottom:8px;">No Prediction Yet</div>
  <div style="font-size:12px;color:#bbb;line-height:1.7;">
    Select at least 3 symptoms from the left panel<br>and click <b>Predict Disease</b> to get started.
  </div>
</div>
""", unsafe_allow_html=True)
            st.markdown("""
<div style="background:#fff;border:1px solid #eee;border-radius:12px;padding:16px;margin-top:16px;">
  <div style="font-size:13px;font-weight:600;color:#1a1a1a;margin-bottom:10px;">💡 Tips for better results</div>
  <div style="font-size:12px;color:#666;line-height:1.9;">
    • Select <b>3 or more symptoms</b> for accurate prediction<br>
    • Use the search bar to find symptoms quickly<br>
    • Be as specific as possible with your symptoms<br>
    • Check the confidence score after prediction
  </div>
</div>
""", unsafe_allow_html=True)