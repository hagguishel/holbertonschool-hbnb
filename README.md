 # HBnB API Project

This project is a modular and scalable RESTful API for the HBnB platform, built using **Flask** and **Flask-RESTx**. It follows a clean architecture with separation of concerns between the API (presentation layer), business logic, and persistence.

---

## 📁 Project Structure

```
hbnb/
├── app/
│   ├── __init__.py               # Initializes Flask app and API
│   ├── api/                      # API routes (organized by version)
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py          # User-related endpoints
│   │       ├── places.py         # Place-related endpoints
│   │       ├── reviews.py        # Review-related endpoints
│   │       └── amenities.py      # Amenity-related endpoints
│   ├── models/                   # Business logic / domain models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/                 # Facade pattern for orchestration
│   │   ├── __init__.py
│   │   └── facade.py
│   └── repositories/            # In-memory repository (replaceable by DB)
│       ├── __init__.py
│       └── in_memory.py
├── run.py                        # Entry point to run the app
├── config.py                     # App configuration
├── requirements.txt              # List of Python dependencies
└── README.md                     # Project documentation
```

---

## ✅ Features

- Flask-based REST API with clean modular structure
- In-memory data storage (easily swappable with database)
- CRUD endpoints for users, places, reviews, and amenities
- Centralized facade layer for orchestrating business logic
- Integrated Swagger UI documentation (`/api/v1/`)

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/JulienPul/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the App

```bash
python run.py
```

Then open your browser at:  
👉 [http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)

You will see the **Swagger UI**, auto-generated by Flask-RESTx.

---

## 🔧 Configuration

The file `config.py` defines application settings. You can switch between environments by changing:

```python
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
```

---

## 📌 Notes

- The app currently uses an **in-memory repository** (`InMemoryRepository`)  
- A real database (e.g., PostgreSQL with SQLAlchemy) will be added in future versions  
- The `HBnBFacade` class acts as the **single point of access** to logic and storage

---

## 🧪 Testing

### Automated Tests

```bash
pytest
```

Make sure `run.py` and `create_app()` are correctly configured to accept the in-memory repository.

### Manual Tests with cURL

#### ✅ Create a User

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ -H "Content-Type: application/json" -d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}'
```

#### ❌ Invalid Email

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ -H "Content-Type: application/json" -d '{
  "first_name": "",
  "last_name": "Doe",
  "email": "notanemail"
}'
```

---

## 📚 Technologies

- Python 3.8+
- Flask
- Flask-RESTx
- REST principles
- Clean architecture

---

## 🧾 License

This project is part of the Holberton School curriculum and is intended for educational purposes only.

## Authors
developpers :
Haggui Razafimaitso
github: https://github.com/hagguishel
Julien Pulon
github: https://github.com/JulienPul
updated: 20/06/2025