from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # USER
    def create_user(self, user_data):
        user_data['password_hash'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data, is_admin=False):
        user = self.user_repo.get(user_id)
        if not user:
            raise KeyError('User not found')

        if not is_admin:
            user_data.pop('email', None)
            user_data.pop('password', None)
        else:
            if 'password' in user_data:
                hashed = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
                user_data['password_hash'] = hashed
                user_data.pop('password', None)

        self.user_repo.update(user_id, user_data)
        return user

    # AMENITY
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    # PLACE
    def create_place(self, place_data):
        user = self.user_repo.get_by_attribute('id', place_data['owner_id'])
        if not user:
            raise KeyError('Invalid input data')
        del place_data['owner_id']
        place_data['owner'] = user
        amenities = place_data.pop('amenities', None)
        if amenities:
            for a in amenities:
                amenity = self.get_amenity(a['id'])
                if not amenity:
                    raise KeyError('Invalid input data')
        place = Place(**place_data)
        self.place_repo.add(place)
        user.add_place(place)
        if amenities:
            for amenity in amenities:
                place.add_amenity(amenity)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)

    # REVIEWS
    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise KeyError('Invalid input data')
        del review_data['user_id']
        review_data['user'] = user

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise KeyError('Invalid input data')
        del review_data['place_id']
        review_data['place'] = place

        review = Review(**review_data)
        self.review_repo.add(review)
        user.add_review(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)

        if not review:
            raise KeyError('Review not found')

        user = review.user
        place = review.place

        session = self.review_repo.session

        with session.no_autoflush:
            if user and review in user.reviews:
                user.reviews.remove(review)
            if place and review in place.reviews:
                place.reviews.remove(review)

        self.review_repo.delete(review_id)

        session.commit()
