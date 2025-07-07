# test.py

import config
from app import create_app, db
from app.models.user import User
import requests

BASE = "http://127.0.0.1:5000/api/v1"  # Définition globale de BASE

def print_result(test_name, result):
    if result:
        print(f"✅ {test_name} : OK")
    else:
        print(f"❌ {test_name} : ECHEC")

def test_factory_config():
    app = create_app()
    with app.app_context():
        print("Test 1 : Config par défaut (DevelopmentConfig)")
        default_ok = app.config["DEBUG"] is True
        print_result("DEBUG = True (par défaut)", default_ok)
        has_custom = hasattr(config.DevelopmentConfig, "DEBUG")
        print_result("Attribut DEBUG existe dans config.DevelopmentConfig", has_custom)

    app2 = create_app(config.ProductionConfig)
    with app2.app_context():
        print("\nTest 2 : Config ProductionConfig")
        prod_ok = app2.config["DEBUG"] is False
        print_result("DEBUG = False (en Production)", prod_ok)
        prod_env = app2.config["ENV"] == "production"
        print_result("ENV = 'production'", prod_env)

    if hasattr(config, "TestingConfig"):
        app3 = create_app(config.TestingConfig)
        with app3.app_context():
            print("\nTest 3 : Config TestingConfig")
            testing_ok = app3.config["TESTING"] is True
            print_result("TESTING = True (en Testing)", testing_ok)

    print("\n==== FIN DES TESTS FACTORY CONFIG ====")

def test_user_password():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("==== Test création utilisateur avec password hashé ====")
        user = User(
            first_name="Bob",
            last_name="Hashed",
            email="bob.hash@example.com"
        )
        user.password = "PasswordUltraSecure123"
        db.session.add(user)
        db.session.commit()

        raw_ok = user.password_hash != "PasswordUltraSecure123" and user.password_hash.startswith("$2b$")
        print_result("Mot de passe hashé et non stocké en clair", raw_ok)

        verify_ok = user.verify_password("PasswordUltraSecure123") is True and user.verify_password("badpass") is False
        print_result("verify_password() : vrai si bon password, faux sinon", verify_ok)

        not_in_dict = "password" not in user.to_dict() and "password_hash" not in user.to_dict()
        print_result("Mot de passe non exposé dans to_dict", not_in_dict)

        print("==== TESTS HASH PASSWORD TERMINÉS ====\n")

def test_jwt_login_and_protected():
    print("==== Test JWT Login et accès endpoint protégé ====")

    r = requests.post(f"{BASE}/users/", json={
        "first_name": "Bob",
        "last_name": "JWTUser",
        "email": "bob.jwt@example.com",
        "password": "SuperSecret123"
    })
    if r.status_code in (200, 201, 409):
        print("✅ Utilisateur prêt (créé ou déjà existant)")
    else:
        print(f"⚠️ Création user: {r.status_code} {r.text}")

    r = requests.post(f"{BASE}/auth/login", json={
        "email": "bob.jwt@example.com",
        "password": "SuperSecret123"
    })
    assert r.status_code == 200, f"Erreur login : {r.status_code} {r.text}"
    data = r.json()
    token = data.get("access_token")
    assert token, "❌ Token non reçu"
    print("✅ Token reçu :", token[:25], "...")

    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE}/auth/protected", headers=headers)
    assert r.status_code == 200, f"Erreur accès protégé: {r.status_code} {r.text}"
    print("✅ Accès endpoint protégé :", r.json())

    r = requests.get(f"{BASE}/auth/protected")
    assert r.status_code == 401, "❌ Endpoint protégé accessible sans token!"
    print("✅ Refus accès sans token : OK")

    print("==== TESTS JWT TERMINÉS ====")

# ----------- Partie Auth Endpoints sécurisés -----------

def get_user_id_by_email(email):
    r = requests.get(f"{BASE}/users/")
    r.raise_for_status()
    for user in r.json():
        if user["email"] == email:
            return user["id"]
    raise Exception("User not found: " + email)

def get_token(email, password):
    r = requests.post(f"{BASE}/auth/login", json={
        "email": email, "password": password
    })
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]

def create_user(email, first, last, password, is_admin=False):
    data = {
        "email": email,
        "first_name": first,
        "last_name": last,
        "password": password
    }
    # Note: si l’API ne permet pas d’indiquer is_admin à la création, gérer la création admin à part
    r = requests.post(f"{BASE}/users/", json=data)
    assert r.status_code in (201, 409), f"User create failed: {r.text}"

