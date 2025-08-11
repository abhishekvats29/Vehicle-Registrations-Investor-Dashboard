# Vehicle Registration Investor Dashboard
## Overview
- This project is an interactive vehicle registration dashboard designed with an investor’s perspective in mind.
- It visualizes Year-over-Year (YoY) and Quarter-over-Quarter (QoQ) growth for different vehicle categories and manufacturers using public Vahan Dashboard data.
- Built with Streamlit, it enables filtering, date range selection, and trend visualization in a clean, professional UI.

---
## Screenshot
- Example investor-friendly dashboard view.
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/b12ae738-4d45-494c-8eba-24779502de69" />


## Tech Stack

- Python (Pandas, NumPy, Requests)
- Streamlit (UI framework)
- Plotly (Interactive charts)
- Requests / BeautifulSoup (Data fetching)
- SQLAlchemy (Optional SQL integration)
- Docker (For containerized deployment)

---

## Data Assumptions

- Data is sourced from Vahan Dashboard or generated as a sample dataset if no live data is available.
- Vehicle categories are standardized to 2W, 3W, and 4W.
- Missing data is handled by interpolation or filling with zeros.
- The data cleaning process ensures consistent manufacturer naming.

---

## Setup Instructions
Clone the repository
- git clone https://github.com/abhishekvats29/Vehicle-Registrations---Investor-Dashboard.git
- cd vehicle-dashboard

Create a virtual environment
- python -m venv .venv
- source .venv/bin/activate   # macOS/Linux
- .venv\Scripts\activate      # Windows

Install dependencies
- pip install -r requirements.txt

Run the data pipeline
- python src/main.py
Launch the dashboard
- streamlit run src/ui.py

Optional – Run via Docker
- docker build -t vehicle-dashboard .
- docker run -p 8501:8501 vehicle-dashboard

---

## Feature Roadmap (If Continued)
- Live API integration with real-time Vahan Dashboard updates.
- Export graphs and reports as PDF for investors.
- Add more granular filters such as state/region-level data.
- Integrate machine learning for future trend forecasting.
- Deploy on cloud (Streamlit Cloud, AWS, or Docker container).

---

## 👤 Author
- Abhishek Vats, Backend developer

- Copyright © 2025 Abhishek Vats. All rights reserved.

## 📄 License
- - This project is Created as part of a hiring process assignment.

