
import math


def calculate_aircraft_comparison(
    mass,
    wing_area,
    wingspan,
    air_density,
    velocity,
    cd0,
    oswald_efficiency,
    cl_max
):
    """
    Calculate aircraft aerodynamic performance
    for design comparison.
    """

    g = 9.81

    # Basic parameters
    weight = mass * g
    aspect_ratio = (wingspan ** 2) / wing_area
    wing_loading = weight / wing_area

    # Dynamic pressure
    q = 0.5 * air_density * velocity ** 2

    # Stall speed
    stall_speed = math.sqrt(
        (2 * weight) /
        (air_density * wing_area * cl_max)
    )

    # Required lift coefficient for level flight
    required_cl = weight / (q * wing_area)

    # Induced drag coefficient
    k = 1 / (
        math.pi * oswald_efficiency * aspect_ratio
    )

    induced_cd = k * required_cl ** 2

    # Total drag coefficient
    total_cd = cd0 + induced_cd

    # Level flight validity
    level_flight_valid = required_cl <= cl_max

    if level_flight_valid:

        # Drag force
        drag_force = q * wing_area * total_cd

        # Power required
        power_required = drag_force * velocity

        # Lift-to-drag ratio
        lift_to_drag = weight / drag_force

    else:
        drag_force = None
        power_required = None
        lift_to_drag = None

    # Maximum theoretical L/D ratio
    # For a parabolic drag polar
    cl_at_max_ld = math.sqrt(cd0 / k)

    max_ld_ratio = 1 / (
        2 * math.sqrt(cd0 * k)
    )

    # Speed at maximum L/D in level flight
    speed_at_max_ld = math.sqrt(
        (2 * weight) /
        (air_density * wing_area * cl_at_max_ld)
    )

    return {
        "Aircraft Mass (kg)": mass,
        "Weight (N)": weight,
        "Wing Area (m²)": wing_area,
        "Wingspan (m)": wingspan,
        "Wing Loading (N/m²)": wing_loading,
        "Aspect Ratio": aspect_ratio,
        "Stall Speed (m/s)": stall_speed,
        "Stall Speed (km/h)": stall_speed * 3.6,
        "Operating Speed (m/s)": velocity,
        "Required Lift Coefficient": required_cl,
        "Induced Drag Coefficient": induced_cd,
        "Total Drag Coefficient": total_cd,
        "Drag Force (N)": drag_force,
        "Power Required (kW)": (
            power_required / 1000
            if power_required is not None else None
        ),
        "Lift-to-Drag Ratio": lift_to_drag,
        "Maximum L/D Ratio": max_ld_ratio,
        "Speed at Maximum L/D (m/s)": speed_at_max_ld,
        "Level Flight Valid": level_flight_valid
    }
