import streamlit as st
import pandas as pd
from comparison import calculate_aircraft_comparison
from optimization import optimize_aircraft_design
from report_generator import generate_aircraft_report

from geometry import (
    calculate_wing_geometry,
    create_aircraft_3d
)

from flight_analysis import (
    calculate_flight_performance,
    generate_flight_performance_data,
    generate_altitude_data
)

from calculations import (
    calculate_aircraft_performance,
    calculate_advanced_aerodynamics
)

from visualization import (
    plot_performance,
    plot_advanced_performance
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Aircraft Performance Analyzer",
    page_icon="✈️",
    layout="wide"
)


# =====================================================
# APPLICATION HEADER
# =====================================================

st.title("✈️ Aircraft Design & Performance Analysis System")

st.subheader("Preliminary Aerodynamic Analysis and Simulation")

st.caption(
    "Def-Space Autumn Internship 2026 | "
    "Developed by MD Rajaak"
)

st.divider()


# =====================================================
# SIDEBAR: AIRCRAFT DESIGN PARAMETERS
# =====================================================

st.sidebar.header("Aircraft Design Parameters")

mass = st.sidebar.number_input(
    "Aircraft Mass (kg)",
    min_value=1.0,
    value=1000.0
)

wing_area = st.sidebar.number_input(
    "Wing Area (m²)",
    min_value=0.1,
    value=16.0
)

wingspan = st.sidebar.number_input(
    "Wing Span (m)",
    min_value=0.1,
    value=10.0
)

velocity = st.sidebar.number_input(
    "Airspeed (m/s)",
    min_value=0.1,
    value=50.0
)

air_density = st.sidebar.number_input(
    "Air Density (kg/m³)",
    min_value=0.1,
    value=1.225
)

lift_coefficient = st.sidebar.number_input(
    "Lift Coefficient (CL)",
    min_value=0.01,
    value=0.8
)

drag_coefficient = st.sidebar.number_input(
    "Drag Coefficient (CD)",
    min_value=0.001,
    value=0.04
)

max_lift_coefficient = st.sidebar.number_input(
    "Maximum Lift Coefficient (CLmax)",
    min_value=0.01,
    value=1.5
)


# =====================================================
# SIDEBAR: ADVANCED AERODYNAMIC PARAMETERS
# =====================================================

st.sidebar.divider()

st.sidebar.subheader("Advanced Aerodynamic Parameters")

zero_lift_drag_coefficient = st.sidebar.number_input(
    "Zero-Lift Drag Coefficient (CD0)",
    min_value=0.001,
    max_value=0.2,
    value=0.025,
    step=0.001,
    format="%.3f"
)

oswald_efficiency = st.sidebar.number_input(
    "Oswald Efficiency Factor (e)",
    min_value=0.1,
    max_value=1.0,
    value=0.80,
    step=0.05
)


# =====================================================
# ANALYSIS BUTTON
# =====================================================

st.sidebar.divider()

analyze = st.sidebar.button(
    "Analyze Aircraft",
    type="primary",
    use_container_width=True
)


# =====================================================
# MAIN AIRCRAFT PERFORMANCE ANALYSIS
# =====================================================

st.header("1. Aircraft Performance Analysis")

