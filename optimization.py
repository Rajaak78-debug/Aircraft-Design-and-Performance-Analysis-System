
import numpy as np
import pandas as pd


def optimize_aircraft_design(
    mass,
    air_density,
    velocity,
    cd0,
    oswald_efficiency,
    clmax,
    area_min,
    area_max,
    span_min,
    span_max,
    samples=40
):
    """
    Search for aircraft wing configurations with:
    1. Minimum drag
    2. Maximum lift-to-drag ratio
    3. Minimum power required

    Only configurations satisfying the selected
    operating-speed stall constraint are considered.
    """

    # Validate inputs
    if mass <= 0 or air_density <= 0 or velocity <= 0:
        raise ValueError("Mass, density and velocity must be positive.")

    if cd0 <= 0 or oswald_efficiency <= 0 or clmax <= 0:
        raise ValueError("Aerodynamic coefficients must be positive.")

    if area_min <= 0 or area_max <= area_min:
        raise ValueError("Invalid wing area range.")

    if span_min <= 0 or span_max <= span_min:
        raise ValueError("Invalid wingspan range.")

    # Fundamental flight parameters
    g = 9.81
    weight = mass * g
    dynamic_pressure = 0.5 * air_density * velocity**2

    # Generate design configurations
    areas = np.linspace(area_min, area_max, samples)
    spans = np.linspace(span_min, span_max, samples)

    area_grid, span_grid = np.meshgrid(areas, spans)

    # Calculate aspect ratio
    aspect_ratio = span_grid**2 / area_grid

    # Required lift coefficient for level flight
    cl_required = weight / (dynamic_pressure * area_grid)

    # Induced drag coefficient
    cd_induced = (
        cl_required**2 /
        (np.pi * oswald_efficiency * aspect_ratio)
    )

    # Total drag coefficient
    cd_total = cd0 + cd_induced

    # Drag force
    drag_force = dynamic_pressure * area_grid * cd_total

    # Power required
    power_required = drag_force * velocity

    # Lift-to-drag ratio
    ld_ratio = cl_required / cd_total

    # Stall speed
    stall_speed = np.sqrt(
        (2 * weight) /
        (air_density * area_grid * clmax)
    )

    # Valid level-flight configurations
    valid = cl_required <= clmax

    if not np.any(valid):
        raise ValueError(
            "No feasible design found. Increase the maximum "
            "wing area or operating speed, or adjust CLmax."
        )

    # Prepare results table
    df = pd.DataFrame({
        "Wing Area (m²)": area_grid[valid],
        "Wingspan (m)": span_grid[valid],
        "Aspect Ratio": aspect_ratio[valid],
        "Required CL": cl_required[valid],
        "Total CD": cd_total[valid],
        "Drag Force (N)": drag_force[valid],
        "Power Required (kW)": power_required[valid] / 1000,
        "Lift-to-Drag Ratio": ld_ratio[valid],
        "Stall Speed (m/s)": stall_speed[valid]
    })

    # Best design for minimum drag
    minimum_drag_design = (
        df.loc[df["Drag Force (N)"].idxmin()].to_dict()
    )

    # Best design for maximum aerodynamic efficiency
    maximum_ld_design = (
        df.loc[df["Lift-to-Drag Ratio"].idxmax()].to_dict()
    )

    # Best design for minimum power
    minimum_power_design = (
        df.loc[df["Power Required (kW)"].idxmin()].to_dict()
    )

    # Return optimization results
    return {
        "minimum_drag": minimum_drag_design,
        "maximum_ld": maximum_ld_design,
        "minimum_power": minimum_power_design,
        "all_designs": df.sort_values(
            "Drag Force (N)"
        ).reset_index(drop=True)
    }
