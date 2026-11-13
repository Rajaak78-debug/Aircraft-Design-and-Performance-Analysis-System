
import numpy as np
import plotly.graph_objects as go


def calculate_wing_geometry(wing_area, wingspan, taper_ratio):

    if wing_area <= 0 or wingspan <= 0:
        raise ValueError("Wing area and wingspan must be positive.")

    if not 0.05 <= taper_ratio <= 1.0:
        raise ValueError("Taper ratio must be between 0.05 and 1.0.")

    aspect_ratio = wingspan**2 / wing_area

    root_chord = (
        2 * wing_area /
        (wingspan * (1 + taper_ratio))
    )

    tip_chord = taper_ratio * root_chord

    mean_aerodynamic_chord = (
        (2 / 3) * root_chord *
        (1 + taper_ratio + taper_ratio**2) /
        (1 + taper_ratio)
    )

    return {
        "Wing Area (m²)": wing_area,
        "Wingspan (m)": wingspan,
        "Aspect Ratio": aspect_ratio,
        "Taper Ratio": taper_ratio,
        "Root Chord (m)": root_chord,
        "Tip Chord (m)": tip_chord,
        "Mean Aerodynamic Chord (m)": mean_aerodynamic_chord
    }


def add_trapezoid_wing(
    fig, span, root_chord, tip_chord,
    x_position, sweep_angle, z_position,
    color, name
):

    half_span = span / 2

    sweep_offset = half_span * np.tan(
        np.radians(sweep_angle)
    )

    # Right and left wing
    for side in [-1, 1]:

        y = [
            0,
            0,
            side * half_span,
            side * half_span
        ]

        x = [
            x_position,
            x_position + root_chord,
            x_position + sweep_offset + tip_chord,
            x_position + sweep_offset
        ]

        z = [z_position] * 4

        fig.add_trace(
            go.Mesh3d(
                x=x,
                y=y,
                z=z,
                i=[0, 0],
                j=[1, 2],
                k=[2, 3],
                color=color,
                opacity=0.85,
                name=name,
                showlegend=(side == 1)
            )
        )


def create_aircraft_3d(
    wing_area,
    wingspan,
    sweep_angle,
    taper_ratio,
    fuselage_length,
    fuselage_diameter,
    tail_span
):

    geometry = calculate_wing_geometry(
        wing_area,
        wingspan,
        taper_ratio
    )

    root_chord = geometry["Root Chord (m)"]
    tip_chord = geometry["Tip Chord (m)"]

    fig = go.Figure()

    # -------------------------------------------------
    # 1. FUSELAGE
    # -------------------------------------------------

    x_values = np.linspace(
        -0.08 * fuselage_length,
        0.92 * fuselage_length,
        50
    )

    theta = np.linspace(
        0, 2 * np.pi, 30
    )

    X, T = np.meshgrid(x_values, theta)

    radius = (
        fuselage_diameter / 2
    ) * np.sin(
        np.pi * (X - x_values.min()) /
        (x_values.max() - x_values.min())
    )**0.35

    Y = radius * np.cos(T)
    Z = radius * np.sin(T)

    fig.add_trace(
        go.Surface(
            x=X,
            y=Y,
            z=Z,
            colorscale="Blues",
            showscale=False,
            opacity=0.9,
            name="Fuselage"
        )
    )

    # -------------------------------------------------
    # 2. MAIN WING
    # -------------------------------------------------

    add_trapezoid_wing(
        fig,
        wingspan,
        root_chord,
        tip_chord,
        0.32 * fuselage_length,
        sweep_angle,
        0,
        "royalblue",
        "Main Wing"
    )

    # -------------------------------------------------
    # 3. HORIZONTAL TAIL
    # -------------------------------------------------

    tail_root_chord = 0.22 * root_chord
    tail_tip_chord = 0.60 * tail_root_chord

    add_trapezoid_wing(
        fig,
        tail_span,
        tail_root_chord,
        tail_tip_chord,
        0.76 * fuselage_length,
        20,
        0,
        "orange",
        "Horizontal Tail"
    )

    # -------------------------------------------------
    # 4. VERTICAL TAIL
    # -------------------------------------------------

    tail_x = 0.78 * fuselage_length

    fin_x = [
        tail_x,
        tail_x + 0.16 * root_chord,
        tail_x + 0.09 * root_chord
    ]

    fin_y = [0, 0, 0]

    fin_z = [
        fuselage_diameter / 2,
        fuselage_diameter / 2,
        0.55 * fuselage_diameter
    ]

    fig.add_trace(
        go.Mesh3d(
            x=fin_x,
            y=fin_y,
            z=fin_z,
            i=[0],
            j=[1],
            k=[2],
            color="crimson",
            opacity=0.9,
            name="Vertical Tail"
        )
    )

    # -------------------------------------------------
    # 5. GRAPH LAYOUT
    # -------------------------------------------------

    fig.update_layout(
        title="Interactive 3D Aircraft Geometry Model",
        scene=dict(
            xaxis_title="Aircraft Length (m)",
            yaxis_title="Wingspan Direction (m)",
            zaxis_title="Height (m)",
            aspectmode="data",
            camera=dict(
                eye=dict(x=1.6, y=1.5, z=1.2)
            )
        ),
        height=650,
        margin=dict(l=0, r=0, t=60, b=0),
        showlegend=True
    )

    return fig
