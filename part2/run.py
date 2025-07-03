from app import create_app, db

from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