if analyze:

    # Basic calculations
    results = calculate_aircraft_performance(
        mass,
        wing_area,
        wingspan,
        velocity,
        air_density,
        lift_coefficient,
        drag_coefficient,
        max_lift_coefficient
    )
    st.session_state["basic_results"] = results

    # Performance metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Lift Force",
        f"{results['Lift Force (N)']:,.2f} N"
    )

    col2.metric(
        "Drag Force",
        f"{results['Drag Force (N)']:,.2f} N"
    )

    col3.metric(
        "Stall Speed",
        f"{results['Stall Velocity (km/h)']:.2f} km/h"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Wing Loading",
        f"{results['Wing Loading (N/m²)']:.2f} N/m²"
    )

    col5.metric(
        "Aspect Ratio",
        f"{results['Aspect Ratio']:.2f}"
    )

    col6.metric(
        "Lift-to-Drag Ratio",
        f"{results['Lift-to-Drag Ratio']:.2f}"
    )

    # Detailed results
    st.subheader("Detailed Performance Results")

    result_df = pd.DataFrame(
        list(results.items()),
        columns=["Parameter", "Value"]
    )

    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )

    # Original performance graphs
    st.subheader("Basic Aerodynamic Performance Graphs")

    fig1, fig2 = plot_performance(
        mass,
        wing_area,
        air_density,
        lift_coefficient,
        drag_coefficient,
        max_lift_coefficient
    )

    st.pyplot(fig1)
    st.pyplot(fig2)

    # Basic CSV download
    st.download_button(
        "Download Basic Analysis CSV",
        data=result_df.to_csv(index=False),
        file_name="aircraft_performance_report.csv",
        mime="text/csv"
    )


    # =================================================
    # ADVANCED AERODYNAMIC ANALYSIS
    # =================================================

    st.divider()

    st.header("2. Advanced Aerodynamic Analysis")

    advanced_results = calculate_advanced_aerodynamics(
        mass,
        wing_area,
        wingspan,
        velocity,
        air_density,
        zero_lift_drag_coefficient,
        oswald_efficiency,
        max_lift_coefficient
    )
    st.session_state["advanced_results"] = advanced_results

    st.subheader("Steady Level-Flight Performance")

    # Stall condition check
    if advanced_results["Level Flight Valid"]:

        st.success(
            "Selected airspeed is above the estimated "
            "stall speed. Level-flight analysis is valid "
            "under the model assumptions."
        )

    else:

        st.error(
            "Selected airspeed is below the estimated "
            "stall speed. Level-flight analysis is invalid."
        )

    # Advanced performance metrics
    a1, a2, a3 = st.columns(3)

    a1.metric(
        "Required Lift Coefficient",
        f"{advanced_results['Required Lift Coefficient']:.4f}"
    )

    a2.metric(
        "Total Drag Coefficient",
        f"{advanced_results['Total Drag Coefficient']:.4f}"
    )

    a3.metric(
        "Induced Drag Coefficient",
        f"{advanced_results['Induced Drag Coefficient']:.4f}"
    )

    a4, a5, a6 = st.columns(3)

    a4.metric(
        "Level Flight Lift",
        f"{advanced_results['Level Flight Lift (N)']:,.2f} N"
    )

    a5.metric(
        "Level Flight Drag",
        f"{advanced_results['Level Flight Drag (N)']:,.2f} N"
    )

    a6.metric(
        "Power Required",
        f"{advanced_results['Power Required (kW)']:.2f} kW"
    )

    st.metric(
        "Advanced Lift-to-Drag Ratio",
        f"{advanced_results['Lift-to-Drag Ratio']:.2f}"
    )

    # Advanced detailed results
    st.subheader("Advanced Calculation Results")

    advanced_df = pd.DataFrame(
        list(advanced_results.items()),
        columns=["Parameter", "Value"]
    )

    st.dataframe(
        advanced_df,
        use_container_width=True,
        hide_index=True
    )

    # Advanced graphs only when level flight is valid
    if advanced_results["Level Flight Valid"]:

        st.subheader("Advanced Aerodynamic Performance Graphs")

        fig3, fig4, fig5 = plot_advanced_performance(
            mass,
            wing_area,
            wingspan,
            air_density,
            zero_lift_drag_coefficient,
            oswald_efficiency,
            max_lift_coefficient,
            velocity
        )

        st.pyplot(fig3)
        st.pyplot(fig4)
        st.pyplot(fig5)

        # Advanced CSV download
        st.download_button(
            "Download Advanced Analysis CSV",
            data=advanced_df.to_csv(index=False),
            file_name="advanced_aircraft_analysis.csv",
            mime="text/csv"
        )

    # Engineering assumptions
    st.divider()

    with st.expander("Engineering Model Assumptions"):

        st.markdown("""
        - Steady, level and unaccelerated flight.
        - Constant air density.
        - Parabolic aerodynamic drag polar.
        - Constant Oswald efficiency factor.
        - No compressibility or Reynolds number corrections.
        - No aircraft trim or propulsion efficiency modelling.

        This application is intended for preliminary
        educational aerodynamic analysis and is not
        a certified aircraft design or flight simulator.
        """)

else:

    # Initial dashboard screen
    st.info(
        "Enter aircraft parameters in the left sidebar "
        "and click Analyze Aircraft."
    )

    st.markdown("""
    ### Available Features

    **Basic Analysis**
    - Lift and drag force calculations
    - Wing loading and aspect ratio
    - Stall speed estimation
    - Basic aerodynamic graphs

    **Advanced Analysis**
    - Required lift coefficient for level flight
    - Induced drag and total drag estimation
    - Parabolic drag polar
    - Lift-to-drag ratio
    - Power required for level flight
    - Advanced aerodynamic performance graphs

    **Reporting**
    - Downloadable CSV analysis reports
    """)

    st.warning(
        "This is an educational preliminary analysis tool, "
        "not a certified aircraft design simulator."
    )


# =====================================================
# MODULE 3: AIRCRAFT DESIGN COMPARISON
# =====================================================

st.divider()

st.header("3. Aircraft Design Comparison")

st.write(
    "Compare two aircraft designs using aerodynamic "
    "performance parameters."
)

st.info(
    "Enter the specifications of two aircraft "
    "and compare their performance."
)

# Common operating conditions
st.subheader("Operating Conditions")

common_col1, common_col2 = st.columns(2)

with common_col1:
    comparison_density = st.number_input(
        "Comparison Air Density (kg/m³)",
        min_value=0.1,
        value=1.225,
        key="comparison_density"
    )

