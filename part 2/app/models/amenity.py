from app.models.BaseModel import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if len(value) > 50:
            raise ValueError("Required, maximum length of 50 characters.")

        self.__name = value

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

        return data
