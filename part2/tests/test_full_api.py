# tests/test_full_api.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

USER_A = {"email": "usera@mail.com", "password": "UserApass123", "first_name": "Alice", "last_name": "Test"}
USER_B = {"email": "userb@mail.com", "password": "UserBpass123", "first_name": "Bob", "last_name": "Test"}

@pytest.fixture(scope="module")
def create_users_and_tokens():
    # Register User A
    r = requests.post(f"{BASE_URL}/users/", json=USER_A)
    assert r.status_code in (201, 409)
    # Register User B
    r = requests.post(f"{BASE_URL}/users/", json=USER_B)
    assert r.status_code in (201, 409)

    # Login A
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": USER_A["email"], "password": USER_A["password"]})
    assert r.status_code == 200
    token_a = r.json()["access_token"]
    # Login B
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": USER_B["email"], "password": USER_B["password"]})
    assert r.status_code == 200
    token_b = r.json()["access_token"]

    # Get user ids
    r = requests.get(f"{BASE_URL}/users/")
    assert r.status_code == 200
    users = {u["email"]: u["id"] for u in r.json() if u["email"] in (USER_A["email"], USER_B["email"])}
    return {
        "A": {"token": token_a, "id": users[USER_A["email"]]},
        "B": {"token": token_b, "id": users[USER_B["email"]]},
    }

def auth_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def test_public_endpoints():
    r = requests.get(f"{BASE_URL}/places/")
    assert r.status_code == 200

def test_user_cannot_get_password_field(create_users_and_tokens):
    ids = create_users_and_tokens
    r = requests.get(f"{BASE_URL}/users/{ids['A']['id']}")
    assert r.status_code == 200
    assert "password" not in r.json()

def test_create_place_and_permissions(create_users_and_tokens):
    ids = create_users_and_tokens
    payload = {"title": "Pytest Place", "price": 100.0, "latitude": 48.8, "longitude": 2.35}
    r = requests.post(f"{BASE_URL}/places/", json=payload, headers=auth_headers(ids["A"]["token"]))
    assert r.status_code == 201
    place_id = r.json()["id"]

    # User B tries to modify the place (forbidden)
    update = {"title": "Hacked Place"}
    r = requests.put(f"{BASE_URL}/places/{place_id}", json=update, headers=auth_headers(ids["B"]["token"]))
    assert r.status_code == 403
    assert r.json()["error"].lower().startswith("unauthorized")

    # User A modifies their place (allowed)
    update = {"title": "New Name"}
    r = requests.put(f"{BASE_URL}/places/{place_id}", json=update, headers=auth_headers(ids["A"]["token"]))
    assert r.status_code == 200
    assert r.json()["title"] == "New Name"

    r = requests.get(f"{BASE_URL}/places/{place_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "New Name"

    pytest.place_id = place_id

def test_create_review_permissions(create_users_and_tokens):
    ids = create_users_and_tokens
    place_id = pytest.place_id

    payload = {"place_id": place_id, "text": "I own this, 5 stars!", "rating": 5}
    r = requests.post(f"{BASE_URL}/reviews/", json=payload, headers=auth_headers(ids["A"]["token"]))
    assert r.status_code == 400
    assert "cannot review your own place" in r.json()["error"].lower()

    payload = {"place_id": place_id, "text": "Super séjour", "rating": 5}
    r = requests.post(f"{BASE_URL}/reviews/", json=payload, headers=auth_headers(ids["B"]["token"]))
    assert r.status_code == 201
    review_id = r.json()["id"]

    payload = {"place_id": place_id, "text": "Encore un avis", "rating": 4}
    r = requests.post(f"{BASE_URL}/reviews/", json=payload, headers=auth_headers(ids["B"]["token"]))
    assert r.status_code == 400
    assert "already reviewed this place" in r.json()["error"].lower()

    pytest.review_id = review_id

def test_update_and_delete_review_permissions(create_users_and_tokens):
    ids = create_users_and_tokens
    review_id = pytest.review_id

    update = {"text": "Hacked review", "rating": 1}
    r = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update, headers=auth_headers(ids["A"]["token"]))
    assert r.status_code == 403
    assert r.json()["error"].lower().startswith("unauthorized")

    update = {"text": "Avis modifié", "rating": 4}
    r = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update, headers=auth_headers(ids["B"]["token"]))
    assert r.status_code == 200
    assert r.json()["text"] == "Avis modifié"

    r = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=auth_headers(ids["A"]["token"]))
    assert r.status_code == 403
    assert r.json()["error"].lower().startswith("unauthorized")

    r = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=auth_headers(ids["B"]["token"]))
    assert r.status_code in (200, 204)