with common_col2:
    comparison_velocity = st.number_input(
        "Comparison Airspeed (m/s)",
        min_value=0.1,
        value=50.0,
        key="comparison_velocity"
    )
    "Comparison Airspeed (m/s)",
    min_value=0.1,
    value=50.0,
    key="comparison_velocity"


st.divider()

# Aircraft input form
with st.form("aircraft_comparison_form"):

    col_a, col_b = st.columns(2)

    with col_a:

        st.subheader("Aircraft A")

        mass_a = st.number_input(
            "Mass (kg)",
            min_value=1.0,
            value=1000.0,
            key="mass_a"
        )

        area_a = st.number_input(
            "Wing Area (m²)",
            min_value=0.1,
            value=16.0,
            key="area_a"
        )

        span_a = st.number_input(
            "Wingspan (m)",
            min_value=0.1,
            value=10.0,
            key="span_a"
        )

        cd0_a = st.number_input(
            "Zero-Lift Drag Coefficient",
            min_value=0.001,
            value=0.025,
            key="cd0_a"
        )

        efficiency_a = st.number_input(
            "Oswald Efficiency",
            min_value=0.1,
            max_value=1.0,
            value=0.80,
            key="efficiency_a"
        )

        clmax_a = st.number_input(
            "Maximum Lift Coefficient",
            min_value=0.1,
            value=1.5,
            key="clmax_a"
        )

    with col_b:

        st.subheader("Aircraft B")

        mass_b = st.number_input(
            "Mass (kg)",
            min_value=1.0,
            value=1200.0,
            key="mass_b"
        )

        area_b = st.number_input(
            "Wing Area (m²)",
            min_value=0.1,
            value=20.0,
            key="area_b"
        )

        span_b = st.number_input(
            "Wingspan (m)",
            min_value=0.1,
            value=12.0,
            key="span_b"
        )

        cd0_b = st.number_input(
            "Zero-Lift Drag Coefficient",
            min_value=0.001,
            value=0.030,
            key="cd0_b"
        )

        efficiency_b = st.number_input(
            "Oswald Efficiency",
            min_value=0.1,
            max_value=1.0,
            value=0.85,
            key="efficiency_b"
        )

        clmax_b = st.number_input(
            "Maximum Lift Coefficient",
            min_value=0.1,
            value=1.6,
            key="clmax_b"
        )

    compare_button = st.form_submit_button(
        "Compare Aircraft Designs",
        type="primary",
        use_container_width=True
    )


# Perform comparison
if compare_button:

    result_a = calculate_aircraft_comparison(
        mass_a,
        area_a,
        span_a,
        comparison_density,
        comparison_velocity,
        cd0_a,
        efficiency_a,
        clmax_a
    )

    result_b = calculate_aircraft_comparison(
        mass_b,
        area_b,
        span_b,
        comparison_density,
        comparison_velocity,
        cd0_b,
        efficiency_b,
        clmax_b
    )

    st.session_state["comparison_results"] = (
        result_a,
        result_b
    )


# Display saved comparison results
if "comparison_results" in st.session_state:

    result_a, result_b = st.session_state[
        "comparison_results"
    ]

    st.divider()

    st.subheader("Aircraft Performance Comparison")

    # Comparison table
    comparison_df = pd.DataFrame({
        "Parameter": list(result_a.keys()),
        "Aircraft A": list(result_a.values()),
        "Aircraft B": list(result_b.values())
    })

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )

    # Flight validity
    st.subheader("Flight Condition")

    status_col1, status_col2 = st.columns(2)

    with status_col1:
        if result_a["Level Flight Valid"]:
            st.success("Aircraft A: Level flight valid")
        else:
            st.error("Aircraft A: Below stall condition")

    with status_col2:
        if result_b["Level Flight Valid"]:
            st.success("Aircraft B: Level flight valid")
        else:
            st.error("Aircraft B: Below stall condition")

    # Comparison charts
    st.divider()

    st.subheader("Comparative Performance Graphs")

    chart_metrics = [
        ("Stall Speed (km/h)", "Stall Speed Comparison"),
        ("Wing Loading (N/m²)", "Wing Loading Comparison"),
        ("Maximum L/D Ratio", "Maximum Lift-to-Drag Ratio"),
    ]

    for metric, chart_title in chart_metrics:

        st.markdown(f"#### {chart_title}")

        chart_df = pd.DataFrame({
            "Aircraft": ["Aircraft A", "Aircraft B"],
            "Value": [
                result_a[metric],
                result_b[metric]
            ]
        })

        st.bar_chart(
            chart_df,
            x="Aircraft",
            y="Value"
        )

    # Drag and power comparison
    st.markdown("#### Drag Force Comparison")

    if (
        result_a["Level Flight Valid"]
        and result_b["Level Flight Valid"]
    ):

        drag_df = pd.DataFrame({
            "Aircraft": ["Aircraft A", "Aircraft B"],
            "Drag Force (N)": [
                result_a["Drag Force (N)"],
                result_b["Drag Force (N)"]
            ]
        })

        st.bar_chart(
            drag_df,
            x="Aircraft",
            y="Drag Force (N)"
        )

        st.markdown("#### Power Requirement Comparison")

        power_df = pd.DataFrame({
            "Aircraft": ["Aircraft A", "Aircraft B"],
            "Power (kW)": [
                result_a["Power Required (kW)"],
                result_b["Power Required (kW)"]
            ]
        })

        st.bar_chart(
            power_df,
            x="Aircraft",
            y="Power (kW)"
        )

    else:
        st.warning(
            "Drag and power comparison at the selected "
            "speed requires both aircraft to satisfy "
            "the level-flight condition."
        )

    # Download comparison report
    st.divider()

    st.subheader("Download Comparison Report")

    csv_data = comparison_df.to_csv(index=False)

    st.download_button(
        "Download Aircraft Comparison CSV",
        data=csv_data,
        file_name="aircraft_design_comparison.csv",
        mime="text/csv",
        use_container_width=True
    )


