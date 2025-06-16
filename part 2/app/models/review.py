from app.models.BaseModel import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not isinstance(text, str) or not text.strip():
            raise ValueError("text is required and must be a non-empty string")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be an integer between 1 and 5")

        if not isinstance(place, Place):
            raise TypeError("Must be validated to ensure the place exists")

        if not isinstance(user, User):
            raise TypeError("Must be validated to ensure the user exists.")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

