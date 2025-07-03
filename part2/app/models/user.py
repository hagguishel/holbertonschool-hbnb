from .basemodel import BaseModel
from app import bcrypt, db
import re
from sqlalchemy.orm import validates
class User(BaseModel):
    __tablename__= 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError(f"{key.replace('_', ' ').capitalize()} must be a string")
        if len(value) > 50:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be at most 50 characters")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        return value

    @validates('password')
    def validate_password(self, key, value):
        if value.startswith('$2b$'):
            return value
        if not isinstance(value, str):
            raise TypeError("Password must be a string")
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return bcrypt.generate_password_hash(value).decode('utf-8')

    @validates('is_admin')
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        return value

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        """Add an amenity to the place."""
        self.places.append(place)

    def add_review(self, review):
        """Add an amenity to the place."""
        self.reviews.append(review)

    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)

    def to_dict(self):
        d = super().to_dict()
        d.update ({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return d