# =====================================================
# MODULE 4: AIRCRAFT DESIGN OPTIMIZATION
# =====================================================

st.divider()

st.header("4. Aircraft Design Optimization")

st.write(
    "Explore different wing configurations and identify "
    "the most efficient aircraft design."
)

st.info(
    "The optimizer searches different wing areas and "
    "wingspans to identify configurations with minimum "
    "drag and maximum aerodynamic efficiency."
)

st.subheader("Optimization Design Constraints")

with st.form("aircraft_optimization_form"):

    opt_col1, opt_col2 = st.columns(2)

    with opt_col1:

        area_min = st.number_input(
            "Minimum Wing Area (m²)",
            min_value=1.0,
            value=10.0,
            key="opt_area_min"
        )

        area_max = st.number_input(
            "Maximum Wing Area (m²)",
            min_value=2.0,
            value=30.0,
            key="opt_area_max"
        )

    with opt_col2:

        span_min = st.number_input(
            "Minimum Wingspan (m)",
            min_value=1.0,
            value=8.0,
            key="opt_span_min"
        )

        span_max = st.number_input(
            "Maximum Wingspan (m)",
            min_value=2.0,
            value=18.0,
            key="opt_span_max"
        )

    samples = st.slider(
        "Optimization Resolution",
        min_value=10,
        max_value=100,
        value=40,
        step=10,
        help="Higher resolution evaluates more configurations."
    )

    optimize_button = st.form_submit_button(
        "Optimize Aircraft Design",
        type="primary",
        use_container_width=True
    )


# Run optimization
if optimize_button:

    try:

        optimization_results = optimize_aircraft_design(
            mass=mass,
            air_density=air_density,
            velocity=velocity,
            cd0=zero_lift_drag_coefficient,
            oswald_efficiency=oswald_efficiency,
            clmax=max_lift_coefficient,
            area_min=area_min,
            area_max=area_max,
            span_min=span_min,
            span_max=span_max,
            samples=samples
        )

        st.session_state["optimization_results"] = (
            optimization_results
        )

        st.success(
            "Aircraft design optimization completed successfully!"
        )

    except ValueError as error:

        st.error(str(error))

    except Exception as error:

        st.error(f"Optimization error: {error}")


