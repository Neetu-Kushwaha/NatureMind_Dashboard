import streamlit as st
import folium
from streamlit_folium import st_folium
import base64
from streamlit.components.v1 import html
from streamlit.components.v1 import html
# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="NatureMind AI Dashboard", layout="wide")

# ------------------------------
# SIDEBAR – LOGO + PARAMETERS
# ------------------------------
st.sidebar.image("nature_logo.png", use_container_width=True)
st.sidebar.markdown("### 🔧 LLM & System Parameters")

query = st.sidebar.text_input("User Query", "Analyze flood resilience for Oxfordshire flood zones")
uploaded_file = st.sidebar.file_uploader("Upload PDF (Optional)", type=["pdf"])
if st.sidebar.button("Submit Query"):
    st.sidebar.success("Query submitted successfully!")

confidence = st.sidebar.slider("LLM Confidence", 0.0, 1.0, 0.92)
mode = "Auto" if confidence >= 0.6 else "Interactive"
st.sidebar.write(f"**Mode:** {mode}")
st.sidebar.write(f"**Location:** Oxfordshire, England")

st.sidebar.divider()
st.sidebar.markdown("#### Model Indicators")
flood_risk = st.sidebar.slider("Flood Risk", 0.0, 1.0, 0.82)
ndvi = st.sidebar.slider("NDVI (Vegetation Index)", 0.0, 1.0, 0.48)
impervious = st.sidebar.slider("Imperviousness", 0.0, 1.0, 0.63)
resilience = round(0.4*(1-flood_risk) + 0.3*(ndvi) + 0.3*(1-impervious), 2)
st.sidebar.metric("Resilience Score", resilience)

# ------------------------------
# MAIN PAGE
# ------------------------------
# st.title(" NatureMind AI - Oxfordshire Flood Resilience & Planning Dashboard (Demo)")
# st.markdown("""
# This dashboard presents **environmental, economic, and compliance insights** derived from
# the *NatureMind Final Report (2025)* on Oxfordshire flood resilience and planning.
# """)

# ------------------------------
# CUSTOM HEADER STYLE — PERFECT LEFT ALIGNMENT
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
        font-size: 18px;
        color: #444;
        margin-top: 6px;
        line-height: 1.45;
        max-width: 900px;
    }
    </style>

    <div class="main-header">
        🌍 NatureMind AI — Oxfordshire Flood Resilience & Planning Dashboard (Demo)
    </div>
    <div class="sub-header">
        This dashboard presents <strong>environmental, economic, and compliance insights</strong> derived from the 
        <em>NatureMind Final Report (2025)</em> on Oxfordshire flood resilience and planning.
    </div>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs([" Map View", "Analytics", " Report Summary"])

# ------------------------------
# MAP TAB
# ------------------------------
with tab1:
    st.subheader(" Interactive Map: Oxfordshire Wetland Sites")
    m = folium.Map(location=[51.75, -1.25], zoom_start=9)
    folium.Marker([51.7041, -1.55257], popup="Site 675 — 32.37 ha — High Suitability").add_to(m)
    folium.Marker([51.8259, -1.16916], popup="Site 294 — 14.54 ha — Moderate Suitability").add_to(m)
    folium.Marker([51.7101, -1.49567], popup="Site 607 — 10.50 ha — Balanced Benefits").add_to(m)
    st_folium(m, width=700, height=480)

