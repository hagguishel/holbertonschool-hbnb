# HBnB API Project

This project is a modular and scalable RESTful API for the HBnB platform, built using **Flask** and **Flask-RESTx**. It follows a clean architecture with separation of concerns between the API (presentation layer), business logic, and persistence.

---

## 📁 Project Structure

hbnb/
├── app/
│ ├── init.py # Initializes Flask app and API
│ ├── api/ # API routes (organized by version)
│ │ ├── init.py
│ │ └── v1/
│ │ ├── init.py
│ │ ├── users.py # User-related endpoints
│ │ ├── places.py # Place-related endpoints
│ │ ├── reviews.py # Review-related endpoints
│ │ └── amenities.py # Amenity-related endpoints
│ ├── models/ # Business logic / domain models
│ │ ├── init.py
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── review.py
│ │ └── amenity.py
│ ├── services/ # Facade pattern for orchestration
│ │ ├── init.py
│ │ └── facade.py
│ └── persistence/ # In-memory repository (will be replaced by DB)
│ ├── init.py
│ └── repository.py
├── run.py # Entry point to run the app
├── config.py # App configuration
├── requirements.txt # List of Python dependencies
└── README.md # Project documentation

---

## ✅ Features

- Flask-based REST API with clean structure
- In-memory data storage (can be replaced by a database)
- Placeholder endpoints for users, places, reviews, amenities
- Centralized facade layer to access repositories and logic
- Ready for Swagger UI at `/api/v1/`

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/JulienPul/holbertonschool-hbnb.git
cd holbertonschool-hbnb

2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

🚀 Running the App

python run.py

Then open your browser at:
👉 http://127.0.0.1:5000/api/v1/

You should see the Swagger UI (auto-generated docs from Flask-RESTx).

🔧 Configuration
The file config.py defines settings for the app. You can switch between development/production modes by modifying:

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

📌 Notes
The current persistence layer uses an in-memory repository (InMemoryRepository)

A real database will be integrated in the next phase using SQLAlchemy

The HBnBFacade class acts as the single access point to business operations and storage

🛠️ Technologies
Python 3.8+

Flask

Flask-RESTx

REST API principles

Clean architecture pattern

📚 License
This project is part of the Holberton School curriculum and is intended for educational
---

