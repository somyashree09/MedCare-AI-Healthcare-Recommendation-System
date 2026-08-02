import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import random

def show():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
.dash-card { animation: fadeInUp 0.45s ease; }

@keyframes countUp {
    from { opacity: 0; transform: scale(0.85); }
    to   { opacity: 1; transform: scale(1); }
}
.stat-number { animation: countUp 0.5s ease; }

.stat-card {
    background: #fff;
    border: 1px solid #eee;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.activity-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid #f3f3f3;
}
.activity-item:last-child { border-bottom: none; }
</style>
""", unsafe_allow_html=True)

    name = st.session_state.current_user or "Guest"
    first_name = name.split("@")[0].capitalize() if name else "Guest"

    # Time-based greeting
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
        emoji = "🌤️"
    elif hour < 17:
        greeting = "Good afternoon"
        emoji = "☀️"
    else:
        greeting = "Good evening"
        emoji = "🌙"

    # Compute stats from session state
    predictions_made = 1 if st.session_state.get("prediction_result") else 0
    medicines_saved = len(st.session_state.get("my_medicine_list", []))
    symptoms_tracked = len(st.session_state.get("selected_symptoms", []))
    diet_viewed = 1 if st.session_state.get("diet_condition") else 0

    # ── HERO GREETING ─────────────────────────────────────────────────────
    st.markdown(f"""
<div class="dash-card" style="background:linear-gradient(135deg,#0B7285 0%,#1aabbd 100%);
            border-radius:18px;padding:32px 36px;margin-bottom:24px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:-50px;right:-30px;width:180px;height:180px;
              background:rgba(255,255,255,0.06);border-radius:50%;"></div>
  <div style="position:absolute;bottom:-60px;right:120px;width:120px;height:120px;
              background:rgba(255,255,255,0.04);border-radius:50%;"></div>
  <div style="font-size:13px;color:rgba(255,255,255,0.7);margin-bottom:6px;">{emoji} {greeting}</div>
  <div style="font-size:26px;font-weight:700;color:#fff;">Welcome back, {first_name}! 👋</div>
  <div style="font-size:13px;color:rgba(255,255,255,0.75);margin-top:6px;max-width:480px;">
    Here's a snapshot of your health journey with MedCare AI today.
  </div>
</div>
""", unsafe_allow_html=True)

    # ── QUICK STAT CARDS ──────────────────────────────────────────────────
    stat_cols = st.columns(4)
    stats = [
        ("🩺", predictions_made, "Predictions Made", "#0B7285"),
        ("💊", medicines_saved, "Medicines Saved", "#534AB7"),
        ("🥗", diet_viewed, "Diet Plans Viewed", "#E67E22"),
        ("📋", symptoms_tracked, "Symptoms Tracked", "#27AE60"),
    ]
    for col, (icon, value, label, color) in zip(stat_cols, stats):
        with col:
            st.markdown(f"""