# ------------------------------
# ANALYTICS TAB (color-coded + maps)
# ------------------------------
with tab2:
    # Styles
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
        .rec-list {
            margin-top: 0.4em;
            margin-left: 1.5em;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---- Compliance Evaluation ----
    st.markdown("<div class='section-title-blue'>️ Compliance Evaluation</div>", unsafe_allow_html=True)
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
    <ul class='rec-list'>
        <li>Expand wetlands and woodland buffers</li>
        <li>Incentivize NbS adoption in land-use planning</li>
        <li>Integrate NbS into local infrastructure upgrades</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ---- Infrastructure & Economic Impact Overview ----
    st.markdown("<div class='section-title-green'> Infrastructure & Economic Impact Overview</div>", unsafe_allow_html=True)
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

    # ---- Flood Map Figures ----
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
        st.image("finance_damage_proportion.png", caption="Proportion of Total Flood-Related Financial Damage (%)", use_container_width=True)

    st.markdown("""
    <div class='content-text'>
    <strong>Interpretation:</strong> These figures illustrate flood exposure, temporal variation, and economic
    damage distribution across Oxfordshire based on hydrological projections.
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# REPORT TAB (aligned text + map + download)
# ------------------------------
with tab3:
    st.markdown("""
        <style>
        .report-text {
            text-align: justify;
            line-height: 1.6;
            max-width: 900px;
            padding-right: 1rem;
        }
        .report-title {
            font-size: 22px;
            font-weight: 700;
            color: #003366;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='report-title'> NatureMind Final Report — Executive Summary</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.25, 1])

    with col1:
        st.markdown("""
        <div class='report-text'>
        The proposed wetland interventions across Oxfordshire focus on hydrologically sensitive regions where 
        flood risk mitigation and ecosystem restoration align most effectively. The three identified sites - 
        <strong>Proposal 675 (32.3 ha)</strong> near western Oxford, <strong>Proposal 294 (14.5 ha)</strong> 
        in the northeast corridor, and <strong>Proposal 607 (10.5 ha)</strong> in the southwest — were selected 
        based on suitability scores from NatureMind’s environmental risk model.  

        These wetlands contribute to:
        <ul>
        <li><strong>Reduced surface runoff</strong> in high flood-frequency zones.</li>
        <li><strong>Improved ecological balance</strong> through vegetation regeneration.</li>
        <li><strong>Increased resilience</strong> for adjacent transport and agricultural infrastructure.</li>
        </ul>

        The selection integrates geospatial hydrology, vegetation indices, and impervious surface mapping, 
        ensuring a balance between flood management and biodiversity gain. Each proposal aligns with Oxfordshire’s 
        climate resilience strategy and demonstrates the value of evidence-based Nature-based Solutions (NbS).
        </div>
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
            st.warning("NatureMind_Final_Report.docx not found in working directory.")

    # with col2:
    #     st.markdown("** Proposed Wetlands Map**")
    #     try:
    #         with open("oxfordshire_planner_map_evt2755.html", "r", encoding="utf-8") as f:
    #             html(f.read(), height=450, scrolling=True)
    #     except FileNotFoundError:
    #         st.warning("️ The file 'oxfordshire_planner_map_evt2755.html' was not found. Please ensure it’s in the same directory as this script.")


    with col2:
        st.markdown("Temporal Flood Extent Evolution (1980–1990)")

        gif_path = "wetlands_animation.gif"
        try:
            with open(gif_path, "rb") as f:
                gif_bytes = f.read()
                b64 = base64.b64encode(gif_bytes).decode()
                gif_html = f"""
                    <div style='text-align:center;'>
                        <img src='data:image/gif;base64,{b64}' alt='Wetland Simulation'
                             style='width:100%; height:auto; border-radius:10px;' />
                        <p style='font-size:14px; color:#555; margin-top:5px;'>
                            Evolution of Proposed Wetlands — Oxfordshire
                        </p>
                    </div>
                """
                html(gif_html, height=420)
        except FileNotFoundError:
            st.warning(
                "⚠️ 'wetlands_animation.gif' not found. Please ensure it's in the same directory as this script.")

    st.markdown("""
    <div class='report-text'>
    <strong>Summary:</strong>  
    The integrated NbS proposals highlight Oxfordshire’s proactive approach to combining 
    flood mitigation, ecological sustainability, and economic adaptation within its policy framework.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("NatureMind AI © 2025 — Demo Dashboard for End-to-End Planning and Resilience Pipeline.")
