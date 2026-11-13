# ✈️ Aircraft Design & Performance Analysis System

A Python-based interactive application for preliminary aircraft aerodynamic analysis, performance estimation, design comparison, optimization, and geometry visualization.

**Developed by MD Rajaak**  
**Def-Space Autumn Internship 2026**

> **Disclaimer:** This is an educational preliminary-analysis tool. Its simplified models are not a substitute for validated engineering analysis, flight testing, or certified aircraft-design software.

## 🚀 Project Overview

The Aircraft Design & Performance Analysis System provides an interactive platform to explore aircraft aerodynamic characteristics and estimate performance using user-defined design parameters.

The application uses Python-based engineering calculations and a Streamlit dashboard to present results through tables, graphs, interactive 3D visualization, and downloadable reports.

## ✨ Key Features

### 1. Aircraft Performance Analysis
- Lift and drag force calculations
- Wing loading and aspect ratio
- Stall velocity estimation
- Aerodynamic performance graphs
- CSV report export

### 2. Advanced Aerodynamic Analysis
- Required lift coefficient
- Induced and total drag coefficients
- Level-flight performance estimation
- Lift-to-drag ratio
- Power required
- Advanced aerodynamic graphs

### 3. Aircraft Design Comparison
- Compare two aircraft configurations
- Compare wing loading and stall speed
- Compare drag and power requirements
- Performance comparison charts
- CSV export

### 4. Aircraft Design Optimization
- Wing-area and wingspan design search
- Minimum drag configuration
- Maximum lift-to-drag ratio
- Minimum power configuration
- Feasible design comparison

### 5. Flight Performance Analysis
- Take-off performance estimation
- Landing performance estimation
- Climb performance
- Range and endurance estimation
- Altitude-dependent stall-speed analysis

### 6. Aircraft Geometry & 3D Visualization
- Wing aspect ratio
- Taper ratio
- Root and tip chord
- Mean aerodynamic chord
- Interactive 3D conceptual aircraft model
- Geometry report export

### 7. Engineering Report Generator
- PDF engineering report generation
- Basic and advanced aerodynamic results
- Downloadable report with engineering disclaimer

## 🛠️ Technologies Used

- Python
- Streamlit
- NumPy
- Pandas
- Matplotlib
- Plotly
- ReportLab

## 📁 Project Structure

```text
Aircraft-Design-and-Performance-Analysis-System/
│
├── app.py
├── calculations.py
├── comparison.py
├── optimization.py
├── flight_analysis.py
├── geometry.py
├── visualization.py
├── report_generator.py
├── requirements.txt
├── README.md
├── aircraft_performance_report.pdf
└── reports/
```

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/Rajaak78-debug/Aircraft-Design-and-Performance-Analysis-System.git
cd Aircraft-Design-and-Performance-Analysis-System
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate it on Windows**

```powershell
venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, normally:

`http://localhost:8501`

Enter the aircraft parameters in the sidebar and explore the seven modules.

## 📐 Engineering Assumptions & Limitations

The application uses simplified preliminary aerodynamic models, including:

- Steady and level flight assumptions where applicable.
- Constant air density for selected operating conditions.
- A parabolic drag polar.
- Induced drag estimation using aspect ratio and Oswald efficiency.
- Simplified take-off, landing, climb, range, and endurance calculations.
- An ISA tropospheric density approximation for altitude calculations.

The 3D aircraft model is conceptual and is not a detailed CAD or structural model.

Results are intended for educational and research purposes only. They must not be used for real-world flight or safety-critical decisions.

## 📸 Application Screenshots

Screenshots of the dashboard, aircraft comparison, optimization, flight analysis, 3D geometry, and PDF report can be added to a `screenshots/` directory.

## 👨‍💻 Developer

**MD Rajaak**  
B.Tech – Electronics and Communication Engineering  
Central University of Karnataka

**Internship:** Def-Space Autumn Internship 2026

## 🔗 Repository

[Aircraft Design & Performance Analysis System](https://github.com/Rajaak78-debug/Aircraft-Design-and-Performance-Analysis-System)
