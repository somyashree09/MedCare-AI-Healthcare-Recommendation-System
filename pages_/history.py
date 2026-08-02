import streamlit as st
from datetime import datetime, timedelta
import random

def show():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.history-item { animation: fadeInUp 0.35s ease; }

.timeline-line {
    position: absolute;
    left: 19px;
    top: 40px;
    bottom: -8px;
    width: 2px;
    background: #e8e8e8;
}
</style>
""", unsafe_allow_html=True)

    if "history_filter" not in st.session_state:
        st.session_state.history_filter = "All"

    # ── HEADER ────────────────────────────────────────────────────────────
    st.markdown("""
<div style="background:linear-gradient(135deg,#0B7285 0%,#1aabbd 100%);
            border-radius:16px;padding:32px 36px;margin-bottom:24px;
            display:flex;align-items:center;gap:20px;">
  <div style="font-size:48px;">🕑</div>
  <div>
    <div style="font-size:22px;font-weight:700;color:#fff;">Activity History</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.75);margin-top:4px;">
      A timeline of your predictions, medicines, and diet plans
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── BUILD REAL HISTORY FROM SESSION STATE ────────────────────────────
    real_events = []
    now = datetime.now()

    if st.session_state.get("prediction_result"):
        real_events.append({
            "type": "Prediction",
            "icon": "🩺",
            "color": "#0B7285",
            "title": f"Predicted: {st.session_state.prediction_result}",
            "subtitle": f"Confidence: {st.session_state.get('prediction_confidence', 0)}%",
            "time": now - timedelta(minutes=12),
        })

    if st.session_state.get("my_medicine_list"):
        for med in st.session_state.my_medicine_list:
            real_events.append({
                "type": "Medicine",
                "icon": "💊",
                "color": "#534AB7",
                "title": f"Saved medicine: {med}",
                "subtitle": "Added to your medicine list",
                "time": now - timedelta(minutes=8),
            })

    if st.session_state.get("diet_condition"):
        real_events.append({
            "type": "Diet",
            "icon": "🥗",
            "color": "#E67E22",
            "title": f"Viewed diet plan: {st.session_state.diet_condition}",
            "subtitle": "Personalised nutrition plan",
            "time": now - timedelta(minutes=4),
        })

    # Add a few sample past events for visual richness (backend teammate replaces with real DB query)
    sample_events = [
        {"type": "Prediction", "icon": "🩺", "color": "#0B7285", "title": "Predicted: Common Cold", "subtitle": "Confidence: 87%", "time": now - timedelta(days=1, hours=3)},
        {"type": "Medicine", "icon": "💊", "color": "#534AB7", "title": "Saved medicine: Paracetamol", "subtitle": "Added to your medicine list", "time": now - timedelta(days=1, hours=2, minutes=50)},
        {"type": "Diet", "icon": "🥗", "color": "#E67E22", "title": "Viewed diet plan: Common Cold", "subtitle": "Personalised nutrition plan", "time": now - timedelta(days=1, hours=2, minutes=40)},
        {"type": "Prediction", "icon": "🩺", "color": "#0B7285", "title": "Predicted: Migraine", "subtitle": "Confidence: 79%", "time": now - timedelta(days=3, hours=5)},
        {"type": "Report", "icon": "📥", "color": "#185FA5", "title": "Downloaded health report", "subtitle": "PDF report generated", "time": now - timedelta(days=3, hours=4, minutes=55)},
        {"type": "Medicine", "icon": "💊", "color": "#534AB7", "title": "Saved medicine: Sumatriptan", "subtitle": "Added to your medicine list", "time": now - timedelta(days=5, hours=1)},
        {"type": "Prediction", "icon": "🩺", "color": "#0B7285", "title": "Predicted: Hypertension", "subtitle": "Confidence: 91%", "time": now - timedelta(days=7, hours=6)},
    ]

    all_events = real_events + sample_events
    all_events.sort(key=lambda x: x["time"], reverse=True)

    # ── STATS ROW ─────────────────────────────────────────────────────────
    total_predictions = len([e for e in all_events if e["type"] == "Prediction"])
    total_medicines = len([e for e in all_events if e["type"] == "Medicine"])
    total_diets = len([e for e in all_events if e["type"] == "Diet"])
    total_reports = len([e for e in all_events if e["type"] == "Report"])

    stat_cols = st.columns(4)
    stat_data = [
        ("🩺", total_predictions, "Total Predictions", "#0B7285"),
        ("💊", total_medicines, "Medicines Saved", "#534AB7"),
        ("🥗", total_diets, "Diet Plans Viewed", "#E67E22"),
        ("📥", total_reports, "Reports Downloaded", "#185FA5"),
    ]
    for col, (icon, val, label, color) in zip(stat_cols, stat_data):
        with col:
            st.markdown(f"""
<div style="background:#fff;border:1px solid #eee;border-radius:14px;padding:16px;text-align:center;
            box-shadow:0 2px 8px rgba(0,0,0,0.03);">
  <div style="width:36px;height:36px;background:{color}15;border-radius:10px;margin:0 auto 8px;
              display:flex;align-items:center;justify-content:center;font-size:17px;">{icon}</div>
  <div style="font-size:20px;font-weight:700;color:#1a1a1a;">{val}</div>
  <div style="font-size:11px;color:#888;margin-top:2px;">{label}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ── FILTER TABS ───────────────────────────────────────────────────────
    filters = ["All", "Prediction", "Medicine", "Diet", "Report"]
    filter_cols = st.columns(len(filters))
    for col, f in zip(filter_cols, filters):
        with col:
            is_active = st.session_state.history_filter == f
            bg = "#0B7285" if is_active else "#fff"
            txt = "#fff" if is_active else "#666"
            border = "#0B7285" if is_active else "#eee"
            st.markdown(
                f'<div style="background:{bg};border:1.5px solid {border};border-radius:10px;'
                f'padding:8px;text-align:center;margin-bottom:4px;">'
                f'<span style="font-size:12px;font-weight:600;color:{txt};">{f}</span></div>',
                unsafe_allow_html=True,
            )
            if st.button("View", key=f"hist_filter_{f}", use_container_width=True):
                st.session_state.history_filter = f
                st.rerun()

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ── FILTERED EVENTS ───────────────────────────────────────────────────
    if st.session_state.history_filter == "All":
        filtered_events = all_events
    else:
        filtered_events = [e for e in all_events if e["type"] == st.session_state.history_filter]

    if not filtered_events:
        st.markdown("""
<div style="background:#f9f9f9;border:1px dashed #ddd;border-radius:16px;
            padding:48px 24px;text-align:center;">
  <div style="font-size:48px;margin-bottom:16px;">📭</div>
  <div style="font-size:15px;font-weight:600;color:#888;">No activity found for this filter</div>
</div>
""", unsafe_allow_html=True)
        return

    # Group by date
    def date_label(dt):
        delta_days = (now.date() - dt.date()).days
        if delta_days == 0:
            return "Today"
        elif delta_days == 1:
            return "Yesterday"
        else:
            return dt.strftime("%B %d, %Y")

    grouped = {}
    for e in filtered_events:
        label = date_label(e["time"])
        grouped.setdefault(label, []).append(e)

    st.markdown('<div style="background:#fff;border:1px solid #eee;border-radius:16px;padding:24px 28px;box-shadow:0 2px 10px rgba(0,0,0,0.03);">', unsafe_allow_html=True)

    for date_group, events in grouped.items():
        st.markdown(f'<div style="font-size:12px;font-weight:700;color:#0B7285;text-transform:uppercase;letter-spacing:1px;margin:18px 0 14px;">{date_group}</div>', unsafe_allow_html=True)

        for e in events:
            time_str = e["time"].strftime("%I:%M %p").lstrip("0")
            st.markdown(f"""
<div class="history-item" style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;
            border-bottom:1px solid #f5f5f5;">
  <div style="width:38px;height:38px;background:{e['color']}15;border-radius:10px;
              display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0;">{e['icon']}</div>
  <div style="flex:1;">
    <div style="font-size:13px;font-weight:600;color:#1a1a1a;">{e['title']}</div>
    <div style="font-size:11.5px;color:#999;margin-top:2px;">{e['subtitle']}</div>
  </div>
  <div style="font-size:11px;color:#bbb;white-space:nowrap;padding-top:3px;">{time_str}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── CLEAR HISTORY ─────────────────────────────────────────────────────
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    _, c, _ = st.columns([2, 1.4, 2])
    with c:
        if st.button("🗑️  Clear My Activity", use_container_width=True, key="clear_history"):
            st.session_state.prediction_result = None
            st.session_state.my_medicine_list = []
            st.session_state.diet_condition = None
            st.success("Your activity has been cleared!")
            st.rerun()