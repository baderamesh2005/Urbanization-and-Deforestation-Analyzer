import streamlit as st
import folium
from streamlit_folium import st_folium
from ee_analysis import analyze_city

st.set_page_config(
    page_title="Urbanization and Deforestation Analyzer",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
/* Main app background */
.stApp {
    background: linear-gradient(135deg, #eef6ff 0%, #f7fbff 40%, #f4fff8 100%);
}

/* Remove default top spacing a little */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Main title card */
.hero-box {
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 50%, #059669 100%);
    padding: 28px 32px;
    border-radius: 22px;
    color: white;
    box-shadow: 0 12px 32px rgba(0,0,0,0.18);
    margin-bottom: 22px;
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 1.05rem;
    opacity: 0.95;
}

/* Section titles */
.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #0f172a;
    margin-top: 10px;
    margin-bottom: 12px;
}

/* Pretty cards */
.pretty-card {
    background: rgba(255,255,255,0.92);
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(226, 232, 240, 0.8);
    margin-bottom: 18px;
}

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
    border-left: 7px solid #2563eb;
    margin-bottom: 14px;
}

.metric-card.green {
    border-left-color: #16a34a;
}

.metric-card.red {
    border-left-color: #dc2626;
}

.metric-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 8px;
}

.metric-line {
    font-size: 0.98rem;
    color: #334155;
    margin-bottom: 4px;
}

.big-number {
    font-size: 1.35rem;
    font-weight: 800;
    color: #111827;
}

/* Summary box */
.summary-box {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #dbeafe;
    box-shadow: 0 8px 18px rgba(59, 130, 246, 0.10);
    color: #1e293b;
    line-height: 1.7;
}

/* Input helper box */
.input-box {
    background: rgba(255,255,255,0.88);
    border-radius: 20px;
    padding: 18px 20px;
    border: 1px solid #dbeafe;
    box-shadow: 0 8px 18px rgba(15,23,42,0.05);
    margin-bottom: 18px;
}

/* Map note */
.map-note {
    background: linear-gradient(135deg, #eff6ff 0%, #ecfeff 100%);
    border-radius: 14px;
    padding: 14px 16px;
    border: 1px solid #bfdbfe;
    color: #0f172a;
    font-size: 0.96rem;
}

/* Footer */
.footer-box {
    text-align: center;
    color: #475569;
    font-size: 0.95rem;
    padding: 18px 0 5px 0;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #059669 100%);
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.4rem;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.28);
}

.stButton > button:hover {
    color: white;
    border: none;
    transform: translateY(-1px);
}