def test_authenticated_endpoints():
    print("==== PREPARATION USERS & TOKENS ====")
    create_user("usera@mail.com", "Alice", "Wonderland", "PasswordA123")
    create_user("userb@mail.com", "Bob", "Builder", "PasswordB123")

    tokenA = get_token("usera@mail.com", "PasswordA123")
    tokenB = get_token("userb@mail.com", "PasswordB123")
    headersA = {"Authorization": f"Bearer {tokenA}"}
    headersB = {"Authorization": f"Bearer {tokenB}"}

    userA_id = get_user_id_by_email("usera@mail.com")
    userB_id = get_user_id_by_email("userb@mail.com")

    print("==== TEST PLACES ====")
    placeA = {
        "title": "Chez Alice",
        "description": "Un super endroit",
        "price": 120,
        "latitude": 42.0,
        "longitude": 2.0
    }
    r = requests.post(f"{BASE}/places/", json=placeA, headers=headersA)
    assert r.status_code == 201, f"Create place failed: {r.text}"
    placeA_id = r.json()["id"]
    print("✅ UserA peut créer sa place")

    r = requests.put(f"{BASE}/places/{placeA_id}", json={"title": "EditBob"}, headers=headersB)
    assert r.status_code == 403 and "Unauthorized" in r.text, "UserB modif la place d'Alice: ECHEC"
    print("✅ UserB ne peut PAS modifier la place d'Alice")

    r = requests.put(f"{BASE}/places/{placeA_id}", json={"title": "EditAlice"}, headers=headersA)
    assert r.status_code == 200, "UserA ne peut pas modifier sa propre place"
    print("✅ UserA peut modifier sa propre place")

    print("==== TEST REVIEWS ====")
    r = requests.post(f"{BASE}/reviews/", json={"place_id": placeA_id, "text": "Je suis chez moi", "rating": 5}, headers=headersA)
    assert r.status_code == 400 and "own place" in r.text, "UserA review sa propre place: ECHEC"
    print("✅ UserA ne peut PAS reviewer sa propre place")

    r = requests.post(f"{BASE}/reviews/", json={"place_id": placeA_id, "text": "Magnifique", "rating": 5}, headers=headersB)
    assert r.status_code == 201, "UserB ne peut pas reviewer la place d'Alice"
    review_id = r.json()["id"]
    print("✅ UserB peut reviewer la place d'Alice")

    r = requests.post(f"{BASE}/reviews/", json={"place_id": placeA_id, "text": "Encore!", "rating": 4}, headers=headersB)
    assert r.status_code == 400 and "already reviewed" in r.text, "UserB peut reviewer deux fois: ECHEC"
    print("✅ UserB ne peut PAS reviewer deux fois la même place")

    r = requests.put(f"{BASE}/reviews/{review_id}", json={"text": "J'édite la review de Bob"}, headers=headersA)
    assert r.status_code == 403, "UserA édite la review de Bob: ECHEC"
    print("✅ UserA ne peut PAS éditer la review de Bob")

    r = requests.put(f"{BASE}/reviews/{review_id}", json={"text": "Edit by Bob", "rating": 4}, headers=headersB)
    assert r.status_code == 200, "UserB ne peut pas éditer sa propre review"
    print("✅ UserB peut éditer sa propre review")

    r = requests.delete(f"{BASE}/reviews/{review_id}", headers=headersA)
    assert r.status_code == 403, "UserA delete review de Bob: ECHEC"
    print("✅ UserA ne peut PAS supprimer la review de Bob")

    r = requests.delete(f"{BASE}/reviews/{review_id}", headers=headersB)
    assert r.status_code == 200, "UserB ne peut pas supprimer sa propre review"
    print("✅ UserB peut supprimer sa propre review")

    print("==== TEST MODIF USER ====")
    r = requests.put(f"{BASE}/users/{userA_id}", json={"email": "hacker@mail.com"}, headers=headersA)
    assert r.status_code == 400 and "cannot modify email" in r.text, "UserA change son email: ECHEC"
    print("✅ UserA ne peut PAS changer son email")

    r = requests.put(f"{BASE}/users/{userA_id}", json={"first_name": "Hacker"}, headers=headersB)
    assert r.status_code == 403 and "Unauthorized" in r.text, "UserB modif UserA: ECHEC"
    print("✅ UserB ne peut PAS modifier un autre user")

    print("==== TEST PUBLIC ENDPOINTS ====")
    r = requests.get(f"{BASE}/places/")
    assert r.status_code == 200, "GET /places/ non accessible publiquement"
    print("✅ GET /places/ accessible publiquement")

    r = requests.get(f"{BASE}/places/{placeA_id}")
    assert r.status_code == 200, "GET /places/<id> non accessible publiquement"
    print("✅ GET /places/<id> accessible publiquement")

    print("\n==== ALL TESTS PASSED, TASK VALIDATED ====")

