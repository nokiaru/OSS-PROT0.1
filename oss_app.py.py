import streamlit as st

st.set_page_config(page_title="Orwellian Surveillance Scale (OSS)", layout="centered")

st.title("Orwellian Surveillance Scale (OSS) – Prototype")
st.write(
    "This tool lets you score a surveillance system on several dimensions and "
    "produces an overall *Orwellian surveillance* index from 0 to 100."
)

# --- Define core dimensions and short descriptions ---
DIMENSIONS = {
    "Visibility / Monitoring": "How constantly and pervasively are people observed or tracked?",
    "Predictive Control": "To what extent is data used to predict and pre-empt behaviour?",
    "Self-Censorship": "Do people change or limit what they say or do because they feel watched?",
    "Datafication": "How fully are people reduced to data points, profiles or risk scores?",
    "Trust in State / Institutions": "How much power over data and surveillance is given to state or major institutions?",
    "Resignation / Normalisation": "Do people feel that surveillance is inevitable and unchangeable?"
}

# Optional theoretical weights – you can tweak these later
WEIGHTS = {
    "Visibility / Monitoring": 1.2,
    "Predictive Control": 1.3,
    "Self-Censorship": 1.5,
    "Datafication": 1.1,
    "Trust in State / Institutions": 1.0,
    "Resignation / Normalisation": 0.9
}

MAX_SCORE_PER_DIM = 4 # 0–4 Likert scale

with st.form("oss_form"):
    st.subheader("1. System being assessed")
    system_name = st.text_input("Name or short description of the system/technology")
    location = st.text_input("Country / location (optional)")
    
    st.markdown("### 2. Rate each dimension from 0 to 4")
    st.markdown(
        "**0 = Not present · 1 = Very weak · 2 = Moderate · 3 = Strong · 4 = Extreme / totalising**"
    )

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

if submitted:
    # --- Calculate weighted score ---
    weighted_sum = 0
    max_weighted_sum = 0

    for dim, score in scores.items():
        w = WEIGHTS[dim]
        weighted_sum += score * w
        max_weighted_sum += MAX_SCORE_PER_DIM * w

    if max_weighted_sum > 0:
        oss_index = round((weighted_sum / max_weighted_sum) * 100, 1)
    else:
        oss_index = 0.0

    # --- Classify the level of Orwellian surveillance ---
    if oss_index <= 25:
        category = "Low surveillance"
        explanation = "Surveillance is present but limited in scope or intensity."
    elif oss_index <= 50:
        category = "Moderate surveillance"
        explanation = "Surveillance is significant but not yet fully structuring everyday life."
    elif oss_index <= 75:
        category = "High behavioural adaptation"
        explanation = "Surveillance is strong and likely shaping behaviour, choices and self-expression."
    else:
        category = "Internalised surveillance"
        explanation = (
            "Surveillance appears deeply embedded and normalised, with strong potential "
            "for chilling effects and systemic control."
        )

    st.subheader("Results")
    if system_name:
        st.write(f"**System assessed:** {system_name}")
    if location:
        st.write(f"**Location:** {location}")

    st.metric("OSS Index (0–100)", oss_index)
    st.write(f"**Category:** {category}")
    st.write(explanation)

    st.subheader("Dimension breakdown")
    for dim, score in scores.items():
        st.write(f"- **{dim}**: {score} / 4 (weight {WEIGHTS[dim]})")

    st.info(
        "This is an early prototype of the OSS. In your dissertation, you can explain the "
        "theoretical basis of each dimension and how the weights and thresholds were chosen."
    )