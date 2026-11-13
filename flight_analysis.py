
import numpy as np
import pandas as pd


def isa_air_density(altitude):
    """
    Estimate ISA air density in the troposphere.
    Valid for altitudes from 0 to 11,000 metres.
    """

    if altitude < 0 or altitude > 11000:
        raise ValueError("Altitude must be between 0 and 11000 m.")

    temperature = 288.15 - 0.0065 * altitude

    pressure = 101325 * (
        temperature / 288.15
    ) ** 5.25588

    density = pressure / (287.05 * temperature)

    return density


def calculate_flight_performance(
    mass,
    wing_area,
    wingspan,
    air_density,
    velocity,
    cd0,
    oswald_efficiency,
    clmax,
    thrust,
    available_power_kw,
    fuel_mass,
    bsfc,
    propeller_efficiency,
    rolling_friction,
    braking_friction
):
    """
    Preliminary flight performance calculations:
    - Take-off performance
    - Landing performance
    - Climb performance
    - Range and endurance
    """

    # Input validation
    if min(
        mass, wing_area, wingspan, air_density,
        velocity, cd0, oswald_efficiency, clmax,
        available_power_kw, fuel_mass, bsfc,
        propeller_efficiency
    ) <= 0:
        raise ValueError("Physical input values must be positive.")

    if oswald_efficiency > 1 or propeller_efficiency > 1:
        raise ValueError("Efficiency factors cannot exceed 1.")

    if rolling_friction < 0 or braking_friction < 0:
        raise ValueError("Friction coefficients cannot be negative.")

    if braking_friction == 0:
        raise ValueError("Braking friction must be greater than zero.")

    if thrust < 0:
        raise ValueError("Thrust cannot be negative.")

    g = 9.81

    weight = mass * g

    aspect_ratio = wingspan**2 / wing_area

    # Dynamic pressure at operating speed
    q = 0.5 * air_density * velocity**2

    # Stall speed
    stall_speed = np.sqrt(
        (2 * weight) /
        (air_density * wing_area * clmax)
    )

    # Required lift coefficient
    cl_required = weight / (q * wing_area)

    flight_valid = cl_required <= clmax

    # Aerodynamic drag at operating speed
    cd_induced = (
        cl_required**2 /
        (np.pi * oswald_efficiency * aspect_ratio)
    )

    total_cd = cd0 + cd_induced

    drag = q * wing_area * total_cd

    power_required = drag * velocity / 1000

    # -------------------------------------------------
    # 1. TAKE-OFF PERFORMANCE
    # -------------------------------------------------

    takeoff_speed = 1.20 * stall_speed

    average_takeoff_speed = 0.70 * takeoff_speed

    q_takeoff = (
        0.5 * air_density * average_takeoff_speed**2
    )

    cl_takeoff = 0.80 * clmax

    lift_takeoff = (
        q_takeoff * wing_area * cl_takeoff
    )

    cd_takeoff = (
        cd0 +
        cl_takeoff**2 /
        (np.pi * oswald_efficiency * aspect_ratio)
    )

    drag_takeoff = (
        q_takeoff * wing_area * cd_takeoff
    )

    rolling_resistance = (
        rolling_friction *
        max(weight - lift_takeoff, 0)
    )

    takeoff_acceleration = (
        thrust - drag_takeoff - rolling_resistance
    ) / mass

    if takeoff_acceleration > 0:

        takeoff_ground_roll = (
            takeoff_speed**2 /
            (2 * takeoff_acceleration)
        )

        takeoff_distance = 1.15 * takeoff_ground_roll

    else:

        takeoff_ground_roll = None
        takeoff_distance = None

    # -------------------------------------------------
    # 2. LANDING PERFORMANCE
    # -------------------------------------------------

    touchdown_speed = 1.15 * stall_speed

    average_landing_speed = 0.70 * touchdown_speed

    q_landing = (
        0.5 * air_density * average_landing_speed**2
    )

    cl_landing = 0.80 * clmax

    lift_landing = (
        q_landing * wing_area * cl_landing
    )

    cd_landing = (
        cd0 +
        cl_landing**2 /
        (np.pi * oswald_efficiency * aspect_ratio)
    )

    drag_landing = (
        q_landing * wing_area * cd_landing
    )

    braking_force = (
        braking_friction *
        max(weight - lift_landing, 0)
        + drag_landing
    )

    landing_deceleration = braking_force / mass

    if landing_deceleration > 0:

        landing_ground_roll = (
            touchdown_speed**2 /
            (2 * landing_deceleration)
        )

        landing_distance = 1.15 * landing_ground_roll

    else:

        landing_ground_roll = None
        landing_distance = None

    # -------------------------------------------------
    # 3. CLIMB PERFORMANCE
    # -------------------------------------------------

    useful_power = (
        available_power_kw *
        propeller_efficiency
    )

    power_excess = (
        useful_power * 1000 -
        drag * velocity
    )

    rate_of_climb = power_excess / weight

    climb_angle_sine = np.clip(
        rate_of_climb / velocity,
        -1,
        1
    )

    climb_angle = np.degrees(
        np.arcsin(climb_angle_sine)
    )

    # -------------------------------------------------
    # 4. RANGE AND ENDURANCE
    # -------------------------------------------------

    shaft_power_for_flight = (
        power_required /
        propeller_efficiency
    )

    if flight_valid and shaft_power_for_flight > 0:

        fuel_flow = (
            bsfc * shaft_power_for_flight
        )

        endurance_hours = fuel_mass / fuel_flow

        estimated_range = (
            velocity * 3.6 * endurance_hours
        )

    else:

        fuel_flow = None
        endurance_hours = None
        estimated_range = None

    # -------------------------------------------------
    # RETURN RESULTS
    # -------------------------------------------------

    return {
        "Weight (N)": weight,
        "Aspect Ratio": aspect_ratio,
        "Stall Speed (m/s)": stall_speed,
        "Stall Speed (km/h)": stall_speed * 3.6,
        "Operating Speed (m/s)": velocity,
        "Required Lift Coefficient": cl_required,
        "Operating Flight Valid": flight_valid,

        "Drag Force (N)": drag,
        "Power Required (kW)": power_required,

        "Take-off Speed (km/h)": takeoff_speed * 3.6,
        "Take-off Acceleration (m/s²)": takeoff_acceleration,
        "Take-off Ground Roll (m)": takeoff_ground_roll,
        "Estimated Take-off Distance (m)": takeoff_distance,

        "Touchdown Speed (km/h)": touchdown_speed * 3.6,
        "Landing Deceleration (m/s²)": landing_deceleration,
        "Landing Ground Roll (m)": landing_ground_roll,
        "Estimated Landing Distance (m)": landing_distance,

        "Available Engine Power (kW)": available_power_kw,
        "Useful Propulsive Power (kW)": useful_power,
        "Excess Power (kW)": power_excess / 1000,
        "Rate of Climb (m/s)": rate_of_climb,
        "Climb Angle (degrees)": climb_angle,

        "Fuel Flow (kg/hour)": fuel_flow,
        "Estimated Endurance (hours)": endurance_hours,
        "Estimated Endurance (minutes)": (
            endurance_hours * 60
            if endurance_hours is not None else None
        ),
        "Estimated Range (km)": estimated_range
    }


