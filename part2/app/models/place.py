from .basemodel import BaseModel
from .user import User
from app import db
from sqlalchemy.orm import validates

amenities_places = db.Table(
    'amenities_places',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
    )
class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', backref='places', lazy='select')
    amenities = db.relationship('Amenity', secondary=amenities_places, backref='places')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')

    @validates('title')
    def validate_title(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not value.strip():
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title must be at most 100 characters")
        return value

    @validates('description')
    def validate_description(self, key, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Description must be a string or None")
        if value and len(value) > 500:
            raise ValueError("Description must be at most 500 characters")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value < 0:
            raise ValueError("Price must be positive.")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Latitude must be a number")
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Longitude must be a number")
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return value


    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        d = super().to_dict()
        d.update({
            'name': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.user_id
        })
        return d

    def to_dict_full(self):
        d = self.to_dict()
        d['amenities'] = [a.to_dict() for a in self.amenities]
        d['reviews'] = [r.to_dict() for r in self.reviews]
        return d