def main():
    print("==== PREPARATION ADMIN ====")
    admin_email = "admin@mail.com"
    user_email = "userc@mail.com"

    create_user(admin_email, "Super", "Admin", "Admin12345", is_admin=True)
    create_user(user_email, "Charlie", "Normal", "UserC12345", is_admin=False)

    admin_token = get_token(admin_email, "Admin12345")
    user_token = get_token(user_email, "UserC12345")
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    headers_user = {"Authorization": f"Bearer {user_token}"}

    print("==== TEST ADMIN CREATE USER ====")
    r = requests.post(f"{BASE}/users/", json={
        "email": "nouvelutilisateur@mail.com",
        "first_name": "Nouveau",
        "last_name": "Utilisateur",
        "password": "SuperPass2025"
    }, headers=headers_admin)
    print_result("Admin peut créer un nouvel utilisateur", r.status_code == 201)

    user_id = requests.get(f"{BASE}/users/", headers=headers_admin).json()[-1]["id"]
    new_email = "utilisateur_modifie@mail.com"
    r = requests.put(f"{BASE}/users/{user_id}", json={
        "first_name": "Modifié",
        "last_name": "Utilisateur",
        "email": new_email,
        "password": "MotDePasseModif2025"
    }, headers=headers_admin)
    print_result("Admin peut modifier toutes les infos d'un user", r.status_code == 200)

    r = requests.put(f"{BASE}/users/{user_id}", json={
        "email": admin_email
    }, headers=headers_admin)
    print_result("Admin reçoit une erreur si email déjà utilisé", r.status_code == 400 and "already in use" in r.text)

    print("==== TEST ADMIN AMENITY ====")
    r = requests.post(f"{BASE}/amenities/", json={"name": "Sauna"}, headers=headers_admin)
    print_result("Admin peut ajouter une amenity", r.status_code == 201)
    amenity_id = r.json()["id"]

    r = requests.put(f"{BASE}/amenities/{amenity_id}", json={"name": "Super Sauna"}, headers=headers_admin)
    print_result("Admin peut modifier une amenity", r.status_code == 200)

    print("==== TEST ADMIN BYPASS OWNERSHIP ====")
    place_data = {
        "title": "Chez Charlie",
        "description": "Endroit simple",
        "price": 99,
        "latitude": 0.0,
        "longitude": 0.0
    }
    r = requests.post(f"{BASE}/places/", json=place_data, headers=headers_user)
    assert r.status_code == 201, "Erreur création place par user normal"
    place_id = r.json()["id"]

    # IMPORTANT : ici on utilise headers_admin pour que l’admin puisse créer la review
    r = requests.post(f"{BASE}/reviews/", json={
        "place_id": place_id,
        "text": "Cool",
        "rating": 5
    }, headers=headers_admin)
    assert r.status_code == 201, "Erreur création review"
    review_id = r.json()["id"]

    r = requests.put(f"{BASE}/places/{place_id}", json={"title": "Modif Admin"}, headers=headers_admin)
    print_result("Admin peut modifier une place qu'il ne possède pas", r.status_code == 200)

    r = requests.put(f"{BASE}/reviews/{review_id}", json={"text": "Admin edit", "rating": 3}, headers=headers_admin)
    print_result("Admin peut éditer une review qu'il ne possède pas", r.status_code == 200)

    r = requests.delete(f"{BASE}/reviews/{review_id}", headers=headers_admin)
    print_result("Admin peut supprimer une review qu'il ne possède pas", r.status_code == 200)

    print("\n==== ALL ADMIN TESTS PASSED IF ALL GREEN ====")

if __name__ == "__main__":
    test_factory_config()
    test_user_password()
    test_jwt_login_and_protected()
    test_authenticated_endpoints()
    main()
