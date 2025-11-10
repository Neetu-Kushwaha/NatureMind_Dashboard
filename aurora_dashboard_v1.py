import streamlit as st
import folium
from streamlit_folium import st_folium
import base64
from streamlit.components.v1 import html
import time

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="NatureMind AI Dashboard", layout="wide")

# ------------------------------
# SESSION STATE
# ------------------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "status" not in st.session_state:
    st.session_state.status = "Idle"

# ------------------------------
# SIDEBAR – LOGO + PARAMETERS
# ------------------------------
st.sidebar.image("nature_logo.png", use_container_width=True)
st.sidebar.markdown("### LLM & System Parameters")

query = st.sidebar.text_input(
    "User Query",
    placeholder="Enter your query (e.g., Analyze flood resilience for Oxfordshire flood zones)"
)
uploaded_file = st.sidebar.file_uploader("Upload PDF (Optional)", type=["pdf"])

# if st.sidebar.button("Submit Query"):
#     if query.strip():
#         st.session_state.status = "Processing"
#         with st.spinner("Processing your query... Please wait ⏳"):
#             time.sleep(3)  # simulate model computation delay
#         st.session_state.submitted = True
#         st.session_state.status = "Ready"
#         st.sidebar.success("✅ Query processed successfully!")
#     else:
#         st.sidebar.warning("⚠️ Please enter a valid query before submitting.")


if st.sidebar.button("Submit Query"):
    if query.strip():
        st.session_state.status = "Processing"
        st.sidebar.info("Running NatureMind AI inference...")

        # Add a dynamic progress bar
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()

        for i in range(100):
            time.sleep(0.08)  # total ~8 seconds
            progress_bar.progress(i + 1)
            status_text.text(f"Processing... {i + 1}%")

        # Finish progress
        progress_bar.empty()
        status_text.text(" Processing complete!")

        st.session_state.submitted = True
        st.session_state.status = "Ready"
        st.sidebar.success(" Query processed successfully!")
    else:
        st.sidebar.warning("️ Please enter a valid query before submitting.")

# ------------------------------
# SIDEBAR METRICS
# ------------------------------
if st.session_state.submitted:
    confidence = st.sidebar.slider("LLM Confidence", 0.0, 1.0, 0.92)
    mode = "Auto" if confidence >= 0.6 else "Interactive"
    st.sidebar.write(f"**Mode:** {mode}")
    st.sidebar.write(f"**Location:** Oxfordshire, England")

    st.sidebar.divider()
    st.sidebar.markdown("#### Model Indicators")
    flood_risk = st.sidebar.slider("Flood Risk", 0.0, 1.0, 0.82)
    ndvi = st.sidebar.slider("NDVI (Vegetation Index)", 0.0, 1.0, 0.48)
    impervious = st.sidebar.slider("Imperviousness", 0.0, 1.0, 0.63)
    resilience = round(0.4 * (1 - flood_risk) + 0.3 * ndvi + 0.3 * (1 - impervious), 2)
    st.sidebar.metric("Resilience Score", resilience)
else:
    st.sidebar.info("Please enter a query and click **Submit Query** to view indicators and the interactive map.")