/* Select boxes */
div[data-baseweb="select"] > div {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🌍 Urbanization and Deforestation Analyzer</div>
    <div class="hero-subtitle">
        Compare forest and urban land-cover changes across cities and years using Google Earth Engine,
        satellite imagery, and an interactive map dashboard.
    </div>
</div>
""", unsafe_allow_html=True)

cities = ["Pune", "Mumbai", "Delhi"]
years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]

dw_palette = [
    "419BDF",  # water
    "397D49",  # trees
    "88B053",  # grass
    "7A87C6",  # flooded vegetation
    "E49635",  # crops
    "DFC35A",  # shrub & scrub
    "C4281B",  # built-up
    "A59B8F",  # bare ground
    "B39FE1",  # snow & ice
]

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = None

# -----------------------------
# INPUT SECTION
# -----------------------------
st.markdown('<div class="section-title">⚙️ Analysis Controls</div>', unsafe_allow_html=True)
st.markdown('<div class="input-box">', unsafe_allow_html=True)

col_a, col_b, col_c, col_d = st.columns([1.2, 1, 1, 0.8])

with col_a:
    city = st.selectbox("Select City", cities)

with col_b:
    old_year = st.selectbox("Select Old Year", years, index=0)

with col_c:
    new_year = st.selectbox("Select New Year", years, index=6)

with col_d:
    st.write("")
    st.write("")
    analyze_clicked = st.button("🔍 Analyze")

st.markdown('</div>', unsafe_allow_html=True)

if new_year <= old_year:
    st.error("New year must be greater than old year.")
else:
    if analyze_clicked:
        with st.spinner("Analyzing satellite data and building map layers..."):
            try:
                result = analyze_city(city, old_year, new_year)
                st.session_state.analysis_result = result
                st.session_state.last_inputs = {
                    "city": city,
                    "old_year": old_year,
                    "new_year": new_year,
                }
            except Exception as e:
                st.error(f"Error: {str(e)}")

# -----------------------------
# RESULTS
# -----------------------------
if st.session_state.analysis_result is not None:
    result = st.session_state.analysis_result
    saved_inputs = st.session_state.last_inputs

    st.success("Analysis completed successfully")

    st.markdown('<div class="section-title">📌 Selected Inputs</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pretty-card">
        <b>City:</b> {saved_inputs['city']} &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
        <b>Old Year:</b> {saved_inputs['old_year']} &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
        <b>New Year:</b> {saved_inputs['new_year']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📊 Change Metrics</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card green">
            <div class="metric-title">🌳 Forest Area</div>
            <div class="metric-line">{result['old_year']}: <span class="big-number">{result['forest_old_sqkm']:.2f}</span> sq km</div>
            <div class="metric-line">{result['new_year']}: <span class="big-number">{result['forest_new_sqkm']:.2f}</span> sq km</div>
            <div class="metric-line"><b>Deforestation:</b> {result['deforestation_percent']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card red">
            <div class="metric-title">🏙️ Urban Area</div>
            <div class="metric-line">{result['old_year']}: <span class="big-number">{result['urban_old_sqkm']:.2f}</span> sq km</div>
            <div class="metric-line">{result['new_year']}: <span class="big-number">{result['urban_new_sqkm']:.2f}</span> sq km</div>
            <div class="metric-line"><b>Urban Growth:</b> {result['urban_growth_percent']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📝 Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary-box">
        In <b>{result['city']}</b>, forest area changed from <b>{result['forest_old_sqkm']:.2f} sq km</b>
        to <b>{result['forest_new_sqkm']:.2f} sq km</b>, while urban area changed from
        <b>{result['urban_old_sqkm']:.2f} sq km</b> to <b>{result['urban_new_sqkm']:.2f} sq km</b>.
        This comparison highlights the land-cover transition between <b>{result['old_year']}</b> and
        <b>{result['new_year']}</b>.
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # MAP
    # -----------------------------
    center_lat, center_lon = result["center"]
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10, tiles="OpenStreetMap")

    satellite_map_id = result["s2_new"].getMapId({
        "bands": ["B4", "B3", "B2"],
        "min": 0,
        "max": 3000
    })
    folium.TileLayer(
        tiles=satellite_map_id["tile_fetcher"].url_format,
        attr="Google Earth Engine",
        name=f"Satellite {result['new_year']}",
        overlay=True,
        control=True
    ).add_to(m)

    old_lc_map_id = result["dw_old"].getMapId({
        "min": 0,
        "max": 8,
        "palette": dw_palette
    })
    folium.TileLayer(
        tiles=old_lc_map_id["tile_fetcher"].url_format,
        attr="Google Earth Engine",
        name=f"Land Cover {result['old_year']}",
        overlay=True,
        control=True
    ).add_to(m)

    new_lc_map_id = result["dw_new"].getMapId({
        "min": 0,
        "max": 8,
        "palette": dw_palette
    })
    folium.TileLayer(
        tiles=new_lc_map_id["tile_fetcher"].url_format,
        attr="Google Earth Engine",
        name=f"Land Cover {result['new_year']}",
        overlay=True,
        control=True
    ).add_to(m)

    forest_loss_map_id = result["forest_loss"].getMapId({
        "palette": ["yellow"]
    })
    folium.TileLayer(
        tiles=forest_loss_map_id["tile_fetcher"].url_format,
        attr="Google Earth Engine",
        name="Forest Loss",
        overlay=True,
        control=True
    ).add_to(m)

    urban_gain_map_id = result["urban_gain"].getMapId({
        "palette": ["red"]
    })
    folium.TileLayer(
        tiles=urban_gain_map_id["tile_fetcher"].url_format,
        attr="Google Earth Engine",
        name="Urban Gain",
        overlay=True,
        control=True
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    # Legend
    legend_html = """
    <div style="
        position: fixed;
        bottom: 40px;
        left: 40px;
        width: 230px;
        background-color: white;
        border: 2px solid #cbd5e1;
        z-index: 9999;
        font-size: 14px;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    ">
    <b>🗺️ Map Legend</b><br><br>

    <b>Change Layers</b><br>
    <i style="background:yellow; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Forest Loss<br>
    <i style="background:red; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Urban Gain<br><br>

    <b>Land Cover</b><br>
    <i style="background:#419BDF; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Water<br>
    <i style="background:#397D49; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Trees / Forest<br>
    <i style="background:#88B053; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Grass<br>
    <i style="background:#7A87C6; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Flooded Vegetation<br>
    <i style="background:#E49635; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Crops<br>
    <i style="background:#DFC35A; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Shrub & Scrub<br>
    <i style="background:#C4281B; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Built-up / Urban<br>
    <i style="background:#A59B8F; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Bare Ground<br>
    <i style="background:#B39FE1; width:14px; height:14px; display:inline-block; margin-right:8px;"></i> Snow / Ice<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    st.markdown('<div class="section-title">🗺️ Interactive Map</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="map-note">
        Use the map layer control to switch between Satellite, Land Cover, Forest Loss, and Urban Gain.
        Zoom and pan to inspect local change more clearly.
    </div>
    """, unsafe_allow_html=True)

    st_folium(m, width=1200, height=680, returned_objects=[])

    st.markdown("""
    <div class="footer-box">
        Built with ❤️ using Streamlit, Folium, and Google Earth Engine
    </div>
    """, unsafe_allow_html=True)
 #PS D:\> cd D:\DL-Urbanization-App
#PS D:\DL-Urbanization-App> .venv\Scripts\python.exe -m streamlit run app.py

