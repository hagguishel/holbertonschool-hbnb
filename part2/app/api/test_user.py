import sys
import os
import pytest

# Ajouter le chemin du projet pour résoudre les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# -----------------------
# Fixtures
# -----------------------


@pytest.fixture(autouse=True)
def reset_user_emails():
    User.used_emails = set()


@pytest.fixture
def user():
    return User("Test", "User", "test@example.com")


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# -----------------------
# Tests API /api/v1/users/
# -----------------------


def test_get_users_empty(client):
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json == []


def test_create_user_success(client):
    data = {"first_name": "Julien", "last_name": "Pulon", "email": "julien@api.com"}
    response = client.post("/api/v1/users/", json=data)
    assert response.status_code == 201
    assert response.json["email"] == "julien@api.com"


def test_update_user_success(client):
    # Crée un utilisateur d'abord (POST)
    res = client.post(
        "/api/v1/users/",
        json={
            "first_name": "Julien",
            "last_name": "Pulon",
            "email": "julien@update.com",
        },
    )
    assert res.status_code == 201
    user_id = res.json["id"]

    # Update de l'utilisateur (PUT)
    update_data = {
        "first_name": "Jules",
        "last_name": "Pulon",
        "email": "julien@update.com",
    }
    res_put = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert res_put.status_code == 200
    assert res_put.json["first_name"] == "Jules"


def test_create_user_invalid_email(client):
    res = client.post(
        "/api/v1/users/",
        json={"first_name": "Test", "last_name": "User", "email": "invalid-email"},
    )
    assert res.status_code == 400

def test_delete_review_success(client):
    # Créer un user + un place
    user = client.post("/api/v1/users/", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "delete@review.com"
    }).json
    place = client.post("/api/v1/places/", json={
        "title": "Test Place",
        "description": "test",
        "price": 100.0,
        "latitude": 45.0,
        "longitude": 3.0,
        "owner_id": user["id"]
    }).json
    # Créer une review
    review = client.post("/api/v1/reviews/", json={
        "text": "Super endroit",
        "rating": 5,
        "user_id": user["id"],
        "place_id": place["id"]
    }).json

    # Supprimer la review
    res = client.delete(f"/api/v1/reviews/{review['id']}")
    assert res.status_code == 200

# -----------------------
# Tests API /api/v1/amenities/
# -----------------------

def test_get_amenities_empty(client):
    response = client.get("/api/v1/amenities/")
    assert response.status_code == 200
    assert response.json == []

def test_create_amenity_success(client):
    data = {"name": "Jacuzzi"}
    response = client.post("/api/v1/amenities/", json=data)
    assert response.status_code == 201
    assert response.json["name"] == "Jacuzzi"

def test_create_amenity_empty_name(client):
    response = client.post("/api/v1/amenities/", json={"name": ""})
    assert response.status_code == 400

def test_get_amenity_by_id(client):
    # Crée d'abord une amenity
    amenity = client.post("/api/v1/amenities/", json={"name": "WiFi"}).json
    amenity_id = amenity["id"]

    # Récupère l'amenity via GET
    res = client.get(f"/api/v1/amenities/{amenity_id}")
    assert res.status_code == 200
    assert res.json["name"] == "WiFi"

def test_get_amenity_not_found(client):
    response = client.get("/api/v1/amenities/invalid-id")
    assert response.status_code == 404

# -----------------------
# Tests User (modèle)
# -----------------------


def test_valid_user_creation():
    user = User("Julien", "Pulon", "julien@example.com")
    assert user.first_name == "Julien"
    assert user.last_name == "Pulon"
    assert user.email == "julien@example.com"


def test_user_creation_with_admin_flag():
    admin = User("Admin", "User", "admin@example.com", is_admin=True)
    assert admin.is_admin is True
    assert admin.is_admin_user is True


def test_empty_user_fields():
    with pytest.raises(ValueError):
        User("", "Pulon", "julien@example.com")
    with pytest.raises(ValueError):
        User("Julien", "", "julien@example.com")
    with pytest.raises(ValueError):
        User("Julien", "Pulon", "")


