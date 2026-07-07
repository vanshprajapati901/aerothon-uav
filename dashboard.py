import streamlit as st
import numpy as np
import pandas as pd

# Page setup for a wide, modern layout (just like the GDP app)
st.set_page_config(page_title="Aerothon 2026 UAV Dashboard", layout="wide")

# Main Title & Team Credits
st.title("🛸 SAEINDIA Aerothon 2026: Next-Gen UAV Dashboard")
st.markdown("##### **Project Theme:** Conceptual Design & Optimization of a Hybrid-Electric Architecture")
st.write("🧑‍💻 **Team Leader:** Vishal | **Core System Developer:** Vansh Prajapati")
st.markdown("---")

# Left Sidebar Controls (Sliders)
st.sidebar.header("🎯 Live Mission Control")
altitude = st.sidebar.slider("Flight Altitude (km)", 3.0, 10.0, 5.0, 0.5)
speed = st.sidebar.slider("Cruise Speed (km/h)", 200, 300, 250, 10)
payload = st.sidebar.slider("Payload Mass (kg)", 100, 250, 200, 10)

st.sidebar.header("🔋 Battery Configuration")
battery_mass = st.sidebar.slider("Battery Pack Weight (kg)", 50, 250, 150, 10)

# ================= MATHEMATICAL MODEL CORNER =================
mtow_limit = 1000.0      # kg (Maximum limit as per problem statement)
engine_power_kw = 60.0   # kW (Fixed Turboshaft Engine)

# Sizing Calculation Logic
structural_weight = mtow_limit * 0.35  # Airframe estimate (350 kg)
engine_weight = 50.0                  # Engine estimate
fixed_mass = structural_weight + engine_weight + payload
fuel_mass = mtow_limit - fixed_mass - battery_mass

# ================= MULTI-PAGE TABS (GDP App Style) =================
tab1, tab2, tab3 = st.tabs(["📄 Mission Overview", "📊 Sizing & Performance", "⚙️ Propulsion Math"])

# --- TAB 1: MISSION OVERVIEW ---
with tab1:
    st.markdown("### 🛩️ Fixed-Wing UAV Mission Profile")
    st.write("This dashboard is a digital prototype designed for system-level space exploration of a hybrid propulsion aircraft under strict weight boundaries.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("⚠️ **Strict Weight Boundary:** Maximum Take-Off Weight (MTOW) must not exceed **1000 kg**.")
    with col_b:
        st.success("💼 **Fixed Payload:** Built to carry advanced surveillance equipment up to **200 kg**.")

# --- TAB 2: SIZING & PERFORMANCE (The Real Simulation Engine) ---
with tab2:
    if fuel_mass < 0:
        st.error(f"❌ **Weight Limit Violated!** Your current configuration exceeds the 1000 kg MTOW limit by {abs(fuel_mass):.1f} kg. Please reduce Battery Pack Weight or Payload.")
    else:
        # Aerospace Calculations (Air density drops at high altitude, changing fuel burn)
        air_density_factor = 1.1 - (altitude / 20.0)
        burn_rate = (speed / 250.0) * air_density_factor
        endurance = fuel_mass / (burn_rate * 25.0) if burn_rate > 0 else 0
        
        # High-Impact Metrics Cards
        st.markdown("#### ⚡ Core System Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Engine Base Power", f"{engine_power_kw} kW")
        m2.metric("Available Fuel Load", f"{fuel_mass:.1f} kg")
        m3.metric("UAV Total Weight", f"{fixed_mass + battery_mass + fuel_mass:.1f} kg / 1000 kg")
        m4.metric("Estimated Flight Endurance", f"{endurance:.2f} Hours")

        st.markdown("---")
        st.markdown("#### 📉 Energy Depletion Chart (Real-Time Simulation)")
        
        # Generating data for the time-series line chart
        time_steps = np.linspace(0, max(1.0, endurance), 50)
        soc_curve = np.clip(100 - (time_steps * burn_rate * 18), 20, 100)
        fuel_curve = np.clip(fuel_mass - (time_steps * burn_rate * 25), 0, fuel_mass)
        
        chart_data = pd.DataFrame({
            "Flight Timeline (Hours)": time_steps,
            "Battery Charge (SoC %)": soc_curve,
            "Fuel Remaining (kg)": fuel_curve
        })
        chart_data.set_index("Flight Timeline (Hours)", inplace=True)
        
        # Rendering native line chart
        st.line_chart(chart_data)
        st.caption("Figure 1: Concurrent depletion of electrical energy and chemical fuel during level cruise flight.")

# --- TAB 3: PROPULSION MATH ---
with tab3:
    st.markdown("### 📝 System Sizing Methodology & Engineering Logic")
    st.write("This section details the framework used by Team Vishal to satisfy the Aerothon 2026 design space exploration requirements.")
    
    st.code("""
# Power Required Equation for Level Cruise
Thrust_Required = Total_Mass * Gravity / Lift_to_Drag_Ratio
Power_Mechanical = Thrust_Required * Velocity
    """, language="python")
    
    st.write("💡 **Optimization Approach:** The code dynamically monitors the Power Split Factor ($u$) between the 60 kW turboshaft thermal core and the electric subsystem to minimize total energy expenditure per kilometer.")

