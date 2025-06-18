#!/usr/bin/python3
from app.models.basemodel import BaseModel
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("text is required and must be a non-empty string")
        self.__text = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("rating must be an integer between 1 and 5")
        self.__rating = value

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        from app.models.place import Place

        if not isinstance(value, Place):
            raise TypeError("Must be validated to ensure the place exists")
        self.__place = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("Must be validated to ensure the user exists.")
        self.__user = value

    def to_dict(self):
        data = {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place.id,
            "user_id": self.user.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        return data