def test_user_duplicate_email():
    User("Julien", "Pulon", "julien@example.com")
    with pytest.raises(ValueError):
        User("Jean", "Dupont", "julien@example.com")


def test_invalid_email():
    with pytest.raises(ValueError):
        User("Julien", "Pulon", "invalid-email")


def test_user_to_dict():
    user = User("Julien", "Pulon", "julien@example.com")
    d = user.to_dict()
    assert d["first_name"] == "Julien"
    assert d["email"] == "julien@example.com"
    assert "id" in d


# -----------------------
# Tests Place
# -----------------------


def test_valid_place_creation(user):
    place = Place(
        "Nice house", "Nice house in front of the beach", 100.0, 45.0, 3.0, user
    )
    assert place.title == "Nice house"
    assert place.price == 100.0


def test_place_title_required(user):
    with pytest.raises(ValueError):
        Place("", "desc", 100.0, 45.0, 3.0, user)


def test_place_title_too_long(user):
    with pytest.raises(ValueError):
        Place("A" * 101, "desc", 100.0, 45.0, 3.0, user)


def test_place_invalid_price(user):
    with pytest.raises(ValueError):
        Place("Nice house", "Beach view", -10.0, 45.0, 3.0, user)


def test_place_invalid_lat_lon(user):
    with pytest.raises(ValueError):
        Place("Nice house", "Desc", 50.0, -100.0, 3.0, user)
    with pytest.raises(ValueError):
        Place("Nice house", "Desc", 50.0, 45.0, -200.0, user)


def test_place_invalid_owner():
    with pytest.raises(ValueError):
        Place("Title", "desc", 100.0, 45.0, 3.0, "not_a_user")


def test_place_invalid_types(user):
    with pytest.raises(ValueError):
        Place("Test", "desc", "one hundred", 45.0, 3.0, user)
    with pytest.raises(ValueError):
        Place("Test", "desc", 100.0, "north", 3.0, user)


def test_place_to_dict(user):
    place = Place("Cabane", "Vue mer", 99.0, 45.0, 3.0, user)
    d = place.to_dict()
    assert d["title"] == "Cabane"
    assert "created_at" in d


def test_place_add_review_and_amenity(user):
    place = Place("Maison", "desc", 100.0, 45.0, 3.0, user)
    review = Review("Top", 5, place, user)
    amenity = Amenity("WiFi")
    place.add_review(review)
    place.add_amenity(amenity)
    assert review in place.reviews
    assert amenity in place.amenities


# -----------------------
# Tests Review
# -----------------------


def test_valid_review_creation(user):
    place = Place("Nice view", "balcony", 120.0, 48.0, 2.0, user)
    review = Review("Très bien", 4, place, user)
    assert review.text == "Très bien"
    assert review.user == user
    assert review.place == place


def test_review_missing_fields(user):
    place = Place("Spot", "desc", 50.0, 45.0, 3.0, user)
    with pytest.raises(ValueError):
        Review("", 3, user, place)
    with pytest.raises(TypeError):
        Review("Parfait", 4, user, "not_a_place")
    with pytest.raises(TypeError):
        Review("Parfait", 4, None, place)


def test_review_invalid_rating(user):
    place = Place("Bad rating", "test", 100.0, 45.0, 3.0, user)
    with pytest.raises(ValueError):
        Review("Trop bas", 0, place, user)
    with pytest.raises(ValueError):
        Review("Trop haut", 6, place, user)


def test_review_invalid_types(user):
    place = Place("Test", "test", 50.0, 45.0, 3.0, user)
    with pytest.raises(ValueError):
        Review(12345, 4, place, user)
    with pytest.raises(ValueError):
        Review("Bien", "quatre", place, user)


def test_review_to_dict(user):
    place = Place("Test", "desc", 100.0, 45.0, 3.0, user)
    review = Review("Top", 5, place, user)
    d = review.to_dict()
    assert "text" in d and d["text"] == "Top"


# -----------------------
# Tests Amenity
# -----------------------


def test_valid_amenity_creation():
    amenity = Amenity("WiFi")
    assert amenity.name == "WiFi"


def test_empty_amenity_name():
    with pytest.raises(ValueError):
        Amenity("")
