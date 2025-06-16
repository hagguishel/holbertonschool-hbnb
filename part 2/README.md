# HBnB API Project

This project is a modular and scalable RESTful API for the HBnB platform, built using Flask and Flask-RESTx. It follows a clean architecture with clear separation of concerns between the presentation layer (API), business logic (models and services), and persistence (in-memory repository for now).

## 📁 Project Structure

hbnb/  
├── app/  
│   ├── __init__.py  
│   ├── api/  
│   │   ├── __init__.py  
│   │   └── v1/  
│   │       ├── __init__.py  
│   │       ├── users.py  
│   │       ├── places.py  
│   │       ├── reviews.py  
│   │       └── amenities.py  
│   ├── models/  
│   │   ├── __init__.py  
│   │   ├── user.py  
│   │   ├── place.py  
│   │   ├── review.py  
│   │   └── amenity.py  
│   ├── services/  
│   │   ├── __init__.py  
│   │   └── facade.py  
│   └── persistence/  
│       ├── __init__.py  
│       └── repository.py  
├── run.py  
├── config.py  
├── requirements.txt  
└── README.md

## ✅ Features

- Flask-based REST API  
- Clean, scalable project architecture  
- In-memory data storage (for now)  
- Modular structure for users, places, reviews, amenities  
- Centralized logic via a facade service layer  
- Auto-generated Swagger documentation

## ⚙️ Installation

1. Clone the repository  
git clone https://github.com/JulienPul/holbertonschool-hbnb.git  
cd holbertonschool-hbnb

2. Create a virtual environment  
python3 -m venv venv  
source venv/bin/activate

3. Install dependencies  
pip install -r requirements.txt

## 🚀 Run the Application

python3 run.py

Then open your browser at:  
http://127.0.0.1:5000/api/v1/

## 🔧 Configuration

You can modify environment settings in config.py. The default setup uses development mode:  
config = {  
    'development': DevelopmentConfig,  
    'default': DevelopmentConfig  
}

## 📌 Notes

- The current setup uses an in-memory repository  
- Database integration (SQLAlchemy) will be added in a future version  
- The HBnBFacade class centralizes access to repositories and logic

## 🛠️ Technologies

- Python 3.8+  
- Flask  
- Flask-RESTx  

## 📚 License

This project is part of the Holberton School curriculum and intended for educational purposes only.
