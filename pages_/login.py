import streamlit as st
import time
import requests

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show():
    # Google Font
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

div[data-testid="stTextInput"] > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #e0e0e0 !important;
    padding: 10px 14px !important;
    font-size: 13px !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #0B7285 !important;
    box-shadow: 0 0 0 3px rgba(11,114,133,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.markdown(
            f'<div style="background:#E1F5EE;border:1px solid #b2dfdb;border-radius:10px;'
            f'padding:20px 24px;text-align:center;max-width:420px;margin:40px auto;">'
            f'<div style="font-size:32px;margin-bottom:8px;">👋</div>'
            f'<div style="font-size:16px;font-weight:600;color:#0B7285;">Welcome back, {st.session_state.current_user}!</div>'
            f'<div style="font-size:12px;color:#666;margin-top:6px;">You are already logged in.</div>'
            f'</div>', unsafe_allow_html=True,
        )
        _, c, _ = st.columns([2, 2, 2])
        with c:
            if st.button("Go to Dashboard →", use_container_width=True, key="login_to_dash"):
                st.session_state.page = "dashboard"
                st.rerun()
        return

    left, right = st.columns([1, 1], gap="large")

    # ── LEFT SIDE ─────────────────────────────────────────────────────────
    with left:
        st.markdown("""
<div style="background:linear-gradient(135deg,#0B7285 0%,#1aabbd 100%);
            border-radius:20px;padding:48px 36px;min-height:520px;
            display:flex;flex-direction:column;justify-content:center;
            position:relative;overflow:hidden;">

  <div style="position:absolute;top:-40px;right:-40px;width:180px;height:180px;
              background:rgba(255,255,255,0.06);border-radius:50%;"></div>
  <div style="position:absolute;bottom:-60px;left:-30px;width:220px;height:220px;
              background:rgba(255,255,255,0.04);border-radius:50%;"></div>

  <div style="font-size:36px;margin-bottom:16px;">🩺</div>
  <div style="font-size:26px;font-weight:700;color:#fff;line-height:1.3;margin-bottom:12px;">
    Your Health,<br>Our Priority
  </div>
  <div style="font-size:13px;color:rgba(255,255,255,0.7);line-height:1.8;margin-bottom:32px;">
    Sign in to access AI-powered disease prediction, personalised medicine and diet recommendations.
  </div>

  <div style="display:flex;flex-direction:column;gap:14px;">
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:36px;height:36px;background:rgba(255,255,255,0.12);border-radius:10px;
                  display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">🧠</div>
      <div>
        <div style="font-size:12px;font-weight:600;color:#fff;">ML-Powered Diagnosis</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.55);">40+ diseases covered with 92% accuracy</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:36px;height:36px;background:rgba(255,255,255,0.12);border-radius:10px;
                  display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">💊</div>
      <div>
        <div style="font-size:12px;font-weight:600;color:#fff;">Personalised Medicines</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.55);">500+ medicines mapped to conditions</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:36px;height:36px;background:rgba(255,255,255,0.12);border-radius:10px;
                  display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">🥗</div>
      <div>
        <div style="font-size:12px;font-weight:600;color:#fff;">Custom Diet Plans</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.55);">Nutrition tailored to your health</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── RIGHT SIDE ────────────────────────────────────────────────────────
    with right:
        st.markdown("""
<div style="padding:12px 0 24px;">
  <div style="font-size:24px;font-weight:700;color:#1a1a1a;margin-bottom:6px;">Welcome back 👋</div>
  <div style="font-size:13px;color:#888;">Sign in to your MedCare AI account</div>
</div>
""", unsafe_allow_html=True)

        st.markdown(
            '<div style="background:#fff;border:1px solid #eee;border-radius:16px;'
            'padding:28px 24px;box-shadow:0 4px 24px rgba(0,0,0,0.06);">',
            unsafe_allow_html=True,
        )

        username = st.text_input("👤  Username", placeholder="Enter your username", key="login_user")
        password = st.text_input("🔑  Password", placeholder="Enter your password", type="password", key="login_pass")

        col_rem, col_forgot = st.columns([1, 1])
        with col_rem:
            st.checkbox("Remember me", key="login_remember")
        with col_forgot:
            st.markdown(
                '<div style="text-align:right;padding-top:4px;">'
                '<span style="font-size:12px;color:#0B7285;cursor:pointer;font-weight:500;">Forgot password?</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        if st.button("🔐  Sign In", use_container_width=True, key="login_submit"):
            if not username or not password:
                st.error("⚠️ Please fill in all fields.")
            elif username in st.session_state.users_db and \
                 st.session_state.users_db[username]["password"] == password:
                with st.spinner("Signing you in..."):
                    time.sleep(0.8)
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success(f"✅ Welcome back, {username}!")
                time.sleep(0.8)
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin:20px 0;">
  <div style="flex:1;height:1px;background:#eee;"></div>
  <span style="font-size:11px;color:#ccc;">OR</span>
  <div style="flex:1;height:1px;background:#eee;"></div>
</div>
<div style="text-align:center;font-size:13px;color:#888;margin-bottom:10px;">
  Don't have an account?
</div>
""", unsafe_allow_html=True)

        if st.button("✨  Create a free account", use_container_width=True, key="login_to_signup"):
            st.session_state.page = "signup"
            st.rerun()