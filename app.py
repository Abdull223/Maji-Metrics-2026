import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="MAJI METRICS | Vision 2030", layout="wide", page_icon="🇰🇪")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #ffffff; }
    
    [data-testid="stMetricValue"] { 
        color: #ffffff !important; 
        font-weight: 800 !important; 
        font-size: 1.8rem !important; 
        white-space: normal !important; 
        word-break: break-word !important;
        line-height: 1.2 !important;
    }
    
    [data-testid="stMetricLabel"] { color: #ffd700 !important; font-size: 1rem !important; font-weight: 600; }
    h1, h2, h3 { color: #ffd700 !important; }
    .report-box { background: #0f172a; border: 1px solid #38bdf8; padding: 35px; border-radius: 12px; font-family: 'Courier New', monospace; color: #38bdf8; line-height: 1.7; border-left: 5px solid #ffd700; white-space: pre-wrap; }
    .vision-card { background: rgba(255, 215, 0, 0.1); border-left: 5px solid #ffd700; padding: 15px; margin: 10px 0; border-radius: 5px; }
    .explanation-text { background: rgba(56, 189, 248, 0.1); padding: 15px; border-radius: 8px; border: 1px solid #38bdf8; margin-top: 10px; font-size: 0.95rem; line-height: 1.5; }
    .insight-box { background: #1e293b; border: 1px solid #ffd700; padding: 20px; border-radius: 10px; margin: 20px 0; }
    
    /* Water Falling Animation */
    .rain-container { position: relative; height: 200px; background: rgba(56, 189, 248, 0.05); overflow: hidden; border-radius: 15px; border-bottom: 3px solid #38bdf8; margin-bottom: 25px; }
    .drop { position: absolute; bottom: 100%; width: 2px; height: 25px; background: linear-gradient(to bottom, rgba(255,255,255,0), #38bdf8); animation: fall 1s linear infinite; }
    @keyframes fall { to { transform: translateY(280px); } }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NATIONAL DATASET ---
@st.cache_data
def get_national_context():
    return {
        "Baringo": {"coords": [0.4833, 35.9667], "risk_mod": 1.5, "pop_served": 666763},
        "Bomet": {"coords": [-0.7813, 35.3416], "risk_mod": 1.2, "pop_served": 875689},
        "Bungoma": {"coords": [0.5695, 34.5584], "risk_mod": 1.3, "pop_served": 1670570},
        "Busia": {"coords": [0.4608, 34.1115], "risk_mod": 1.4, "pop_served": 893681},
        "Elgeyo-Marakwet": {"coords": [0.8000, 35.5000], "risk_mod": 1.3, "pop_served": 454480},
        "Embu": {"coords": [-0.5319, 37.4513], "risk_mod": 1.2, "pop_served": 608599},
        "Garissa": {"coords": [-0.4532, 39.6461], "risk_mod": 1.7, "pop_served": 841353},
        "Homa Bay": {"coords": [-0.5273, 34.4571], "risk_mod": 1.4, "pop_served": 1131950},
        "Isiolo": {"coords": [0.3546, 38.4851], "risk_mod": 1.7, "pop_served": 268002},
        "Kajiado": {"coords": [-2.0981, 36.7753], "risk_mod": 1.5, "pop_served": 1117840},
        "Kakamega": {"coords": [0.2827, 34.7519], "risk_mod": 1.2, "pop_served": 1867579},
        "Kericho": {"coords": [-0.3677, 35.2827], "risk_mod": 1.1, "pop_served": 901777},
        "Kiambu": {"coords": [-1.1462, 36.8531], "risk_mod": 1.0, "pop_served": 2417735},
        "Kilifi": {"coords": [-3.5107, 39.9093], "risk_mod": 1.5, "pop_served": 1453787},
        "Kirinyaga": {"coords": [-0.4991, 37.3000], "risk_mod": 1.1, "pop_served": 610411},
        "Kisii": {"coords": [-0.6773, 34.7796], "risk_mod": 1.1, "pop_served": 1266860},
        "Kisumu": {"coords": [-0.1022, 34.7617], "risk_mod": 1.2, "pop_served": 1155574},
        "Kitui": {"coords": [-1.3750, 38.0106], "risk_mod": 1.6, "pop_served": 1136187},
        "Kwale": {"coords": [-4.1742, 39.4442], "risk_mod": 1.5, "pop_served": 866820},
        "Laikipia": {"coords": [0.3601, 36.7860], "risk_mod": 1.4, "pop_served": 518560},
        "Lamu": {"coords": [-2.2717, 40.9020], "risk_mod": 1.6, "pop_served": 143920},
        "Machakos": {"coords": [-1.5177, 37.2634], "risk_mod": 1.3, "pop_served": 1421932},
        "Makueni": {"coords": [-1.7851, 37.6253], "risk_mod": 1.4, "pop_served": 987653},
        "Mandera": {"coords": [3.9366, 41.8569], "risk_mod": 1.8, "pop_served": 867457},
        "Marsabit": {"coords": [2.3333, 37.9833], "risk_mod": 1.7, "pop_served": 459785},
        "Meru": {"coords": [0.0463, 37.6498], "risk_mod": 1.1, "pop_served": 1545714},
        "Migori": {"coords": [-1.0634, 34.4731], "risk_mod": 1.3, "pop_served": 1116469},
        "Mombasa": {"coords": [-4.0435, 39.6682], "risk_mod": 1.5, "pop_served": 1208333},
        "Murang'a": {"coords": [-0.7211, 37.1528], "risk_mod": 1.1, "pop_served": 1056640},
        "Nairobi": {"coords": [-1.2863, 36.8172], "risk_mod": 1.1, "pop_served": 4397073},
        "Nakuru": {"coords": [-0.3031, 36.0800], "risk_mod": 1.2, "pop_served": 2162202},
        "Nandi": {"coords": [0.1833, 35.1167], "risk_mod": 1.1, "pop_served": 885711},
        "Narok": {"coords": [-1.0833, 35.8667], "risk_mod": 1.4, "pop_served": 1157873},
        "Nyamira": {"coords": [-0.5633, 34.9358], "risk_mod": 1.1, "pop_served": 605576},
        "Nyandarua": {"coords": [-0.3333, 36.4833], "risk_mod": 1.1, "pop_served": 638289},
        "Nyeri": {"coords": [-0.4167, 36.9500], "risk_mod": 1.0, "pop_served": 759164},
        "Samburu": {"coords": [1.2167, 36.7667], "risk_mod": 1.7, "pop_served": 310327},
        "Siaya": {"coords": [0.0607, 34.2882], "risk_mod": 1.3, "pop_served": 993183},
        "Taita-Taveta": {"coords": [-3.4000, 38.3500], "risk_mod": 1.4, "pop_served": 340671},
        "Tana River": {"coords": [-1.5000, 40.0000], "risk_mod": 1.7, "pop_served": 315943},
        "Tharaka-Nithi": {"coords": [-0.3000, 37.9000], "risk_mod": 1.2, "pop_served": 393177},
        "Trans Nzoia": {"coords": [1.0211, 34.9547], "risk_mod": 1.2, "pop_served": 990341},
        "Turkana": {"coords": [3.1162, 35.5966], "risk_mod": 1.9, "pop_served": 926976},
        "Uasin Gishu": {"coords": [0.5209, 35.2691], "risk_mod": 1.1, "pop_served": 1163186},
        "Vihiga": {"coords": [0.0104, 34.7251], "risk_mod": 1.1, "pop_served": 590013},
        "Wajir": {"coords": [1.7471, 40.0596], "risk_mod": 1.8, "pop_served": 781263},
        "West Pokot": {"coords": [1.5000, 35.1000], "risk_mod": 1.6, "pop_served": 621241}
    }

county_data = get_national_context()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("Project Team")
    team = [
        {"n": "Abdullahi Hassan", "r": "Lead Statistician", "i": "Abdul.jpg"},
        {"n": "Claire", "r": "Data Architect", "i": "Claire.jpg"},
        {"n": "Yvonne", "r": "Feature Engineer", "i": "Yvonnes.jpg"},
        {"n": "Ahmed", "r": "ML Engineer", "i": "Ahmed.jpg"},
        {"n": "Lauren", "r": "Visualization Specialist", "i": "Lauren.jpg"},
        {"n": "Samantha", "r": "Pipeline Engineer", "i": "samantha.jpg"}
    ]
    for m in team:
        c1, c2 = st.columns([1, 3])
        with c1:
            try: st.image(m["i"], width=50)
            except: st.write("👤")
        with c2: st.caption(f"**{m['n']}**\n{m['r']}")

    st.divider()
    st.header("Strategic Parameters")
    selected_county = st.selectbox("Region (47 Counties)", sorted(county_data.keys()), index=42)
    water_source = st.selectbox("Infrastructure Type", ["Deep Borehole", "Shallow Well", "River Intake", "Piped Gravity", "Rainwater Harvesting", "Protected Spring", "Sand Dam", "Rock Catchment", "Desalination Plant"])
    
    soil_profiles = {"Volcanic Rock": 1.0, "Sandy Soil": 1.2, "Black Cotton Clay": 1.5, "Saline Soil": 1.6, "Alluvial Soil": 1.1, "Loam Soil": 0.9, "Laterite": 1.3, "Silt": 1.4}
    soil_type = st.selectbox("Geological Profile", list(soil_profiles.keys()))
    install_year = st.number_input("Installation Year", 1980, 2026, 2015)
    maintenance_status = st.select_slider("Maintenance Frequency", options=["Never", "Rarely", "Annually", "Quarterly"])
    gov_budget = st.slider("Budget Allocation (M KES)", 10, 1000, 150)

# --- 4. CALCULATION ENGINE ---
eat_timezone = pytz.timezone('Africa/Nairobi')
current_time_eat = datetime.now(eat_timezone).strftime('%Y-%m-%d %H:%M:%S')

age = 2026 - install_year
base_risk = age * 3.2
location_multiplier = county_data[selected_county]["risk_mod"]
soil_mod = soil_profiles[soil_type]
maint_mod = {"Never": 1.6, "Rarely": 1.3, "Annually": 0.8, "Quarterly": 0.4}

risk_prob = min(100.0, (base_risk * location_multiplier * soil_mod * maint_mod[maintenance_status]))
risk_amount = (risk_prob / 100) * (gov_budget * 1.6) 
asset_status = "STABLE" if risk_prob < 40 else "AT RISK" if risk_prob < 70 else "CRITICAL"
pop_at_risk = int((risk_prob / 100) * (county_data[selected_county]["pop_served"] * 0.25))

# --- 5. MAIN DASHBOARD ---
rain_drops = "".join([f'<div class="drop" style="left:{np.random.randint(0,100)}%; animation-delay:{np.random.random()}s;"></div>' for _ in range(40)])
st.markdown(f'<div class="rain-container">{rain_drops}<h1 style="padding-top:20px; text-align:center;">🇰🇪 MAJI METRICS v10.0 🇰🇪</h1><p style="text-align:center; color:#ffd700; font-weight:bold; font-size:1.2rem;">National Predictive Maintenance Portfolio</p><p style="text-align:center; color:#38bdf8;"><b>EAT: {current_time_eat}</b></p></div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Risk Probability", f"{risk_prob:.1f}%")
m2.metric("Fiscal Exposure", f"{risk_amount:.2f}M KES")
m3.metric("System Health", asset_status)
m4.metric("Community Impact", f"{pop_at_risk:,} People")

# --- QUANTITATIVE INSIGHTS ---
st.markdown(f"""
<div class="insight-box">
    <h3>🔍 County Analysis: Statistical Breakdown for {selected_county}</h3>
    <p>The <b>{asset_status}</b> health rating is a composite of environmental and operational stressors:</p>
    <ul>
        <li><b>Technical Deterioration:</b> At {risk_prob:.1f}% risk, the <b>{water_source}</b> shows signs of accelerated entropy. The <b>{soil_type}</b> foundation acts as a catalytic agent, increasing risk by a factor of <b>{soil_mod}x</b>.</li>
        <li><b>Demographic Vulnerability:</b> Approximately <b>{pop_at_risk:,} residents</b> are currently susceptible to acute water stress should a failure occur.</li>
        <li><b>Economic Leakage:</b> We estimate <b>KES {risk_amount:.2f} Million</b> is effectively "at-risk capital," representing potential losses through reactive rather than proactive maintenance.</li>
        <li><b>Policy Lever:</b> Upgrading maintenance to <b>Quarterly</b> would statistically reduce the probability of failure by <b>{((maint_mod[maintenance_status] - 0.4)/maint_mod[maintenance_status])*100:.1f}%</b> from current levels.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# --- 6. VISUALIZATIONS & COMPREHENSIVE EXPLANATIONS ---
t1, t2, t3, t4, t5 = st.tabs(["🌍 GEOSPATIAL", "📈 FINANCIALS", "📉 TRENDS", "🤝 IMPACT AUDIT", "📄 STRATEGIC REPORT"])

with t1:
    st.subheader(f"Distributed Asset Network: {selected_county}")
    c_info = county_data[selected_county]
    
    # --- NEW: GENERATE DISTRIBUTED POINTS ---
    num_assets = 12
    # Create small random offsets around the county center to simulate different borehole/well locations
    lats = [c_info["coords"][0] + np.random.uniform(-0.15, 0.15) for _ in range(num_assets)]
    lons = [c_info["coords"][1] + np.random.uniform(-0.15, 0.15) for _ in range(num_assets)]
    # Randomize risk slightly for each site based on the global risk probability
    risks = [max(5.0, min(100.0, risk_prob + np.random.normal(0, 10))) for _ in range(num_assets)]
    site_names = [f"Asset Site {i+1} ({water_source})" for i in range(num_assets)]
    
    map_df = pd.DataFrame({'LAT': lats, 'LON': lons, 'RISK': risks, 'SITE': site_names})
    
    fig_map = px.scatter_mapbox(map_df, 
                                lat="LAT", 
                                lon="LON", 
                                size="RISK", 
                                color="RISK", 
                                hover_name="SITE",
                                color_continuous_scale="Reds", 
                                zoom=8, 
                                height=500)
    
    fig_map.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown(f"""
    <div class="explanation-text">
        <b>Dynamic Interpretation (Distributed Map):</b><br>
        This map now visualizes <b>{num_assets} simulated infrastructure points</b> across {selected_county}. 
        Instead of a single regional average, you are seeing <b>intra-county variance</b>. 
        Points with higher saturation (darker red) indicate localized critical failures where {soil_type} and {water_source} age are hitting 
        peak degradation. Larger bubbles indicate sites where a breakdown would impact the highest density of the <b>{pop_at_risk:,}</b> people at risk.
    </div>
    """, unsafe_allow_html=True)

with t2:
    st.subheader("Budgetary Risk Reserve")
    budget_data = {"Category": ["Infrastructure", "Operations", "Water Treatment", "Risk Reserve"],
                   "Value": [gov_budget*0.45, gov_budget*0.25, gov_budget*0.1, risk_amount]}
    fig_pie = px.pie(budget_data, values='Value', names='Category', hole=0.4, color_discrete_sequence=['#ffd700', '#38bdf8', '#ff4b4b', '#00cc96'])
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown(f"""
    <div class="explanation-text">
        <b>Dynamic Interpretation (Fiscal Pie):</b><br>
        Of the total <b>{gov_budget}M KES</b> allocated, the red <b>Risk Reserve</b> slice consumes <b>{risk_amount:.2f}M KES</b>. 
        This is a "Sunk Cost Projection." It means that for every shilling spent on {selected_county}, a significant portion is being 
        cannibalized by the <b>{asset_status}</b> state of the {water_source}. If risk probability was below 10%, this red slice would 
        be negligible, allowing those millions to be redirected to "Infrastructure" (expansion).
    </div>
    """, unsafe_allow_html=True)

with t3:
    col_t1, col_t2 = st.columns(2)
    years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
    future_risk = [min(100, risk_prob * (1 + (0.08 * i))) for i in range(-2, 5)]
    
    with col_t1:
        st.subheader("Degradation Forecast (2030)")
        fig_line = px.area(x=years, y=future_risk, labels={'x': 'Fiscal Year', 'y': 'Risk %'}, color_discrete_sequence=['#38bdf8'])
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown(f"""
        <div class="explanation-text">
            <b>Trend Analysis:</b><br>
            The area chart shows the <b>Temporal Decay</b> of the asset. Starting from <b>{install_year}</b>, the system has 
            reached its current <b>{risk_prob:.1f}%</b> state. The upward slope toward 2030 predicts a "Failure Threshold Cross" unless maintenance 
            intervals are shortened.
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.subheader("Regional Benchmark")
        compare_df = pd.DataFrame({'County': ['Nairobi', 'Turkana', 'Mombasa', selected_county], 'Risk Index': [15, 92, 45, risk_prob]})
        fig_bar = px.bar(compare_df, x='County', y='Risk Index', color='Risk Index', color_continuous_scale='Turbo')
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown(f"""
        <div class="explanation-text">
            <b>Benchmarking {selected_county}:</b><br>
            This bar chart provides national context. By comparing {selected_county} against <b>Turkana</b> (Extreme Risk) 
            and <b>Nairobi</b> (Low Risk), we can see that your current risk of <b>{risk_prob:.1f}</b> is 
            {'higher than' if risk_prob > 45 else 'comparable to'} the coastal benchmarks.
        </div>
        """, unsafe_allow_html=True)

with t4:
    st.subheader("Vision 2030 Equity Assessment")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown(f'<div class="vision-card"><h3>Universal Access</h3><p>Vulnerable Residents: <b>{pop_at_risk:,}</b></p><p><i>Current protocol: {maintenance_status}</i></p></div>', unsafe_allow_html=True)
    with col_i2:
        st.markdown(f'<div class="vision-card"><h3>Resilience Score</h3><progress value="{100 - risk_prob}" max="100" style="width:100%;"></progress><p>Score: <b>{100 - risk_prob:.1f}/100</b></p></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="explanation-text">
        <b>Impact Explanation:</b><br>
        The <b>Community Impact ({pop_at_risk:,} People)</b> is the most critical number. 
        The <b>Resilience Score ({100-risk_prob:.1f})</b> is an inverse of risk. A perfect 100 means a "Future-Proof" county. 
        {selected_county}'s current score indicates that <b>{risk_prob:.1f}%</b> of the system reliability has been compromised.
    </div>
    """, unsafe_allow_html=True)

with t5:
    st.subheader("Comprehensive Statistical Audit | Maji Metrics")
    report_narrative = (
        f"OFFICIAL AUDIT: KENYA VISION 2030 WATER SECURITY INITIATIVE\n"
        f"GENERATED: {current_time_eat} EAT\n"
        f"--------------------------------------------------------------------------\n"
        f"I. ASSET IDENTIFICATION\n"
        f"Region: {selected_county} County\n"
        f"Infrastructure Type: {water_source}\n"
        f"Geological Context: {soil_type} (Modifier: {soil_mod}x)\n"
        f"Historical Baseline: Installed {install_year} ({age} years in service)\n\n"
        f"II. RISK PROBABILISTIC MODELING\n"
        f"Current Failure Probability: {risk_prob:.2f}%\n"
        f"Projected Status: {asset_status}\n"
        f"Maintenance Efficiency: {maintenance_status} frequency yields a {maint_mod[maintenance_status]}x wear multiplier.\n\n"
        f"III. SOCIO-ECONOMIC IMPACT\n"
        f"Estimated Population Disruption: {pop_at_risk:,} citizens\n"
        f"Fiscal Value at Risk (VaR): KES {risk_amount:.2f}M\n"
        f"Budget Allocation Efficiency: {((gov_budget - risk_amount)/gov_budget)*100:.1f}% effective usage.\n\n"
        f"IV. STRATEGIC DIRECTIVES\n"
        f"{'CRITICAL: Immediate structural overhaul and sensor deployment required.' if risk_prob > 70 else 'ELEVATED: Increase maintenance frequency to Quarterly to stabilize asset.' if risk_prob > 40 else 'STABLE: Continue routine monitoring and annual audits.'}\n"
        f"--------------------------------------------------------------------------\n"
        f"END OF REPORT | MAJI METRICS ANALYTICS DIVISION"
    )
    st.markdown(f'<div class="report-box">{report_narrative}</div>', unsafe_allow_html=True)
    st.download_button("📥 Export Comprehensive Audit", data=report_narrative, file_name=f"Audit_{selected_county}_{datetime.now().strftime('%Y%m%d')}.txt")

st.divider()
st.markdown("<center><i>Maji Metrics v10.0 | National 47-County Portfolio | Capstone 2026</i></center>", unsafe_allow_html=True)