def generate_flight_performance_data(
    mass,
    wing_area,
    wingspan,
    air_density,
    cd0,
    oswald_efficiency,
    clmax,
    available_power_kw,
    propeller_efficiency,
    operating_velocity
):
    """
    Generate speed-dependent drag, power and climb data.
    """

    weight = mass * 9.81

    aspect_ratio = wingspan**2 / wing_area

    stall_speed = np.sqrt(
        (2 * weight) /
        (air_density * wing_area * clmax)
    )

    speeds = np.linspace(
        1.05 * stall_speed,
        max(2.5 * stall_speed, 1.5 * operating_velocity),
        100
    )

    q = 0.5 * air_density * speeds**2

    cl = weight / (q * wing_area)

    cd_induced = (
        cl**2 /
        (np.pi * oswald_efficiency * aspect_ratio)
    )

    cd = cd0 + cd_induced

    drag = q * wing_area * cd

    power = drag * speeds / (
        1000 * propeller_efficiency
    )

    useful_power = (
        available_power_kw * propeller_efficiency
    )

    climb_rate = (
        useful_power * 1000 - drag * speeds
    ) / weight

    valid = cl <= clmax

    return pd.DataFrame({
        "Airspeed (m/s)": speeds[valid],
        "Drag Force (N)": drag[valid],
        "Power Required (kW)": power[valid],
        "Rate of Climb (m/s)": climb_rate[valid]
    })


def generate_altitude_data(
    mass,
    wing_area,
    clmax
):
    """
    Calculate stall speed at different altitudes
    using the ISA tropospheric density model.
    """

    altitudes = np.arange(0, 11001, 500)

    weight = mass * 9.81

    stall_speeds = []

    for altitude in altitudes:

        density = isa_air_density(altitude)

        speed = np.sqrt(
            (2 * weight) /
            (density * wing_area * clmax)
        )

        stall_speeds.append(speed)

    return pd.DataFrame({
        "Altitude (m)": altitudes,
        "Stall Speed (m/s)": stall_speeds,
        "Stall Speed (km/h)": (
            np.array(stall_speeds) * 3.6
        )
    })
