import streamlit as st
import time

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
            f'<div style="font-size:32px;margin-bottom:8px;">✅</div>'
            f'<div style="font-size:16px;font-weight:600;color:#0B7285;">Already signed in as {st.session_state.current_user}!</div>'
            f'</div>', unsafe_allow_html=True,
        )
        return

    left, right = st.columns([1, 1], gap="large")

    # ── LEFT SIDE ─────────────────────────────────────────────────────────
    with left:
        st.markdown("""
<div style="background:linear-gradient(135deg,#0B7285 0%,#1aabbd 100%);
            border-radius:20px;padding:48px 36px;min-height:620px;
            display:flex;flex-direction:column;justify-content:center;
            position:relative;overflow:hidden;">

  <div style="position:absolute;top:-40px;right:-40px;width:180px;height:180px;
              background:rgba(255,255,255,0.06);border-radius:50%;"></div>
  <div style="position:absolute;bottom:-60px;left:-30px;width:220px;height:220px;
              background:rgba(255,255,255,0.04);border-radius:50%;"></div>

  <div style="font-size:36px;margin-bottom:16px;">🌟</div>
  <div style="font-size:26px;font-weight:700;color:#fff;line-height:1.3;margin-bottom:12px;">
    Start Your Health<br>Journey Today
  </div>
  <div style="font-size:13px;color:rgba(255,255,255,0.7);line-height:1.8;margin-bottom:32px;">
    Create a free account and get instant access to AI-powered healthcare recommendations.
  </div>

  <div style="display:flex;flex-direction:column;gap:16px;">
    <div style="background:rgba(255,255,255,0.1);border-radius:12px;padding:16px;">
      <div style="font-size:22px;font-weight:700;color:#fff;">40+</div>
      <div style="font-size:11px;color:rgba(255,255,255,0.6);">Diseases we can predict</div>
    </div>
    <div style="background:rgba(255,255,255,0.1);border-radius:12px;padding:16px;">
      <div style="font-size:22px;font-weight:700;color:#fff;">92%</div>
      <div style="font-size:11px;color:rgba(255,255,255,0.6);">Model accuracy rate</div>
    </div>
    <div style="background:rgba(255,255,255,0.1);border-radius:12px;padding:16px;">
      <div style="font-size:22px;font-weight:700;color:#fff;">500+</div>
      <div style="font-size:11px;color:rgba(255,255,255,0.6);">Medicines in our database</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── RIGHT SIDE ────────────────────────────────────────────────────────
    with right:
        st.markdown("""
<div style="padding:12px 0 20px;">
  <div style="font-size:24px;font-weight:700;color:#1a1a1a;margin-bottom:6px;">Create your account ✨</div>
  <div style="font-size:13px;color:#888;">Join MedCare AI — it's completely free</div>
</div>
""", unsafe_allow_html=True)

        # NOTE: First/Last Name now use full-width stacked inputs instead of
        # nested 2-column split inside an already-narrow `right` column.
        # The old nested st.columns(2) inside a 50%-width column made the
        # Last Name box too cramped, which caused unreliable input capture.
        first_name = st.text_input("First Name", placeholder="John", key="signup_page_fname")
        last_name = st.text_input("Last Name", placeholder="Doe", key="signup_page_lname")

        email    = st.text_input("📧  Email Address", placeholder="john@email.com", key="signup_page_email")
        username = st.text_input("👤  Username", placeholder="Choose a username", key="signup_page_username")

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            password  = st.text_input("🔑  Password", placeholder="Min 6 chars", type="password", key="signup_page_password")
        with col_p2:
            password2 = st.text_input("🔑  Confirm", placeholder="Repeat password", type="password", key="signup_page_confirm")

        if password:
            strength = len(password)
            if strength < 6:
                bar_color, label, bar_w = "#e74c3c", "Weak", "33%"
            elif strength < 10:
                bar_color, label, bar_w = "#f39c12", "Medium", "66%"
            else:
                bar_color, label, bar_w = "#27ae60", "Strong", "100%"
            st.markdown(
                f'<div style="margin:4px 0 8px;">'
                f'<div style="display:flex;justify-content:space-between;font-size:10px;color:#888;margin-bottom:4px;">'
                f'<span>Password strength</span>'
                f'<span style="color:{bar_color};font-weight:600;">{label}</span></div>'
                f'<div style="background:#f0f0f0;border-radius:4px;height:5px;">'
                f'<div style="background:{bar_color};width:{bar_w};height:5px;border-radius:4px;"></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

        agree = st.checkbox("I agree to the Terms of Service and Privacy Policy", key="signup_page_agree")
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button("🚀  Create Account", use_container_width=True, key="signup_page_submit"):

            first_name = first_name.strip()
            last_name = last_name.strip()
            email = email.strip()
            username = username.strip()

            if not all([
                first_name,
                last_name,
                email,
                username,
                password,
                password2
            ]):
                st.error("⚠️ Please fill in all fields.")

            elif len(password) < 6:
                st.error("⚠️ Password must be at least 6 characters.")

            elif password != password2:
                st.error("⚠️ Passwords do not match.")

            elif "@" not in email:
                st.error("⚠️ Please enter a valid email address.")

            elif username in st.session_state.users_db:
                st.error("⚠️ Username already taken. Please choose another.")

            elif not agree:
                st.error("⚠️ Please agree to the Terms of Service.")

            else:
                with st.spinner("Creating your account..."):
                    time.sleep(1)

                st.session_state.users_db[username] = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                }

                st.session_state.logged_in = True
                st.session_state.current_user = username

                st.success(f"🎉 Account created! Welcome, {first_name}!")

                time.sleep(1)

                st.session_state.page = "dashboard"
                st.rerun()