# ------------------------------
# STATUS INDICATOR (TOP-LEFT BADGE)
# ------------------------------
status_colors = {"Idle": "#6c757d", "Processing": "#f0ad4e", "Ready": "#5cb85c"}
st.markdown(
    f"""
    <div style="
        position: fixed;
        top: 10px;
        left: 10px;
        background-color: {status_colors[st.session_state.status]};
        color: white;
        padding: 8px 14px;
        border-radius: 12px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
        z-index: 1000;">
        Status: {st.session_state.status}
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# MAIN PAGE HEADER
# ------------------------------
st.markdown("""
    <style>
    .main-header {
        text-align: left;
        font-size: 44px;
        font-weight: 800;
        color: #222;
        margin-bottom: 0px;
        line-height: 1.15;
    }
    .sub-header {
        text-align: left;
        font-size: 16px;
        color: #444;
        margin-top: 6px;
        line-height: 1.45;
        max-width: 900px;
    }
    </style>

    <div class="main-header">
         NatureMind AI - Oxfordshire Flood Resilience & Planning Dashboard (Demo)
    </div>
    <div class="sub-header">
        This dashboard presents <strong>environmental, economic, and compliance insights</strong> derived from the 
        <em>NatureMind Final Report (2025)</em> on Oxfordshire flood resilience and planning.
    </div>
""", unsafe_allow_html=True)

# ------------------------------
# TABS
# ------------------------------
tab1, tab2, tab3 = st.tabs([" Map View", " Analytics", " Report Summary"])

# ------------------------------
# TAB 1 — INTERACTIVE MAP
# ------------------------------
with tab1:
    st.subheader("Interactive Map: Oxfordshire Wetland Sites")

    if st.session_state.submitted:
        # Create map only after query submission
        m = folium.Map(location=[51.75, -1.25], zoom_start=9)

        folium.CircleMarker(
            [51.7041, -1.55257],
            radius=7, color='blue', fill=True, fill_color='blue',
            popup="Site 675 — 32.37 ha — High Suitability"
        ).add_to(m)

        folium.CircleMarker(
            [51.8259, -1.16916],
            radius=7, color='green', fill=True, fill_color='green',
            popup="Site 294 — 14.54 ha — Moderate Suitability"
        ).add_to(m)

        folium.CircleMarker(
            [51.7101, -1.49567],
            radius=7, color='orange', fill=True, fill_color='orange',
            popup="Site 607 — 10.50 ha — Balanced Benefits"
        ).add_to(m)

        st_folium(m, width=700, height=480)
    else:
        st.info("💡 Enter a query in the sidebar and click **Submit Query** to load the interactive map.")

# ------------------------------
# TAB 2 — ANALYTICS
# ------------------------------
with tab2:
    st.markdown("""
        <style>
        .section-title-blue {
            font-size: 22px !important;
            font-weight: 700;
            border-bottom: 2px solid #B0C4DE;
            padding-bottom: 4px;
            color: #003366;
            margin-top: 1.2em;
        }
        .section-title-green {
            font-size: 22px !important;
            font-weight: 700;
            border-bottom: 2px solid #A3C1AD;
            padding-bottom: 4px;
            color: #006400;
            margin-top: 1.2em;
        }
        .content-text {
            width: 100%;
            max-width: 1000px;
            text-align: justify;
            line-height: 1.55;
            padding-left: 0.3rem;
            padding-right: 0.3rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title-blue'>Compliance Evaluation</div>", unsafe_allow_html=True)
    st.metric("Compliance Score", "0.85", "Fully Compliant")

    st.markdown("""
    <div class='content-text'>
    <strong>Summary:</strong> Policy alignment verified with <em>Flood & Water Management Act (2010)</em> and
    <em>Climate Change Act (2008)</em>. The Nature-based Solutions (NbS) framework is fully compliant with
    Oxfordshire’s sustainable drainage and resilience strategies.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='content-text'>
    <strong>Recommendations:</strong>
    <ul>
        <li>Expand wetlands and woodland buffers</li>
        <li>Incentivize NbS adoption in land-use planning</li>
        <li>Integrate NbS into local infrastructure upgrades</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-title-green'>Infrastructure & Economic Impact Overview</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='content-text'>
    Flood events in Oxfordshire have the greatest effect on <strong>roads</strong> and <strong>railways</strong>,
    which together account for over <strong>95% of total economic losses</strong>. Projected damages rise
    substantially by 2080 due to climate change, highlighting the urgency of resilience planning.
    <br><br>
    <strong>Nature-based solutions (NbS)</strong> such as wetlands and woodlands have proven effective
    in attenuating these impacts, demonstrating the value of ecological flood management.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Flood Map Figures and Spatial Insights")

    col1, col2 = st.columns(2)
    with col1:
        st.image("flood_frequency_map.png", caption="Flood Frequency Distribution (Oxfordshire)", use_container_width=True)
    with col2:
        st.image("temporal_segmentation_map.png", caption="Temporal Segmentation Map (Pre- and Post-Flood Zones)", use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.image("finance_damage_by_asset.png", caption="Estimated Damages by Asset Type (€)", use_container_width=True)
    with col4:
        st.image("finance_damage_proportion.png", caption="Proportion of Total Flood-Related Financial Damage (%)", use_container_width=True)

# ------------------------------
# TAB 3 — REPORT SUMMARY
# ------------------------------
with tab3:
    st.markdown("<div class='section-title-blue'>NatureMind Final Report - Executive Summary</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.25, 1])

    with col1:
        st.markdown("""
        The proposed wetland interventions across Oxfordshire focus on hydrologically sensitive regions where 
        flood risk mitigation and ecosystem restoration align most effectively. The three identified sites - 
        <strong>Proposal 675 (32.3 ha)</strong>, <strong>Proposal 294 (14.5 ha)</strong>, and 
        <strong>Proposal 607 (10.5 ha)</strong> - were selected based on suitability scores from 
        NatureMind’s environmental risk model.  
        <br><br>
        These wetlands contribute to:<br>
        • Reduced surface runoff in high flood-frequency zones.<br>
        • Improved ecological balance through vegetation regeneration.<br>
        • Increased resilience for adjacent transport and agricultural infrastructure.
        """, unsafe_allow_html=True)

        try:
            with open("NatureMind_Final_Report.docx", "rb") as f:
                st.download_button(
                    label=" Download NatureMind Final Report",
                    data=f,
                    file_name="NatureMind_Final_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except FileNotFoundError:
            st.warning("️ 'NatureMind_Final_Report.docx' not found in working directory.")

    with col2:
        st.markdown("Temporal Flood Extent Evolution (1980–2021)")
        gif_path = "wetlands_animation.gif"
        try:
            with open(gif_path, "rb") as f:
                gif_bytes = f.read()
                b64 = base64.b64encode(gif_bytes).decode()
                gif_html = f"""
                    <div style='text-align:center;'>
                        <img src='data:image/gif;base64,{b64}' alt='Flood Animation'
                             style='width:100%; height:auto; border-radius:10px;' />
                        <p style='font-size:14px; color:#555; margin-top:5px;'>
                            Historical flood extent dynamics across Oxfordshire — illustrating spatial expansion of flood zones up to 1990.
                        </p>
                    </div>Processing your query... Please wait 
                """
                html(gif_html, height=420)
        except FileNotFoundError:
            st.warning("️ 'wetlands_animation.gif' not found. Please ensure it's in the same directory.")

st.markdown("---")
st.caption("NatureMind AI © 2025 - Demo Dashboard for End-to-End Planning and Resilience Pipeline.")
