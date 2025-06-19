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
    review = Review("Très bien", "123", "456")
    assert review.text == "Très bien"
    assert review.user_id == "123"
    assert review.place_id == "456"

def test_review_missing_fields():
    with pytest.raises(ValueError):
        Review("", "123", "456")
    with pytest.raises(ValueError):
        Review("Parfait", "", "456")
    with pytest.raises(ValueError):
        Review("Parfait", "123", "")

# -----------------------
# Tests pour Amenity
# -----------------------
def test_valid_amenity_creation():
    amenity = Amenity("WiFi")
    assert amenity.name == "WiFi"

def test_empty_amenity_name():
    with pytest.raises(ValueError):
        Amenity("")