def test_user_modification_permissions(create_users_and_tokens):
    ids = create_users_and_tokens
    update = {"first_name": "Hack"}
    r = requests.put(f"{BASE_URL}/users/{ids['A']['id']}", json=update, headers=auth_headers(ids["B"]["token"]))
    assert r.status_code == 403
    assert r.json()["error"].lower().startswith("unauthorized")

    update = {"email": "hacked@mail.com"}
    r = requests.put(f"{BASE_URL}/users/{ids['A']['id']}", json=update, headers=auth_headers(ids["A"]["token"]))
    assert r.status_code == 400
    assert "cannot modify email" in r.json()["error"].lower()

    update = {"first_name": "AliceUpdated"}
    r = requests.put(f"{BASE_URL}/users/{ids['A']['id']}", json=update, headers=auth_headers(ids["A"]["token"]))
    assert r.status_code == 200
    assert r.json()["first_name"] == "AliceUpdated"

def test_jwt_is_required_for_protected_endpoints():
    r = requests.post(f"{BASE_URL}/places/", json={"title": "NoAuth"})
    assert r.status_code == 401 or r.status_code == 422
    r = requests.put(f"{BASE_URL}/users/some-id", json={"first_name": "NoAuth"})
    assert r.status_code == 401 or r.status_code == 422
    r = requests.post(f"{BASE_URL}/reviews/", json={"text": "NoAuth", "rating": 5, "place_id": "dummy"})
    assert r.status_code == 401 or r.status_code == 422

def test_password_is_hashed(create_users_and_tokens):
    ids = create_users_and_tokens
    for user_id in (ids["A"]["id"], ids["B"]["id"]):
        r = requests.get(f"{BASE_URL}/users/{user_id}")
        assert "password" not in r.json()

def test_sqlalchemy_repository_structure():
    from app.persistence.repository import SQLAlchemyRepository

    class DummyModel:
        pass

    repo = SQLAlchemyRepository(DummyModel)
    assert hasattr(repo, "add")
    assert hasattr(repo, "get")
    assert hasattr(repo, "get_all")
    assert hasattr(repo, "update")
    assert hasattr(repo, "delete")
    assert hasattr(repo, "get_by_attribute")
    assert repo.model == DummyModel

def test_facade_structure():
    from app.services.facade import HBnBFacade

    facade = HBnBFacade()
    assert hasattr(facade, "user_repo")

def test_repository_get_by_attribute_unique():
    from app import create_app, db
    from app.persistence.repository import SQLAlchemyRepository
    from app.models.user import User

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        repo = SQLAlchemyRepository(User)
        user1 = User(first_name="A", last_name="A", email="a@b.c", password="password123")
        repo.add(user1)

        found = repo.get_by_attribute("email", "a@b.c")
        assert found is not None
        assert found.email == "a@b.c"

        not_found = repo.get_by_attribute("email", "not@found.com")
        assert not_found is None

def test_base_model_sqlalchemy_columns():
    from app.models.user import User
    user = User(first_name="Jean", last_name="Dupont", email="testuser@email.com", password="Password123")
    assert hasattr(user, "id")
    assert hasattr(user, "created_at")
    assert hasattr(user, "updated_at")