# Display optimization results
if "optimization_results" in st.session_state:

    opt_results = st.session_state[
        "optimization_results"
    ]

    min_drag = opt_results["minimum_drag"]

    max_ld = opt_results["maximum_ld"]

    min_power = opt_results["minimum_power"]

    all_designs = opt_results["all_designs"]

    st.divider()

    st.subheader("Optimization Results")

    # Minimum drag design
    st.markdown("### 1. Minimum Drag Design")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Optimized Wing Area",
        f"{min_drag['Wing Area (m²)']:.2f} m²"
    )

    c2.metric(
        "Optimized Wingspan",
        f"{min_drag['Wingspan (m)']:.2f} m"
    )

    c3.metric(
        "Minimum Drag",
        f"{min_drag['Drag Force (N)']:.2f} N"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Aspect Ratio",
        f"{min_drag['Aspect Ratio']:.2f}"
    )

    c5.metric(
        "Power Required",
        f"{min_drag['Power Required (kW)']:.2f} kW"
    )

    c6.metric(
        "Lift-to-Drag Ratio",
        f"{min_drag['Lift-to-Drag Ratio']:.2f}"
    )

    # Maximum L/D design
    st.divider()

    st.markdown("### 2. Maximum Aerodynamic Efficiency")

    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Wing Area",
        f"{max_ld['Wing Area (m²)']:.2f} m²"
    )
    d2.metric(
        "Wingspan",
        f"{max_ld['Wingspan (m)']:.2f} m"
    )

    d3.metric(
        "Maximum L/D Ratio",
        f"{max_ld['Lift-to-Drag Ratio']:.2f}"
    )

    # Minimum power design
    st.divider()

    st.markdown("### 3. Minimum Power Design")

    p1, p2, p3 = st.columns(3)

    p1.metric(
        "Wing Area",
        f"{min_power['Wing Area (m²)']:.2f} m²"
    )

    p2.metric(
        "Wingspan",
        f"{min_power['Wingspan (m)']:.2f} m"
    )

    p3.metric(
        "Minimum Power",
        f"{min_power['Power Required (kW)']:.2f} kW"
    )

    # Design comparison table
    st.divider()

    st.subheader("Optimized Design Comparison")

    design_comparison = pd.DataFrame(
        [
            {
                "Optimization Objective": "Minimum Drag",
                **min_drag
            },
            {
                "Optimization Objective": "Maximum L/D",
                **max_ld
            },
            {
                "Optimization Objective": "Minimum Power",
                **min_power
            }
        ]
    )

    st.dataframe(
        design_comparison,
        use_container_width=True,
        hide_index=True
    )

    # Design-space exploration
    st.divider()

    st.subheader("Design Space Analysis")

    st.write(
        "Explore the relationship between wing area, "
        "wingspan and aerodynamic drag."
    )

    st.scatter_chart(
        all_designs,
        x="Wing Area (m²)",
        y="Drag Force (N)",
        color="Aspect Ratio",
        size="Wingspan (m)"
    )

    st.subheader("Best Feasible Configurations")

    st.dataframe(
        all_designs.head(10),
        use_container_width=True,
        hide_index=True
    )

    # Download optimization report
    st.divider()

    st.subheader("Download Optimization Report")

    optimization_csv = all_designs.to_csv(index=False)

    st.download_button(
        "Download Optimization CSV",
        data=optimization_csv,
        file_name="aircraft_design_optimization.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption(
        "Optimization uses a preliminary parabolic drag-polar "
        "model. Results depend on the selected design bounds, "
        "operating conditions and aerodynamic assumptions."
    )

else:

    st.info(
        "Set the design constraints above and click "
        "'Optimize Aircraft Design' to begin."
    )


# =====================================================
# MODULE 5: FLIGHT PERFORMANCE ANALYSIS
# =====================================================

st.divider()

st.header("5. Flight Performance Analysis")

st.write(
    "Analyze aircraft performance during take-off, "
    "landing, climbing and cruise flight."
)

st.info(
    "This module estimates flight performance using "
    "aircraft geometry, aerodynamic characteristics, "
    "engine power and fuel parameters."
)


# =====================================================
# FLIGHT PERFORMANCE INPUTS
# =====================================================

st.subheader("Engine and Flight Parameters")

with st.form("flight_performance_form"):

    fcol1, fcol2 = st.columns(2)

    with fcol1:

        engine_thrust = st.number_input(
            "Available Take-off Thrust (N)",
            min_value=1.0,
            value=3000.0,
            key="flight_thrust"
        )

        available_power = st.number_input(
            "Available Engine Power (kW)",
            min_value=1.0,
            value=60.0,
            key="flight_power"
        )

        fuel_mass = st.number_input(
            "Usable Fuel Mass (kg)",
            min_value=1.0,
            value=100.0,
            key="flight_fuel"
        )

        bsfc = st.number_input(
            "Brake Specific Fuel Consumption (kg/kWh)",
            min_value=0.01,
            value=0.25,
            step=0.01,
            key="flight_bsfc"
        )

    with fcol2:

        propeller_efficiency = st.number_input(
            "Propeller Efficiency",
            min_value=0.1,
            max_value=1.0,
            value=0.80,
            step=0.05,
            key="flight_prop_efficiency"
        )

        rolling_friction = st.number_input(
            "Take-off Rolling Friction Coefficient",
            min_value=0.0,
            value=0.04,
            step=0.01,
            key="flight_rolling_friction"
        )

        braking_friction = st.number_input(
            "Landing Braking Friction Coefficient",
            min_value=0.01,
            value=0.35,
            step=0.05,
            key="flight_braking_friction"
        )

    flight_button = st.form_submit_button(
        "Analyze Flight Performance",
        type="primary",
        use_container_width=True
    )


# =====================================================
# PERFORM FLIGHT ANALYSIS
# =====================================================

if flight_button:

    try:

        flight_results = calculate_flight_performance(
            mass=mass,
            wing_area=wing_area,
            wingspan=wingspan,
            air_density=air_density,
            velocity=velocity,
            cd0=zero_lift_drag_coefficient,
            oswald_efficiency=oswald_efficiency,
            clmax=max_lift_coefficient,
            thrust=engine_thrust,
            available_power_kw=available_power,
            fuel_mass=fuel_mass,
            bsfc=bsfc,
            propeller_efficiency=propeller_efficiency,
            rolling_friction=rolling_friction,
            braking_friction=braking_friction
        )

        flight_profile = generate_flight_performance_data(
            mass,
            wing_area,
            wingspan,
            air_density,
            zero_lift_drag_coefficient,
            oswald_efficiency,
            max_lift_coefficient,
            available_power,
            propeller_efficiency,
            velocity
        )

        altitude_profile = generate_altitude_data(
            mass,
            wing_area,
            max_lift_coefficient
        )

        st.session_state["flight_results"] = flight_results

        st.session_state["flight_profile"] = flight_profile

        st.session_state["altitude_profile"] = altitude_profile

        st.success(
            "Flight performance analysis completed successfully!"
        )

    except ValueError as error:

        st.error(str(error))

    except Exception as error:

        st.error(f"Flight analysis error: {error}")


