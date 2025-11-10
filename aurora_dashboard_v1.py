import streamlit as st
import folium
from streamlit_folium import st_folium
import base64
from streamlit.components.v1 import html

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="NatureMind AI Dashboard", layout="wide")

# ------------------------------
# SIDEBAR – LOGO + PARAMETERS
# ------------------------------
st.sidebar.image("nature_logo.png", use_container_width=True)
st.sidebar.markdown("### LLM & System Parameters")

# Use session state to persist submit action
if "submitted" not in st.session_state:
    st.session_state.submitted = False

query = st.sidebar.text_input(
    "User Query",
    placeholder="Enter your query (e.g., Analyze flood resilience for Oxfordshire flood zones)"
)
uploaded_file = st.sidebar.file_uploader("Upload PDF (Optional)", type=["pdf"])

if st.sidebar.button("Submit Query"):
    if query.strip():
        st.session_state.submitted = True
        st.sidebar.success(" Query submitted successfully!")
    else:
        st.sidebar.warning(" Please enter a valid query before submitting.")

# Only show indicators and map after submission
if st.session_state.submitted:
    confidence = st.sidebar.slider("LLM Confidence", 0.0, 1.0, 0.92)
    mode = "Auto" if confidence >= 0.6 else "Interactive"
    st.sidebar.write(f"**Mode:** {mode}")
    st.sidebar.write(f"**Location:** Oxfordshire, England")

    st.sidebar.divider()
    st.sidebar.markdown("####  Model Indicators")
    flood_risk = st.sidebar.slider("Flood Risk", 0.0, 1.0, 0.82)
    ndvi = st.sidebar.slider("NDVI (Vegetation Index)", 0.0, 1.0, 0.48)
    impervious = st.sidebar.slider("Imperviousness", 0.0, 1.0, 0.63)
    resilience = round(0.4 * (1 - flood_risk) + 0.3 * ndvi + 0.3 * (1 - impervious), 2)
    st.sidebar.metric("Resilience Score", resilience)
else:
    st.sidebar.info(" Please enter a query and click **Submit Query** to view indicators and the interactive map.")

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
# MAP TAB — appears only after submission
# ------------------------------
# ------------------------------
# MAP TAB — show clean Oxfordshire map only
# ------------------------------
with tab1:
    st.subheader("Interactive Map: Oxfordshire Wetland Sites")

    # Create the map centered on Oxfordshire
    m = folium.Map(location=[51.75, -1.25], zoom_start=9, tiles='OpenStreetMap')

    # Add circle markers instead of default icon markers (which sometimes break in Streamlit)
    folium.CircleMarker(
        location=[51.7041, -1.55257],
        radius=7,
        color='blue',
        fill=True,
        fill_color='blue',
        popup="Site 675 — 32.37 ha — High Suitability"
    ).add_to(m)

    folium.CircleMarker(
        location=[51.8259, -1.16916],
        radius=7,
        color='green',
        fill=True,
        fill_color='green',
        popup="Site 294 — 14.54 ha — Moderate Suitability"
    ).add_to(m)

    folium.CircleMarker(
        location=[51.7101, -1.49567],
        radius=7,
        color='orange',
        fill=True,
        fill_color='orange',
        popup="Site 607 — 10.50 ha — Balanced Benefits"
    ).add_to(m)

    # Display map in Streamlit
    st_folium(m, width=700, height=480)
# ------------------------------
# ANALYTICS TAB
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
            margin-left: 0 !important;
            margin-right: auto !important;
            text-align: justify;
            line-height: 1.55;
            padding-left: 0.3rem;
            padding-right: 0.3rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title-blue'> Compliance Evaluation</div>", unsafe_allow_html=True)
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
    st.subheader(" Flood Map Figures and Spatial Insights")

    col1, col2 = st.columns(2)
    with col1:
        st.image("flood_frequency_map.png", caption="Flood Frequency Distribution (Oxfordshire)", use_container_width=True)
    with col2:
        st.image("temporal_segmentation_map.png", caption="Temporal Segmentation Map (Pre- and Post-Flood Zones)", use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.image("finance_damage_by_asset.png", caption="Estimated Damages by Asset Type (€)", use_container_width=True)
    with col4:
        st.image("finance_damage_proportion1.png", caption="Proportion of Total Flood-Related Financial Damage (%)", use_container_width=True)

# ------------------------------
# REPORT TAB
# ------------------------------
with tab3:
    st.markdown("<div class='section-title-blue'> NatureMind Final Report - Executive Summary</div>", unsafe_allow_html=True)

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
            with open("NatureMind_Final_Report1.docx", "rb") as f:
                st.download_button(
                    label=" Download NatureMind Final Report",
                    data=f,
                    file_name="NatureMind_Final_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except FileNotFoundError:
            st.warning(" 'NatureMind_Final_Report.docx' not found in working directory.")

    with col2:
        st.markdown(" Temporal Flood Extent Evolution (1980–1990)")
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
                    </div>
                """
                html(gif_html, height=420)
        except FileNotFoundError:
            st.warning("️ 'wetlands_animation.gif' not found. Please ensure it's in the same directory.")

st.markdown("---")
st.caption("NatureMind AI © 2025 - Demo Dashboard for End-to-End Planning and Resilience Pipeline.")
