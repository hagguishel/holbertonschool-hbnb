#!/usr/bin/python3
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    # Placeholder method for fetching a place by ID

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute("name", name)

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    def create_place(self, data):
        owner = self.get_user(data["owner_id"])
        if not owner:
            return None

        try:
            place = Place(
                title=data["title"],
                description=data.get("description", ""),
                price=data["price"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                owner=owner,
            )
        except ValueError:
            return None

        for amenity_id in data.get("amenities", []):
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                return None
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = place.owner

        amenities = []
        for amenity in place.amenities:
            amenities.append({"id": amenity.id, "name": amenity.name})

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email,
            },
            "amenities": amenities,
        }

    def get_all_places(self):
        places = self.place_repo.get_all()
        result = []
        for place in places:
            result.append(
                {
                    "id": place.id,
                    "title": place.title,
                    "latitude": place.latitude,
                    "longitude": place.longitude,
                }
            )
        return result

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if "price" in place_data:
            price = place_data["price"]
            if not isinstance(price, (int, float)) or price < 0:
                return None

        if "latitude" in place_data:
            latitude = place_data["latitude"]
            if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
                return None

        if "longitude" in place_data:
            longitude = place_data["longitude"]
            if not isinstance(longitude, (int, float)) or not (
                -180 <= longitude <= 180
            ):
                return None

        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    def create_review(self, review_data):
        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])
        if not user or not place:
            raise ValueError("User or Place not found")

        text = review_data.get("text")
        if not text or not isinstance(text, str):
            raise ValueError("Review text must be a non-empty string")

        rating = review_data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        review = Review(text=text, rating=rating, user=user, place=place)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id,
        }

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        result = []
        for review in reviews:
            result.append(
                {
                    "id": review.id,
                    "text": review.text,
                    "rating": review.rating,
                    "user_id": review.user.id,
                    "place_id": review.place.id,
                }
            )
        return result

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        result = []
        for review in reviews:
            if review.place.id == place_id:
                result.append(
                    {
                        "id": review.id,
                        "text": review.text,
                        "rating": review.rating,
                        "user_id": review.user.id,
                        "place_id": review.place.id,
                    }
                )
        return result

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        text = review_data.get("text")
        if text is not None:
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Text must be a non-empty string")
            review.text = text

        rating = review_data.get("rating")
        if rating is not None:
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = rating

        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
