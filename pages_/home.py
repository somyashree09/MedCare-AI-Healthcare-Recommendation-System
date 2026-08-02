import streamlit as st

def show():
    st.markdown("""
<div style="background:linear-gradient(135deg,#0B7285 0%,#0e8fa5 60%,#1aabbd 100%);
            padding:48px 48px 36px;text-align:center;border-radius:12px;margin-bottom:16px;">
  <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:12px;">
    <div style="width:44px;height:44px;background:rgba(255,255,255,0.15);border-radius:12px;
                display:flex;align-items:center;justify-content:center;
                border:1px solid rgba(255,255,255,0.25);font-size:22px;">🩺</div>
    <span style="font-size:26px;font-weight:700;color:#ffffff;letter-spacing:-0.5px;">MedCare AI</span>
  </div>
  <div style="display:inline-block;background:rgba(255,255,255,0.12);
              border:1px solid rgba(255,255,255,0.22);border-radius:20px;padding:4px 16px;margin-bottom:18px;">
    <span style="font-size:11px;color:rgba(255,255,255,0.85);letter-spacing:0.5px;">Healthcare Recommendation System</span>
  </div>
  <p style="font-size:15px;color:rgba(255,255,255,0.75);max-width:440px;margin:0 auto 28px;line-height:1.7;">
    Predict diseases, get personalised medicine and diet recommendations — powered by machine learning.
  </p>
  <div style="display:flex;justify-content:center;flex-wrap:wrap;margin-bottom:28px;">
    <div style="display:flex;align-items:center;gap:10px;padding:10px 22px;border-right:1px solid rgba(255,255,255,0.15);">
      <div style="width:32px;height:32px;background:rgba(255,255,255,0.12);border-radius:8px;
                  display:flex;align-items:center;justify-content:center;font-size:15px;">🧠</div>
      <div style="text-align:left;">
        <div style="font-size:12px;font-weight:600;color:#fff;">Predict Diseases</div>
        <div style="font-size:10px;color:rgba(255,255,255,0.5);">ML-powered diagnosis</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;padding:10px 22px;border-right:1px solid rgba(255,255,255,0.15);">
      <div style="width:32px;height:32px;background:rgba(255,255,255,0.12);border-radius:8px;
                  display:flex;align-items:center;justify-content:center;font-size:15px;">💊</div>
      <div style="text-align:left;">
        <div style="font-size:12px;font-weight:600;color:#fff;">Medicine Suggestions</div>
        <div style="font-size:10px;color:rgba(255,255,255,0.5);">Personalised plans</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;padding:10px 22px;">
      <div style="width:32px;height:32px;background:rgba(255,255,255,0.12);border-radius:8px;
                  display:flex;align-items:center;justify-content:center;font-size:15px;">🥗</div>
      <div style="text-align:left;">
        <div style="font-size:12px;font-weight:600;color:#fff;">Diet Plans</div>
        <div style="font-size:10px;color:rgba(255,255,255,0.5);">Nutrition recommendations</div>
      </div>
    </div>
  </div>
  <div style="display:flex;justify-content:center;flex-wrap:wrap;padding-top:20px;border-top:1px solid rgba(255,255,255,0.12);">
    <div style="text-align:center;padding:0 28px;border-right:1px solid rgba(255,255,255,0.15);">
      <div style="font-size:22px;font-weight:700;color:#fff;">40+</div>
      <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-top:2px;">Diseases covered</div>
    </div>
    <div style="text-align:center;padding:0 28px;border-right:1px solid rgba(255,255,255,0.15);">
      <div style="font-size:22px;font-weight:700;color:#fff;">92%</div>
      <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-top:2px;">Model accuracy</div>
    </div>
    <div style="text-align:center;padding:0 28px;border-right:1px solid rgba(255,255,255,0.15);">
      <div style="font-size:22px;font-weight:700;color:#fff;">5</div>
      <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-top:2px;">ML models</div>
    </div>
    <div style="text-align:center;padding:0 28px;">
      <div style="font-size:22px;font-weight:700;color:#fff;">500+</div>
      <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-top:2px;">Medicines mapped</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    _, c1, c2, _ = st.columns([3, 1.5, 1.5, 3])
    with c1:
        if st.button("🩺  Check Symptoms", use_container_width=True, key="home_disease"):
            st.session_state.page = "disease"
            st.rerun()
    with c2:
        if st.button("📊  View Dashboard", use_container_width=True, key="home_dash"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    cards = [
        ("🩺", "#E1F5EE", "Disease Prediction",  "Enter symptoms and get an AI-powered disease diagnosis.", "disease"),
        ("💊", "#EEEDFE", "Medicines",            "Personalised medicine recommendations for your condition.", "medicine"),
        ("🥗", "#FAEEDA", "Diet Plans",           "Custom nutrition plans to support your recovery.", "diet"),
        ("📥", "#E6F1FB", "Reports",              "Download your full health report and history.", "report"),
    ]

    cols = st.columns(4, gap="medium")
    for col, (icon, bg, title, desc, pg) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div style="background:#fff;border:1px solid #e8e8e8;border-radius:12px;'
                f'padding:18px 16px 10px;min-height:150px;">'
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">'
                f'<div style="width:36px;height:36px;background:{bg};border-radius:9px;'
                f'display:flex;align-items:center;justify-content:center;font-size:18px;">{icon}</div>'
                f'<span style="font-size:13px;font-weight:600;color:#1a1a1a;">{title}</span></div>'
                f'<p style="font-size:12px;color:#888;line-height:1.6;margin:0 0 10px;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button(f"Open {title}", key=f"home_card_{pg}", use_container_width=True):
                st.session_state.page = pg
                st.rerun()
