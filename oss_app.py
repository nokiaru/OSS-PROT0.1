import streamlit as st
import plotly.express as px
from fpdf import FPDF

def generate_pdf(system_name, location, oss_score, category, explanation, scores):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Orwellian Surveillance Scale (OSS) Report", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 8, f"System: {system_name}", ln=True)
    pdf.cell(0, 8, f"Location: {location}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 8, f"OSS Score: {oss_score}", ln=True)
    pdf.cell(0, 8, f"Category: {category}", ln=True)
    pdf.ln(5)

    pdf.multi_cell(0, 8, f"Interpretation: {explanation}")
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Dimension Scores", ln=True)

    pdf.set_font("Arial", size=12)
    for dim, val in scores.items():
        pdf.cell(0, 8, f"{dim}: {val}", ln=True)

    return pdf.output(dest="S").encode("latin-1")

st.set_page_config(page_title="Orwellian Surveillance Scale (OSS)", layout="centered")

st.title("Orwellian Surveillance Scale (OSS) – Prototype")

st.write(
    "This tool lets you score a surveillance system across key dimensions "
    "and produces an overall Orwellian surveillance index from 0 to 100."
)

# --- Core dimensions and descriptions ---
DIMENSIONS = {
    "Visibility / Monitoring": "How constantly and pervasively are people observed or tracked?",
    "Predictive Control": "To what extent is data used to predict and pre-empt behaviour?",
    "Self-Censorship": "Do people change what they say or do because they feel watched?",
    "Datafication": "How fully are people reduced to data points or algorithmic profiles?",
    "Trust in State / Institutions": "How much power over data is given to institutions?",
    "Resignation / Normalisation": "Do people feel surveillance is inevitable and unchangeable?"
}

# --- Weights (you can tweak these later based on theory) ---
WEIGHTS = {
    "Visibility / Monitoring": 1.2,
    "Predictive Control": 1.3,
    "Self-Censorship": 1.5,
    "Datafication": 1.1,
    "Trust in State / Institutions": 1.0,
    "Resignation / Normalisation": 0.9
}

MAX_SCORE = 4 # 0–4 Likert

# --- Form UI ---
with st.form("oss_form"):
    system_name = st.text_input("System or technology being assessed")
    location = st.text_input("Country / location (optional)")

    st.markdown("### Rate each dimension from 0 to 4")
    st.caption("0 = Not present · 1 = Very weak · 2 = Moderate · 3 = Strong · 4 = Extreme / totalising")

    scores = {}
    for dim, desc in DIMENSIONS.items():
        st.markdown(f"**{dim}**")
        st.caption(desc)
        scores[dim] = st.slider(
            label=f"Score for {dim}",
            min_value=0,
            max_value=4,
            value=0,
            key=dim
        )

    submitted = st.form_submit_button("Calculate OSS score")

# --- Logic after submit ---
if submitted:
    weighted_sum = 0
    max_weighted_sum = 0

    for dim, score in scores.items():
        w = WEIGHTS[dim]
        weighted_sum += score * w
        max_weighted_sum += MAX_SCORE * w

    if max_weighted_sum > 0:
        oss_score = round((weighted_sum / max_weighted_sum) * 100, 1)
    else:
        oss_score = 0.0

    # Classification bands
    if oss_score <= 25:
        category = "Low surveillance"
        explanation = "Surveillance is present but limited in scope or intensity."
    elif oss_score <= 50:
        category = "Moderate surveillance"
        explanation = "Surveillance is significant but not yet fully structuring everyday life."
    elif oss_score <= 75:
        category = "High behavioural adaptation"
        explanation = "Surveillance is strong and likely shaping behaviour, choices and self-expression."
    else:
        category = "Internalised surveillance"
        explanation = (
            "Surveillance appears deeply embedded and normalised, with strong potential "
            "for chilling effects and systemic control."
        )

    st.subheader("OSS Result")
    if system_name:
        st.write("**System:**", system_name)
    if location:
        st.write("**Location:**", location)

    st.metric("OSS Score (0–100)", oss_score)
    st.write(f"**Category:** {category}")
    st.write(explanation)

    # --- Radar chart of dimension scores ---
    st.subheader("Dimension Profile")

    categories = list(DIMENSIONS.keys())
    values = [scores[dim] for dim in categories]

    # Close the loop for radar
    categories_loop = categories + [categories[0]]
    values_loop = values + [values[0]]

    fig = px.line_polar(
        r=values_loop,
        theta=categories_loop,
        line_close=True,
        range_r=[0, 4],
        title="OSS Dimension Radar",
    )
    fig.update_traces(fill="toself")

    st.plotly_chart(fig, use_container_width=True)

  st.subheader("Download Report")

pdf_bytes = generate_pdf(
    system_name,
    location,
    oss_score,
    category,
    explanation,
    scores,
)

st.download_button(
    label="Download OSS Report as PDF",
    data=pdf_bytes,
    file_name="OSS_Report.pdf",
    mime="application/pdf"
)