# =====================================================
# DISPLAY FLIGHT RESULTS
# =====================================================

if "flight_results" in st.session_state:

    fr = st.session_state["flight_results"]

    flight_profile = st.session_state["flight_profile"]

    altitude_profile = st.session_state["altitude_profile"]

    st.divider()

    # -------------------------------------------------
    # 1. TAKE-OFF PERFORMANCE
    # -------------------------------------------------

    st.subheader("1. Take-off Performance")

    t1, t2, t3 = st.columns(3)

    t1.metric(
        "Stall Speed",
        f"{fr['Stall Speed (km/h)']:.2f} km/h"
    )

    t2.metric(
        "Take-off Speed",
        f"{fr['Take-off Speed (km/h)']:.2f} km/h"
    )

    t3.metric(
        "Take-off Acceleration",
        f"{fr['Take-off Acceleration (m/s²)']:.2f} m/s²"
    )

    if fr["Estimated Take-off Distance (m)"] is not None:

        st.metric(
            "Estimated Take-off Distance",
            f"{fr['Estimated Take-off Distance (m)']:.2f} m"
        )

    else:

        st.error(
            "Available thrust is insufficient for the "
            "estimated take-off acceleration."
        )

    # -------------------------------------------------
    # 2. LANDING PERFORMANCE
    # -------------------------------------------------

    st.divider()

    st.subheader("2. Landing Performance")

    l1, l2 = st.columns(2)

    l1.metric(
        "Touchdown Speed",
        f"{fr['Touchdown Speed (km/h)']:.2f} km/h"
    )

    l2.metric(
        "Landing Deceleration",
        f"{fr['Landing Deceleration (m/s²)']:.2f} m/s²"
    )

    if fr["Estimated Landing Distance (m)"] is not None:

        st.metric(
            "Estimated Landing Distance",
            f"{fr['Estimated Landing Distance (m)']:.2f} m"
        )

    # -------------------------------------------------
    # 3. CLIMB PERFORMANCE
    # -------------------------------------------------

    st.divider()

    st.subheader("3. Climb Performance")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Available Engine Power",
        f"{fr['Available Engine Power (kW)']:.2f} kW"
    )

    c2.metric(
        "Excess Power",
        f"{fr['Excess Power (kW)']:.2f} kW"
    )

    c3.metric(
        "Rate of Climb",
        f"{fr['Rate of Climb (m/s)']:.2f} m/s"
    )

    st.metric(
        "Climb Angle",
        f"{fr['Climb Angle (degrees)']:.2f}°"
    )

    if fr["Rate of Climb (m/s)"] > 0:

        st.success(
            "Positive climb performance under the "
            "selected model assumptions."
        )

    else:

        st.warning(
            "The available power is insufficient for "
            "a positive climb at the selected speed."
        )

    # -------------------------------------------------
    # 4. RANGE AND ENDURANCE
    # -------------------------------------------------

    st.divider()

    st.subheader("4. Range and Endurance Analysis")

    if fr["Estimated Range (km)"] is not None:

        r1, r2, r3 = st.columns(3)

        r1.metric(
            "Fuel Flow",
            f"{fr['Fuel Flow (kg/hour)']:.2f} kg/h"
        )

        r2.metric(
            "Estimated Endurance",
            f"{fr['Estimated Endurance (hours)']:.2f} hours"
        )

        r3.metric(
            "Estimated Flight Range",
            f"{fr['Estimated Range (km)']:.2f} km"
        )

    else:

        st.warning(
            "Range and endurance cannot be estimated "
            "because level flight is not feasible."
        )

    # -------------------------------------------------
    # 5. DETAILED FLIGHT PERFORMANCE TABLE
    # -------------------------------------------------

    st.divider()

    st.subheader("Detailed Flight Performance Results")

    flight_df = pd.DataFrame(
        list(fr.items()),
        columns=["Parameter", "Value"]
    )

    st.dataframe(
        flight_df,
        use_container_width=True,
        hide_index=True
    )
    st.dataframe(
        flight_df,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------------------------------
    # 6. FLIGHT PERFORMANCE GRAPHS
    # -------------------------------------------------

    st.divider()

    st.subheader("5. Flight Performance Graphs")

    st.markdown("#### Drag Force vs Airspeed")

    st.line_chart(
        flight_profile,
        x="Airspeed (m/s)",
        y="Drag Force (N)"
    )

    st.markdown("#### Power Required vs Airspeed")

    st.line_chart(
        flight_profile,
        x="Airspeed (m/s)",
        y="Power Required (kW)"
    )

    st.markdown("#### Rate of Climb vs Airspeed")

    st.line_chart(
        flight_profile,
        x="Airspeed (m/s)",
        y="Rate of Climb (m/s)"
    )

    st.markdown("#### Stall Speed vs Altitude")

    st.line_chart(
        altitude_profile,
        x="Altitude (m)",
        y="Stall Speed (km/h)"
    )

    # -------------------------------------------------
    # 7. DOWNLOAD REPORT
    # -------------------------------------------------

    st.divider()

    st.subheader("Download Flight Performance Report")

    st.download_button(
        "Download Flight Analysis CSV",
        data=flight_df.to_csv(index=False),
        file_name="aircraft_flight_performance.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.download_button(
        "Download Flight Envelope Data",
        data=flight_profile.to_csv(index=False),
        file_name="aircraft_flight_envelope.csv",
        mime="text/csv",
        use_container_width=True
    )

    # -------------------------------------------------
    # 8. ENGINEERING ASSUMPTIONS
    # -------------------------------------------------

    with st.expander("Flight Analysis Model Assumptions"):

        st.markdown("""
        **Take-off**
        - Take-off speed is estimated as 1.20 times stall speed.
        - Average ground-roll speed is approximated as 70% of take-off speed.
        - Constant thrust and average acceleration are assumed.
        - A 15% allowance is applied to estimated ground roll.

        **Landing**
        - Touchdown speed is estimated as 1.15 times stall speed.
        - Average aerodynamic lift and drag are used.
        - Constant braking friction and deceleration are assumed.
        - A 15% allowance is applied to estimated ground roll.

        **Climb**
        - Rate of climb is calculated from excess propulsive power.
        - Available engine power is converted using propeller efficiency.

        **Range and Endurance**
        - Constant operating speed and aerodynamic drag are assumed.
        - Fuel consumption is based on the supplied BSFC.
        - Fuel reserves, changing aircraft mass and mission phases are ignored.

        **Atmosphere**
        - Standard ISA atmosphere is used for the altitude graph.
        - The altitude graph represents stall speed only, not a complete
          aircraft flight envelope.
        """)

    st.warning(
        "These are preliminary educational estimates. "
        "They are not certified take-off, landing, range "
        "or flight-safety predictions."
    )

else:

    st.info(
        "Enter the engine and fuel parameters above "
        "and click Analyze Flight Performance."
    )


# =====================================================
# MODULE 6: AIRCRAFT GEOMETRY AND 3D VISUALIZATION
# =====================================================

st.divider()

st.header("6. Aircraft Geometry & 3D Visualization")

st.write(
    "Explore aircraft geometry through interactive "
    "3D visualization and aerodynamic wing calculations."
)

st.info(
    "Modify the design parameters to generate a "
    "simplified 3D aircraft geometry model."
)

# -----------------------------------------------------
# DESIGN INPUTS
# -----------------------------------------------------

st.subheader("Aircraft Geometry Parameters")

with st.form("aircraft_geometry_form"):

    gcol1, gcol2 = st.columns(2)

    with gcol1:

        geometry_area = st.number_input(
            "Wing Area (m²)",
            min_value=1.0,
            value=float(wing_area),
            key="geometry_area"
        )

        geometry_span = st.number_input(
            "Wingspan (m)",
            min_value=1.0,
            value=float(wingspan),
            key="geometry_span"
        )

        geometry_sweep = st.number_input(
            "Wing Sweep Angle (degrees)",
            min_value=0.0,
            max_value=60.0,
            value=15.0,
            key="geometry_sweep"
        )

    with gcol2:

        geometry_taper = st.number_input(
            "Wing Taper Ratio",
            min_value=0.05,
            max_value=1.0,
            value=0.50,
            step=0.05,
            key="geometry_taper"
        )

        fuselage_length = st.number_input(
            "Fuselage Length (m)",
            min_value=2.0,
            value=8.0,
            key="fuselage_length"
        )

        fuselage_diameter = st.number_input(
            "Fuselage Diameter (m)",
            min_value=0.2,
            value=1.2,
            key="fuselage_diameter"
        )

        tail_span = st.number_input(
            "Horizontal Tail Span (m)",
            min_value=0.5,
            value=3.5,
            key="tail_span"
        )

    geometry_button = st.form_submit_button(
        "Generate 3D Aircraft Model",
        type="primary",
        use_container_width=True
    )


# -----------------------------------------------------
# GENERATE AIRCRAFT GEOMETRY
# -----------------------------------------------------

if geometry_button:

    try:

        geometry_results = calculate_wing_geometry(
            geometry_area,
            geometry_span,
            geometry_taper
        )

        aircraft_fig = create_aircraft_3d(
            geometry_area,
            geometry_span,
            geometry_sweep,
            geometry_taper,
            fuselage_length,
            fuselage_diameter,
            tail_span
        )

        st.session_state["geometry_results"] = geometry_results

        st.session_state["aircraft_fig"] = aircraft_fig

        st.success(
            "Aircraft geometry generated successfully!"
        )

    except ValueError as error:

        st.error(str(error))

    except Exception as error:

        st.error(f"Geometry generation error: {error}")


# -----------------------------------------------------
# DISPLAY 3D MODEL
# -----------------------------------------------------

if "aircraft_fig" in st.session_state:

    st.divider()

    st.subheader("Interactive 3D Aircraft Model")

    st.caption(
        "Use your mouse to rotate, zoom and explore "
        "the aircraft from different angles."
    )

    st.plotly_chart(
        st.session_state["aircraft_fig"],
        use_container_width=True
    )

    # -------------------------------------------------
    # WING GEOMETRY RESULTS
    # -------------------------------------------------

    st.divider()

    st.subheader("Wing Geometry Analysis")

    gr = st.session_state["geometry_results"]

    gc1, gc2, gc3 = st.columns(3)

    gc1.metric(
        "Aspect Ratio",
        f"{gr['Aspect Ratio']:.2f}"
    )

    gc2.metric(
        "Root Chord",
        f"{gr['Root Chord (m)']:.3f} m"
    )

    gc3.metric(
        "Tip Chord",
        f"{gr['Tip Chord (m)']:.3f} m"
    )

    gc4, gc5, gc6 = st.columns(3)

    gc4.metric(
        "Mean Aerodynamic Chord",
        f"{gr['Mean Aerodynamic Chord (m)']:.3f} m"
    )

    gc5.metric(
        "Wing Area",
        f"{gr['Wing Area (m²)']:.2f} m²"
    )

    gc6.metric(
        "Wingspan",
        f"{gr['Wingspan (m)']:.2f} m"
    )

    # -------------------------------------------------
    # DETAILED GEOMETRY TABLE
    # -------------------------------------------------

    st.divider()

    st.subheader("Detailed Geometry Parameters")

    geometry_df = pd.DataFrame(
        list(gr.items()),
        columns=["Parameter", "Value"]
    )

    st.dataframe(
        geometry_df,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------------------------------
    # DOWNLOAD GEOMETRY REPORT
    # -------------------------------------------------

    st.download_button(
        "Download Aircraft Geometry Report",
        data=geometry_df.to_csv(index=False),
        file_name="aircraft_geometry_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    # -------------------------------------------------
    # ENGINEERING ASSUMPTIONS
    # -------------------------------------------------

    with st.expander("Geometry Model Assumptions"):

        st.markdown("""
        - The main wing is modelled as a symmetric trapezoidal wing.
        - The wing area is the total area of both wing halves.
        - The taper ratio is the tip chord divided by root chord.
        - The horizontal tail is represented by a simplified trapezoid.
        - The vertical tail is represented by a simplified triangular surface.
        - The fuselage is represented by an idealized elliptical body.
        - The model is intended for visualization and preliminary geometry study.

        This is not a detailed CAD model or a validated aerodynamic simulation.
        """)

else:

    st.info(
        "Enter aircraft geometry parameters and click "
        "'Generate 3D Aircraft Model' to visualize your design."
    )


# =====================================================
# MODULE 7: PDF ENGINEERING REPORT GENERATOR
# =====================================================

st.divider()

st.header("7. Engineering Report Generator")

st.write(
    "Generate a PDF report containing the saved basic and "
    "advanced aircraft performance results."
)

if (
    "basic_results" in st.session_state
    and "advanced_results" in st.session_state
):

    if st.button(
        "Generate Aircraft PDF Report",
        type="primary",
        use_container_width=True
    ):

        combined_results = {}

        for key, value in st.session_state["basic_results"].items():
            combined_results[f"Basic - {key}"] = value

        for key, value in st.session_state["advanced_results"].items():
            combined_results[f"Advanced - {key}"] = value

        try:

            report_file = generate_aircraft_report(
                combined_results,
                "aircraft_performance_report.pdf"
            )

            with open(report_file, "rb") as pdf:
                pdf_data = pdf.read()

            st.success("PDF report generated successfully!")

            st.download_button(
                label="Download Aircraft Engineering Report",
                data=pdf_data,
                file_name="Aircraft_Performance_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as error:

            st.error(f"Report generation failed: {error}")

else:

    st.info(
        "First enter the aircraft parameters in the sidebar and click "
        "'Analyze Aircraft'. The PDF report will then become available."
    )


# =====================================================
# APPLICATION FOOTER
# =====================================================

st.divider()

st.caption(
    "Aircraft Design & Performance Analysis System | "
    "Def-Space Autumn Internship 2026 | "
    "Developed by MD Reza"
)