<div class="stat-card">
  <div style="display:flex;align-items:center;justify-content:space-between;">
    <div style="width:40px;height:40px;background:{color}15;border-radius:10px;
                display:flex;align-items:center;justify-content:center;font-size:19px;">{icon}</div>
  </div>
  <div class="stat-number" style="font-size:26px;font-weight:700;color:#1a1a1a;margin-top:12px;">{value}</div>
  <div style="font-size:11.5px;color:#888;margin-top:2px;">{label}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    chart_left, chart_right = st.columns([1.3, 1], gap="large")

    # ── LEFT: ACTIVITY BAR CHART ──────────────────────────────────────────
    with chart_left:
        st.markdown('<div class="dash-card" style="font-size:15px;font-weight:600;color:#1a1a1a;margin-bottom:12px;">📈 Weekly Activity Overview</div>', unsafe_allow_html=True)

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        random.seed(42)
        predictions_data = [random.randint(0, 5) for _ in days]
        medicine_data = [random.randint(0, 4) for _ in days]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=days, y=predictions_data, name="Predictions",
            marker_color="#0B7285",
            hovertemplate="<b>%{x}</b><br>Predictions: %{y}<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            x=days, y=medicine_data, name="Medicines Viewed",
            marker_color="#7FD4D9",
            hovertemplate="<b>%{x}</b><br>Medicines: %{y}<extra></extra>",
        ))
        fig.update_layout(
            barmode="group",
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=11, color="#666"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
            bargap=0.3,
            bargroupgap=0.15,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Disease distribution donut
        st.markdown('<div class="dash-card" style="font-size:15px;font-weight:600;color:#1a1a1a;margin:20px 0 12px;">🍩 Conditions Checked This Month</div>', unsafe_allow_html=True)

        labels = ["Common Cold", "Diabetes", "Migraine", "Hypertension", "Others"]
        values = [8, 5, 4, 3, 6]
        colors = ["#0B7285", "#1aabbd", "#7FD4D9", "#B2E5E8", "#E1F5EE"]

        fig2 = go.Figure(data=[go.Pie(
            labels=labels, values=values, hole=0.6,
            marker=dict(colors=colors, line=dict(color="#fff", width=2)),
            hovertemplate="<b>%{label}</b><br>%{value} checks (%{percent})<extra></extra>",
            textinfo="percent",
            textfont=dict(size=11),
        )])
        fig2.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=11, color="#666"),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05, font=dict(size=10)),
            annotations=[dict(text="26\nChecks", x=0.5, y=0.5, font_size=16, showarrow=False, font=dict(color="#0B7285", family="Inter"))],
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # ── RIGHT: HEALTH SCORE GAUGE + ACTIVITY FEED ─────────────────────────
    with chart_right:
        st.markdown('<div class="dash-card" style="font-size:15px;font-weight:600;color:#1a1a1a;margin-bottom:12px;">🎯 Your Health Engagement Score</div>', unsafe_allow_html=True)

        engagement_score = min(100, 20 + (predictions_made * 25) + (medicines_saved * 10) + (diet_viewed * 20) + (symptoms_tracked * 3))

        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=engagement_score,
            domain={"x": [0, 1], "y": [0, 1]},
            number={"suffix": "%", "font": {"size": 32, "color": "#0B7285", "family": "Inter"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "#ccc"},
                "bar": {"color": "#0B7285", "thickness": 0.3},
                "bgcolor": "white",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "#FDEDED"},
                    {"range": [40, 70], "color": "#FFF3CD"},
                    {"range": [70, 100], "color": "#E1F5EE"},
                ],
            },
        ))
        fig3.update_layout(
            height=220,
            margin=dict(l=20, r=20, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        if engagement_score < 40:
            msg = "Just getting started — try a disease prediction!"
        elif engagement_score < 70:
            msg = "Good progress — keep exploring your health insights."
        else:
            msg = "Excellent engagement! You're making the most of MedCare AI."
        st.markdown(f'<div style="text-align:center;font-size:12px;color:#888;margin-top:-10px;margin-bottom:20px;">{msg}</div>', unsafe_allow_html=True)

        # Recent Activity Feed
        st.markdown('<div class="dash-card" style="font-size:15px;font-weight:600;color:#1a1a1a;margin-bottom:12px;">🕑 Recent Activity</div>', unsafe_allow_html=True)

        activities = []
        if predictions_made:
            activities.append(("🩺", f"Predicted: {st.session_state.prediction_result}", "Just now", "#0B7285"))
        if medicines_saved:
            activities.append(("💊", f"Saved {medicines_saved} medicine(s) to list", "Recently", "#534AB7"))
        if diet_viewed:
            activities.append(("🥗", f"Viewed diet plan: {st.session_state.diet_condition}", "Recently", "#E67E22"))
        if not activities:
            activities.append(("✨", "No activity yet — start with a Disease Prediction!", "—", "#999"))

        st.markdown('<div class="dash-card" style="background:#fff;border:1px solid #eee;border-radius:14px;padding:6px 18px;">', unsafe_allow_html=True)
        for icon, text, time_label, color in activities:
            st.markdown(f"""
<div class="activity-item">
  <div style="width:32px;height:32px;background:{color}15;border-radius:9px;
              display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;">{icon}</div>
  <div style="flex:1;">
    <div style="font-size:12.5px;color:#333;font-weight:500;">{text}</div>
    <div style="font-size:10.5px;color:#aaa;margin-top:2px;">{time_label}</div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Quick action buttons
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="dash-card" style="font-size:13px;font-weight:600;color:#1a1a1a;margin-bottom:10px;">⚡ Quick Actions</div>', unsafe_allow_html=True)
        qa1, qa2 = st.columns(2)
        with qa1:
            if st.button("🩺 New Check", use_container_width=True, key="dash_qa_disease"):
                st.session_state.page = "disease"
                st.rerun()
        with qa2:
            if st.button("📥 Report", use_container_width=True, key="dash_qa_report"):
                st.session_state.page = "report"
                st.rerun()