
import math


def calculate_aircraft_performance(
    mass,
    wing_area,
    wingspan,
    velocity,
    air_density,
    lift_coefficient,
    drag_coefficient,
    max_lift_coefficient
):
    """
    Calculate basic aircraft aerodynamic parameters.
    SI units are used throughout.
    """

    gravity = 9.81

    # Aircraft weight
    weight = mass * gravity

    # Dynamic pressure
    dynamic_pressure = 0.5 * air_density * velocity**2

    # Lift force
    lift = dynamic_pressure * wing_area * lift_coefficient

    # Drag force
    drag = dynamic_pressure * wing_area * drag_coefficient

    # Wing loading
    wing_loading = weight / wing_area

    # Aspect ratio
    aspect_ratio = wingspan**2 / wing_area

    # Stall velocity
    stall_velocity = math.sqrt(
        (2 * weight) /
        (air_density * wing_area * max_lift_coefficient)
    )

    # Lift-to-drag ratio
    lift_drag_ratio = (
        lift / drag if drag != 0 else 0
    )

    return {
        "Weight (N)": weight,
        "Dynamic Pressure (Pa)": dynamic_pressure,
        "Lift Force (N)": lift,
        "Drag Force (N)": drag,
        "Wing Loading (N/m²)": wing_loading,
        "Aspect Ratio": aspect_ratio,
        "Stall Velocity (m/s)": stall_velocity,
        "Stall Velocity (km/h)": stall_velocity * 3.6,
        "Lift-to-Drag Ratio": lift_drag_ratio
    }



def calculate_advanced_aerodynamics(
    mass,
    wing_area,
    wingspan,
    velocity,
    air_density,
    zero_lift_drag_coefficient,
    oswald_efficiency,
    max_lift_coefficient
):
    """
    Advanced aerodynamic analysis using a parabolic drag polar.
    Assumes steady, level, unaccelerated flight.
    """

    gravity = 9.81

    # Aircraft weight
    weight = mass * gravity

    # Wing aspect ratio
    aspect_ratio = wingspan**2 / wing_area

    # Dynamic pressure
    dynamic_pressure = 0.5 * air_density * velocity**2

    # Required lift coefficient for level flight
    cl_required = weight / (dynamic_pressure * wing_area)

    # Induced drag coefficient
    induced_drag_coefficient = (
        cl_required**2 /
        (math.pi * oswald_efficiency * aspect_ratio)
    )

    # Total drag coefficient
    total_drag_coefficient = (
        zero_lift_drag_coefficient +
        induced_drag_coefficient
    )

    # Calculate lift and drag
    lift_force = dynamic_pressure * wing_area * cl_required

    drag_force = (
        dynamic_pressure *
        wing_area *
        total_drag_coefficient
    )

    # Lift-to-drag ratio
    lift_drag_ratio = cl_required / total_drag_coefficient

    # Power required for level flight
    power_required = drag_force * velocity

    # Calculate stall velocity
    stall_velocity = math.sqrt(
        (2 * weight) /
        (air_density * wing_area * max_lift_coefficient)
    )

    # Check level-flight validity
    is_valid = velocity >= stall_velocity

    return {
        "Required Lift Coefficient": cl_required,
        "Induced Drag Coefficient": induced_drag_coefficient,
        "Zero-Lift Drag Coefficient": zero_lift_drag_coefficient,
        "Total Drag Coefficient": total_drag_coefficient,
        "Level Flight Lift (N)": lift_force,
        "Level Flight Drag (N)": drag_force,
        "Lift-to-Drag Ratio": lift_drag_ratio,
        "Power Required (W)": power_required,
        "Power Required (kW)": power_required / 1000,
        "Stall Velocity (m/s)": stall_velocity,
        "Level Flight Valid": is_valid
    }
