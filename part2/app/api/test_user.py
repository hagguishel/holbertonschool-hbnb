import pytest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# ✅ Réinitialise les emails utilisés entre chaque test
@pytest.fixture(autouse=True)
def reset_user_emails():
    User.used_emails = set()

# -----------------------
# Tests pour User
# -----------------------
def test_valid_user_creation():
    user = User("Julien", "Pulon", "julien@example.com")
    assert user.first_name == "Julien"
    assert user.last_name == "Pulon"
    assert user.email == "julien@example.com"

def test_empty_user_fields():
    with pytest.raises(ValueError):
        User("", "Pulon", "julien@example.com")
    with pytest.raises(ValueError):
        User("Julien", "", "julien@example.com")
    with pytest.raises(ValueError):
        User("Julien", "Pulon", "")

def test_invalid_email():
    with pytest.raises(ValueError):
        User("Julien", "Pulon", "invalid-email")

# -----------------------
# Tests pour Place
# -----------------------
def test_valid_place_creation():
    user = User("Julien", "Pulon", "julien1@example.com")
    place = Place("Nice house", "Nice house in front of the beach", 100.0, 45.0, 3.0, user)
    assert place.title == "Nice house"
    assert place.price == 100.0

def test_place_invalid_price():
    user = User("Julien", "Pulon", "julien2@example.com")
    with pytest.raises(ValueError):
        Place("Nice house", "Beach view", -10.0, 45.0, 3.0, user)

def test_place_invalid_lat_lon():
    user = User("Julien", "Pulon", "julien3@example.com")
    with pytest.raises(ValueError):
        Place("Nice house", "Desc", 50.0, -100.0, 3.0, user)  # lat < -90
    with pytest.raises(ValueError):
        Place("Nice house", "Desc", 50.0, 45.0, -200.0, user)  # lon < -180

def test_place_empty_title():
    user = User("Julien", "Pulon", "julien4@example.com")
    with pytest.raises(ValueError):
        Place("", "Nice", 100.0, 45.0, 3.0, user)

# -----------------------
# Tests pour Review
# -----------------------
def test_valid_review_creation():
    user = User("Julien", "Pulon", "reviewer@example.com")
    place = Place("Nice view", "balcony", 120.0, 48.0, 2.0, user)
    review = Review("Très bien", 4, place, user)
    assert review.text == "Très bien"
    assert review.user == user
    assert review.place == place


def test_review_missing_fields():
    user = User("Julien", "Pulon", "missing@example.com")
    place = Place("Spot", "desc", 50.0, 45.0, 3.0, user)

    with pytest.raises(ValueError):
        Review("", 3, user, place)

    with pytest.raises(TypeError):
        Review("Parfait", 4, user, "not_a_place")

    with pytest.raises(TypeError):
        Review("Parfait", 4, None, place)

# -----------------------
# Tests pour Amenity
# -----------------------
def test_valid_amenity_creation():
    amenity = Amenity("WiFi")
    assert amenity.name == "WiFi"

def test_empty_amenity_name():
    with pytest.raises(ValueError):
        Amenity("")
