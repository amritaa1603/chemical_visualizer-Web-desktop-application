Chemical Equipment Parameter Visualizer
Hybrid Web and Desktop Analytics Platform
This project is a unified analytics tool designed to monitor chemical equipment parameters across different platforms. It features a single Django backend that serves both a modern React web dashboard and a native PyQt5 desktop application.

How the Hybrid System Works
The core of this project is a shared API. This means:

Any data you upload through the desktop app is immediately available on the web dashboard.

The analytics logic is powered by Pandas, ensuring that statistics like average pressure and temperature are identical on both platforms.

Both frontends track the last 5 datasets stored in a shared SQLite database.

Technology Stack
Backend: Django and Django REST Framework for API orchestration.

Web Frontend: React.js with Chart.js for interactive dashboarding.

Desktop Frontend: PyQt5 with Matplotlib for native data visualization.

Data Processing: Pandas for fast CSV parsing and statistical analysis.

Reporting: ReportLab for generating individual PDF summaries.

Key Features
Smart CSV Parsing: Automatically detects equipment names, types, flowrate, pressure, and temperature.

Dual Visualizations: View equipment distribution using Chart.js on the web and Matplotlib on the desktop.

History Management: Built-in logic to store and display the last 5 uploads.

PDF Export: Create professional summary reports for any upload in your history list.

Setup Instructions
Prerequisites You will need Python 3.9 or higher and Node.js installed on your system.

Backend and Desktop Setup Open your terminal in the root project folder:

Activate your virtual environment: venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux).

Install dependencies: pip install -r requirements.txt.

Prepare the database: python manage.py migrate.

Start the API: python manage.py runserver.

Web Frontend Setup Open a second terminal:

Navigate to the folder: cd frontend.

Install packages: npm install.

Start the dashboard: npm run dev.

Running the Desktop App Open a third terminal (with your virtual environment active):

Run the command: python desktop_app.py.

Sample Data
You can find a file named sample_equipment_data.csv in the main folder to use for your initial testing and demo.