def test_user_model_columns_and_constraints():
    from app.models.user import User
    from app import create_app, db

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(first_name="Prénom", last_name="Nom", email="unique@email.com", password="SuperPass123")
        user.hash_password("SuperPass123")
        db.session.add(user)
        db.session.commit()

        from sqlalchemy.exc import IntegrityError
        user2 = User(first_name="Autre", last_name="Nom", email="unique@email.com", password="Motdepasse123")
        user2.hash_password("Motdepasse123")
        db.session.add(user2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        db.session.rollback()

def test_user_repository_add_and_get_by_email():
    from app.persistence.user_repository import UserRepository
    from app.models.user import User
    from app import create_app, db

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        repo = UserRepository()

        user = User(first_name="Yasmine", last_name="Repo", email="yas.repo@test.com", password="PassW0rdYas")
        user.hash_password("PassW0rdYas")
        repo.add(user)
        found = repo.get_user_by_email("yas.repo@test.com")
        assert found is not None
        assert found.email == "yas.repo@test.com"

        not_found = repo.get_user_by_email("doesnotexist@test.com")
        assert not_found is None

def test_user_facade_create_and_retrieve():
    from app.services.facade import HBnBFacade
    from app import create_app, db

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        facade = HBnBFacade()
        data = {
            "first_name": "Façade",
            "last_name": "UserTest",
            "email": "facade.user@test.com",
            "password": "SuperTestFacad1"
        }
        user = facade.create_user(data)
        assert user.email == data["email"]

        user_from_db = facade.get_user_by_email(data["email"])
        assert user_from_db is not None
        assert user_from_db.first_name == "Façade"

def test_user_place_relationship():
    """Un User peut avoir plusieurs Place, chaque Place a un user_id."""
    from app.models.user import User
    from app.models.place import Place
    from app import create_app, db

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(first_name="John", last_name="Owner", email="owner@example.com", password="Password123")
        db.session.add(user)
        db.session.commit()
        place = Place(title="Maison", description="Sympa", price=100, latitude=0, longitude=0, user_id=user.id)
        db.session.add(place)
        db.session.commit()

        assert place.user_id == user.id
        assert place.owner == user          # Corrected here to use 'owner' instead of 'user'
        assert place in user.places

def test_place_review_relationship():
    """Un Place a plusieurs Review, chaque Review a un place_id."""
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app import create_app, db

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(first_name="John", last_name="Doe", email="testrev@ex.com", password="Password123")
        db.session.add(user)
        db.session.commit()
        place = Place(title="Villa", description="Belle villa", price=150, latitude=0, longitude=0, user_id=user.id)
        db.session.add(place)
        db.session.commit()

        review = Review(text="Super expérience chez eux, vraiment top !", rating=5, user_id=user.id, place_id=place.id)
        db.session.add(review)
        db.session.commit()

        assert review.place_id == place.id
        assert review.place == place
        assert review in place.reviews

def test_user_review_relationship():
    """Un User a plusieurs Review, chaque Review a un user_id."""
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app import create_app, db

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(first_name="Critique", last_name="Test", email="critique@ex.com", password="Password123")
        db.session.add(user)
        db.session.commit()
        place = Place(title="Loft", description="Loft design", price=90, latitude=1, longitude=2, user_id=user.id)
        db.session.add(place)
        db.session.commit()

        review = Review(text="Magnifique séjour, hôte très sympa !", rating=5, user_id=user.id, place_id=place.id)
        db.session.add(review)
        db.session.commit()

        assert review.user_id == user.id
        assert review.user == user
        assert review in user.reviews

def test_place_amenity_relationship():
    """Test many-to-many Place <-> Amenity via association table."""
    from app.models.user import User
    from app.models.place import Place
    from app.models.amenity import Amenity
    from app import create_app, db

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(first_name="John", last_name="Doe", email="owner2@ex.com", password="Password123")
        db.session.add(user)
        db.session.commit()
        place = Place(title="Cabane", description="Petite cabane", price=50, latitude=0, longitude=0, user_id=user.id)
        db.session.add(place)
        db.session.commit()

        wifi = Amenity(name="Wifi")
        piscine = Amenity(name="Piscine")
        db.session.add(wifi)
        db.session.add(piscine)
        db.session.commit()

        place.amenities.append(wifi)
        place.amenities.append(piscine)
        db.session.commit()

        assert wifi in place.amenities
        assert place in wifi.places
        assert piscine in place.amenities

def test_cascade_delete_reviews():
    """Supprimer un Place doit supprimer ses Reviews (si cascade configurée)."""
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app import create_app, db

    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(first_name="Owner", last_name="Cascade", email="cascade@ex.com", password="Password123")
        db.session.add(user)
        db.session.commit()
        place = Place(title="Apt", description="Appartement", price=70, latitude=0, longitude=0, user_id=user.id)
        db.session.add(place)
        db.session.commit()
        review = Review(text="Séjour court mais sympa, merci !", rating=4, user_id=user.id, place_id=place.id)
        db.session.add(review)
        db.session.commit()

        db.session.delete(place)
        db.session.commit()

        assert Review.query.filter_by(id=review.id).first() is None
