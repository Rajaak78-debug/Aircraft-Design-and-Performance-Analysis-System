
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_aircraft_report(results, filename="aircraft_report.pdf"):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            "Aircraft Design & Performance Analysis Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Def-Space Autumn Internship 2026",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "Developed by MD Rajaak",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            "Aircraft Performance Results",
            styles["Heading2"]
        )
    )

    table_data = [["Parameter", "Calculated Value"]]

    for parameter, value in results.items():
        table_data.append([
            str(parameter),
            str(value)
        ])

    table = Table(
        table_data,
        colWidths=[3.2 * inch, 2.5 * inch]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph(
            "Engineering Disclaimer",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "This report is generated using preliminary "
            "aerodynamic models. Results are intended for "
            "educational and research purposes and should "
            "not be treated as certified aircraft design data.",
            styles["Normal"]
        )
    )

    doc.build(elements)

    return filename
