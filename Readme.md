# Chemical Equipment Parameter Visualizer
## Hybrid Web and Desktop Analytics Platform

This project is a unified analytics tool designed to monitor chemical equipment parameters across different platforms. It features a single **Django** backend that serves both a modern **React** web dashboard and a native **PyQt5** desktop application.

---

### How the Hybrid System Works
The core of this project is a shared API. This ensures data consistency and real-time updates across environments:

* **Shared Data:** Any data uploaded through the desktop app is immediately available on the web dashboard via the central database.
* **Unified Logic:** Analytics logic is powered by **Pandas**, ensuring that statistics like average pressure and temperature are identical on both platforms.
* **History Sync:** Both frontends track the last 5 datasets stored in a shared **SQLite** database.



---

### Technology Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Django & Django REST Framework |
| **Web Frontend** | React.js & Chart.js |
| **Desktop Frontend** | PyQt5 & Matplotlib |
| **Data Processing** | Pandas |
| **Reporting** | ReportLab (PDF Generation) |

---

### Key Features
* **Smart CSV Parsing:** Automatically detects equipment names, types, flowrate, pressure, and temperature from raw files.
* **Dual Visualizations:** Interactive equipment distribution charts using **Chart.js** (Web) and **Matplotlib** (Desktop).
* **History Management:** Built-in logic to automatically store and display the last 5 uploads for quick access.
* **PDF Export:** Generate professional, individual summary reports for any upload in your history list.

---

### Setup Instructions

#### 1. Prerequisites
* Python 3.9 or higher
* Node.js (for the React dashboard)

#### 2. Backend and Desktop Setup
Open your terminal in the root project folder:
1.  **Activate virtual environment:**
    * Windows: `venv\Scripts\activate`
    * Mac/Linux: `source venv/bin/activate`
2.  **Install dependencies:** `pip install -r requirements.txt`
3.  **Prepare database:** `python manage.py migrate`
4.  **Start API:** `python manage.py runserver`

#### 3. Web Frontend Setup
Open a second terminal:
1.  **Navigate to folder:** `cd frontend`
2.  **Install packages:** `npm install`
3.  **Start dashboard:** `npm run dev`

#### 4. Running the Desktop App
Open a third terminal (with your virtual environment active):
1.  **Run command:** `python desktop_app.py`

---

### Sample Data
A file named `sample_equipment_data.csv` is included in the main folder. Use this file for initial testing to see how the system parses and visualizes parameters.
