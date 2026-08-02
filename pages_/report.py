import streamlit as st
from datetime import datetime
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_pdf_report(username, prediction, confidence, medicines, diet_condition):
    """Builds a real PDF in-memory and returns the bytes. No external system
    dependencies (no wkhtmltopdf / chrome needed) — pure Python via reportlab,
    so this works reliably on any machine without extra installs."""

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=20 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
    )

    teal = HexColor("#0B7285")
    dark = HexColor("#1a1a1a")
    gray = HexColor("#666666")
    light_bg = HexColor("#F0F8F8")

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=22, textColor=teal, spaceAfter=2, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle("SubtitleStyle", parent=styles["Normal"], fontSize=10, textColor=gray, alignment=TA_CENTER, spaceAfter=14)
    section_style = ParagraphStyle("SectionStyle", parent=styles["Heading2"], fontSize=13, textColor=teal, spaceBefore=14, spaceAfter=8)
    body_style = ParagraphStyle("BodyStyle", parent=styles["Normal"], fontSize=10, textColor=dark, leading=15)
    meta_style = ParagraphStyle("MetaStyle", parent=styles["Normal"], fontSize=9, textColor=gray)
    disclaimer_style = ParagraphStyle("DisclaimerStyle", parent=styles["Normal"], fontSize=8, textColor=gray, leading=12)

    elements = []

    # ── Header ───────────────────────────────────────────────────────────
    elements.append(Paragraph("🩺 MedCare AI", title_style))
    elements.append(Paragraph("Healthcare Recommendation Report", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.2, color=teal, spaceAfter=14))

    # ── Patient Info ─────────────────────────────────────────────────────
    elements.append(Paragraph("Report Summary", section_style))
    info_data = [
        ["Generated for:", username or "Guest User"],
        ["Date Generated:", datetime.now().strftime("%B %d, %Y at %I:%M %p")],
        ["Report ID:", f"MC-{datetime.now().strftime('%Y%m%d%H%M%S')}"],
    ]
    info_table = Table(info_data, colWidths=[110, 350])
    info_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 0), (0, -1), gray),
        ("TEXTCOLOR", (1, 0), (1, -1), dark),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(info_table)

    # ── Disease Prediction Section ───────────────────────────────────────
    elements.append(Paragraph("🩺 Disease Prediction", section_style))
    if prediction:
        pred_data = [
            ["Predicted Condition:", prediction],
            ["Confidence Score:", f"{confidence}%"],
        ]
        pred_table = Table(pred_data, colWidths=[150, 310])
        pred_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), light_bg),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, 0), (0, -1), teal),
            ("TEXTCOLOR", (1, 0), (1, -1), dark),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#cce5e5")),
        ]))
        elements.append(pred_table)
    else:
        elements.append(Paragraph("No disease prediction recorded in this session.", body_style))

    # ── Medicines Section ────────────────────────────────────────────────
    elements.append(Paragraph("💊 Saved Medicines", section_style))
    if medicines:
        med_rows = [["#", "Medicine Name"]]
        for i, m in enumerate(medicines, 1):
            med_rows.append([str(i), m])
        med_table = Table(med_rows, colWidths=[30, 430])
        med_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), teal),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), light_bg]),
            ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#dddddd")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(med_table)
    else:
        elements.append(Paragraph("No medicines saved in this session.", body_style))

    # ── Diet Section ─────────────────────────────────────────────────────
    elements.append(Paragraph("🥗 Diet Recommendation", section_style))
    if diet_condition:
        elements.append(Paragraph(f"A personalised diet plan was reviewed for: <b>{diet_condition}</b>", body_style))
    else:
        elements.append(Paragraph("No diet plan viewed in this session.", body_style))

    # ── Disclaimer ───────────────────────────────────────────────────────
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=0.8, color=HexColor("#dddddd"), spaceAfter=10))
    elements.append(Paragraph(
        "<b>Disclaimer:</b> This report is generated by an AI-based recommendation system and is intended "
        "for informational purposes only. It is not a substitute for professional medical diagnosis or advice. "
        "Please consult a qualified healthcare provider before making any medical decisions.",
        disclaimer_style,
    ))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("Generated by MedCare AI — Healthcare Recommendation System", meta_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def show():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
</style>
""", unsafe_allow_html=True)

    name = st.session_state.current_user or "Guest"

    # ── HEADER ────────────────────────────────────────────────────────────
    st.markdown("""
<div style="background:linear-gradient(135deg,#0B7285 0%,#1aabbd 100%);
            border-radius:16px;padding:32px 36px;margin-bottom:24px;
            display:flex;align-items:center;gap:20px;">
  <div style="font-size:48px;">📥</div>
  <div>
    <div style="font-size:22px;font-weight:700;color:#fff;">Download Report</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.75);margin-top:4px;">
      Get a complete PDF summary of your health activity
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Pull data from session safely (never crashes even if nothing was done yet)
    prediction = st.session_state.get("prediction_result")
    confidence = st.session_state.get("prediction_confidence", 0)
    medicines = st.session_state.get("my_medicine_list", [])
    diet_condition = st.session_state.get("diet_condition")

    left_col, right_col = st.columns([1.3, 1], gap="large")

    # ── LEFT: PREVIEW OF WHAT WILL BE IN THE REPORT ───────────────────────
    with left_col:
        st.markdown('<div style="font-size:15px;font-weight:600;color:#1a1a1a;margin-bottom:14px;">📄 Report Preview</div>', unsafe_allow_html=True)

        st.markdown('<div style="background:#fff;border:1px solid #eee;border-radius:16px;padding:24px;box-shadow:0 2px 10px rgba(0,0,0,0.04);">', unsafe_allow_html=True)

        # Patient info
        st.markdown(f"""
<div style="border-bottom:1px solid #f0f0f0;padding-bottom:14px;margin-bottom:14px;">
  <div style="font-size:11px;color:#999;text-transform:uppercase;letter-spacing:1px;">Generated for</div>
  <div style="font-size:16px;font-weight:700;color:#1a1a1a;">{name}</div>
  <div style="font-size:11px;color:#999;margin-top:4px;">{datetime.now().strftime('%B %d, %Y · %I:%M %p')}</div>
</div>
""", unsafe_allow_html=True)

        # Prediction preview
        if prediction:
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #f5f5f5;">
  <div style="width:34px;height:34px;background:#E1F5EE;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;">🩺</div>
  <div style="flex:1;">
    <div style="font-size:12.5px;font-weight:600;color:#1a1a1a;">Disease Prediction</div>
    <div style="font-size:11px;color:#888;">{prediction} · {confidence}% confidence</div>
  </div>
  <span style="color:#27AE60;font-size:14px;">✓</span>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #f5f5f5;opacity:0.5;">
  <div style="width:34px;height:34px;background:#f0f0f0;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;">🩺</div>
  <div style="flex:1;">
    <div style="font-size:12.5px;font-weight:600;color:#999;">Disease Prediction</div>
    <div style="font-size:11px;color:#bbb;">Not done yet</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # Medicines preview
        if medicines:
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #f5f5f5;">
  <div style="width:34px;height:34px;background:#EEEDFE;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;">💊</div>
  <div style="flex:1;">
    <div style="font-size:12.5px;font-weight:600;color:#1a1a1a;">Medicines Saved</div>
    <div style="font-size:11px;color:#888;">{len(medicines)} medicine(s) recorded</div>
  </div>
  <span style="color:#27AE60;font-size:14px;">✓</span>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #f5f5f5;opacity:0.5;">
  <div style="width:34px;height:34px;background:#f0f0f0;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;">💊</div>
  <div style="flex:1;">
    <div style="font-size:12.5px;font-weight:600;color:#999;">Medicines Saved</div>
    <div style="font-size:11px;color:#bbb;">None saved yet</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # Diet preview
        if diet_condition:
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;padding:10px 0;">
  <div style="width:34px;height:34px;background:#FAEEDA;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;">🥗</div>
  <div style="flex:1;">
    <div style="font-size:12.5px;font-weight:600;color:#1a1a1a;">Diet Recommendation</div>
    <div style="font-size:11px;color:#888;">{diet_condition}</div>
  </div>
  <span style="color:#27AE60;font-size:14px;">✓</span>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="display:flex;align-items:center;gap:12px;padding:10px 0;opacity:0.5;">
  <div style="width:34px;height:34px;background:#f0f0f0;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px;">🥗</div>
  <div style="flex:1;">
    <div style="font-size:12.5px;font-weight:600;color:#999;">Diet Recommendation</div>
    <div style="font-size:11px;color:#bbb;">Not viewed yet</div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: DOWNLOAD ACTION ─────────────────────────────────────────────
    with right_col:
        st.markdown('<div style="font-size:15px;font-weight:600;color:#1a1a1a;margin-bottom:14px;">📥 Generate &amp; Download</div>', unsafe_allow_html=True)

        st.markdown("""
<div style="background:#fff;border:1px solid #eee;border-radius:16px;padding:24px;
            box-shadow:0 2px 10px rgba(0,0,0,0.04);text-align:center;">
  <div style="font-size:42px;margin-bottom:10px;">📄</div>
  <div style="font-size:14px;font-weight:600;color:#1a1a1a;margin-bottom:4px;">MedCare_AI_Report.pdf</div>
  <div style="font-size:11px;color:#999;margin-bottom:18px;">PDF · Generated instantly</div>
""", unsafe_allow_html=True)

        # Generate the PDF bytes safely — this always succeeds even with empty data,
        # so the download button never errors out for the user.
        try:
            pdf_bytes = generate_pdf_report(name, prediction, confidence, medicines, diet_condition)
            pdf_ready = True
        except Exception as e:
            pdf_ready = False
            st.error(f"Something went wrong generating the report: {e}")

        if pdf_ready:
            st.download_button(
                label="⬇️  Download PDF Report",
                data=pdf_bytes,
                file_name=f"MedCare_AI_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_report_btn",
            )

        st.markdown("</div>", unsafe_allow_html=True)

        if not (prediction or medicines or diet_condition):
            st.markdown("""
<div style="background:#FFF9E6;border:1px solid #F7DC6F;border-radius:10px;
            padding:12px 14px;margin-top:14px;">
  <div style="font-size:11px;color:#856404;">
    💡 You haven't done any predictions yet. The report will still download,
    but it will be more useful after you try Disease Prediction, Medicines, or Diet pages.
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        if st.button("🩺  Run a Disease Prediction First", use_container_width=True, key="report_goto_disease"):
            st.session_state.page = "disease"
            st.rerun()