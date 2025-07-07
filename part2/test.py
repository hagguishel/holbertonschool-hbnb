# test_relationships.py

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def main():
    app = create_app()
    with app.app_context():
        # Reset database (attention, efface tout !)
        db.drop_all()
        db.create_all()

        print("==== Création des entités ====")
        user = User(first_name="Alice", last_name="Wonderland", email="alice@mail.com", password="SuperSecret123")
        db.session.add(user)
        db.session.commit()
        print("User:", user.id, user.first_name)

        place = Place(
            title="Château Magique",
            description="Un superbe endroit",
            price=150.0,
            latitude=48.853,
            longitude=2.349,
            owner=user  # Lien via la relation
        )
        db.session.add(place)
        db.session.commit()
        print("Place:", place.id, place.title, "Owner:", place.owner.first_name)

        wifi = Amenity(name="WiFi")
        pool = Amenity(name="Piscine")
        db.session.add_all([wifi, pool])
        db.session.commit()
        print("Amenities:", [a.name for a in [wifi, pool]])

        # Ajout des amenities à la place
        place.amenities.append(wifi)
        place.amenities.append(pool)
        db.session.commit()
        print("Place amenities:", [a.name for a in place.amenities])
        print("WiFi places:", [p.title for p in wifi.places])

        review = Review(
            text="Incroyable expérience !",
            rating=5,
            user=user,
            place=place
        )
        db.session.add(review)
        db.session.commit()
        print("Review:", review.text, "By:", review.user.first_name, "For place:", review.place.title)

        # Vérif des relations
        print("\n==== Vérification des relations ====")
        print("user.places:", [p.title for p in user.places])            # [Château Magique]
        print("user.reviews:", [r.text for r in user.reviews])           # [Incroyable expérience !]
        print("place.owner:", place.owner.first_name)                    # Alice
        print("place.amenities:", [a.name for a in place.amenities])     # [WiFi, Piscine]
        print("place.reviews:", [r.text for r in place.reviews])         # [Incroyable expérience !]
        print("wifi.places:", [p.title for p in wifi.places])            # [Château Magique]
        print("review.user:", review.user.first_name)                    # Alice
        print("review.place:", review.place.title)                       # Château Magique

        print("\n==== TEST OK ====")

if __name__ == "__main__":
    main()
