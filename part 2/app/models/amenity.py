from app.models.BaseModel import BaseModel

class Aminity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if len(name) > 50:
            raise ValueError("Required, maximum length of 50 characters.")

        self.name = name
        self.place_ids = []
