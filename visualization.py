
import numpy as np
import matplotlib.pyplot as plt


def plot_performance(
    mass,
    wing_area,
    air_density,
    lift_coefficient,
    drag_coefficient,
    max_lift_coefficient
):
    gravity = 9.81
    weight = mass * gravity

    # Generate velocity range
    velocities = np.linspace(5, 100, 100)

    # Calculate dynamic pressure
    dynamic_pressure = 0.5 * air_density * velocities**2

    # Calculate lift and drag
    lift = (
        dynamic_pressure
        * wing_area
        * lift_coefficient
    )

    drag = (
        dynamic_pressure
        * wing_area
        * drag_coefficient
    )

    # Calculate stall speed
    stall_speed = np.sqrt(
        (2 * weight) /
        (air_density * wing_area * max_lift_coefficient)
    )

    # Lift and Drag Graph
    fig1, ax1 = plt.subplots(figsize=(8, 4))

    ax1.plot(
        velocities,
        lift,
        label="Lift Force"
    )

    ax1.plot(
        velocities,
        drag,
        label="Drag Force"
    )

    ax1.axvline(
        stall_speed,
        linestyle="--",
        label="Estimated Stall Speed"
    )

    ax1.set_title("Lift and Drag vs Airspeed")
    ax1.set_xlabel("Airspeed (m/s)")
    ax1.set_ylabel("Force (N)")
    ax1.legend()
    ax1.grid(True)

    fig1.tight_layout()

    # Lift-to-Drag Ratio Graph
    ratio = lift / drag

    fig2, ax2 = plt.subplots(figsize=(8, 4))

    ax2.plot(
        velocities,
        ratio,
        label="Lift-to-Drag Ratio"
    )

    ax2.set_title("Lift-to-Drag Ratio vs Airspeed")
    ax2.set_xlabel("Airspeed (m/s)")
    ax2.set_ylabel("L/D Ratio")
    ax2.legend()
    ax2.grid(True)

    fig2.tight_layout()

    return fig1, fig2


def plot_advanced_performance(
    mass,
    wing_area,
    wingspan,
    air_density,
    zero_lift_drag_coefficient,
    oswald_efficiency,
    max_lift_coefficient,
    operating_velocity
):
    gravity = 9.81
    weight = mass * gravity

    aspect_ratio = wingspan**2 / wing_area

    # Calculate stall speed
    stall_speed = np.sqrt(
        (2 * weight) /
        (air_density * wing_area * max_lift_coefficient)
    )

    # Plot only speeds above estimated stall speed
    velocities = np.linspace(
        stall_speed * 1.02,
        max(100, stall_speed * 2.5),
        150
    )

    # Dynamic pressure
    q = 0.5 * air_density * velocities**2

    # Required lift coefficient for level flight
    cl = weight / (q * wing_area)

    # Induced drag coefficient
    cdi = (
        cl**2 /
        (np.pi * oswald_efficiency * aspect_ratio)
    )

    # Total drag coefficient
    cd = zero_lift_drag_coefficient + cdi

    # Drag force
    drag = q * wing_area * cd

    # Lift-to-drag ratio
    ld_ratio = cl / cd

    # Power required
    power = drag * velocities / 1000

    # Calculate operating point
    q_op = 0.5 * air_density * operating_velocity**2
    cl_op = weight / (q_op * wing_area)

    cdi_op = (
        cl_op**2 /
        (np.pi * oswald_efficiency * aspect_ratio)
    )

    cd_op = zero_lift_drag_coefficient + cdi_op
    drag_op = q_op * wing_area * cd_op
    ld_op = cl_op / cd_op
    power_op = drag_op * operating_velocity / 1000

    # Graph 1: Drag versus velocity
    fig1, ax1 = plt.subplots(figsize=(8, 4))

    ax1.plot(velocities, drag, label="Total Drag")

    ax1.axvline(
        operating_velocity,
        linestyle="--",
        label="Operating Speed"
    )

    ax1.set_title("Aircraft Drag vs Airspeed")
    ax1.set_xlabel("Airspeed (m/s)")
    ax1.set_ylabel("Drag Force (N)")
    ax1.grid(True)
    ax1.legend()
    fig1.tight_layout()

    # Graph 2: L/D ratio versus velocity
    fig2, ax2 = plt.subplots(figsize=(8, 4))

    ax2.plot(
        velocities,
        ld_ratio,
        label="Lift-to-Drag Ratio"
    )

    ax2.axvline(
        operating_velocity,
        linestyle="--",
        label="Operating Speed"
    )

    ax2.set_title("Lift-to-Drag Ratio vs Airspeed")
    ax2.set_xlabel("Airspeed (m/s)")
    ax2.set_ylabel("L/D Ratio")
    ax2.grid(True)
    ax2.legend()
    fig2.tight_layout()

    # Graph 3: Power versus velocity
    fig3, ax3 = plt.subplots(figsize=(8, 4))

    ax3.plot(
        velocities,
        power,
        label="Power Required"
    )

    ax3.axvline(
        operating_velocity,
        linestyle="--",
        label="Operating Speed"
    )

    ax3.set_title("Power Required vs Airspeed")
    ax3.set_xlabel("Airspeed (m/s)")
    ax3.set_ylabel("Power (kW)")
    ax3.grid(True)
    ax3.legend()
    fig3.tight_layout()

    return fig1, fig2, fig3
