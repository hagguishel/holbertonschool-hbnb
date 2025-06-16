from app.models.BaseModel import BaseModel
from app.models.user import User
from app.models.review import Review

class place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        
        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError("title is required and must be a string with max 100 characters.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("price must be a positive number.")
        if not isinstance(latitude, (int, float)) or not (-90.0 <= latitude <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0.")
        if not isinstance(longitude, (int, float)) or not (-180.0 <= longitude <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0.")
        if not isinstance(owner, User):
            raise ValueError("owner must be a valid User instance.")
        

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner
        self.amenities = []
        self.reviews = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
