from app import create_app, db
from app.models.user import User

app = create_app()
app.app_context().push()

def create_admin():
    admin_email = "admin@test.com"
    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        print("Admin déjà existant.")
        return

    admin = User(
        first_name="Super",
        last_name="Admin",
        email=admin_email,
        is_admin=True
    )
    admin.password = "AdminPass123"
    db.session.add(admin)
    db.session.commit()
    admin = User.query.filter_by(email="admin@test.com").first()
    print("Admin exists:", admin is not None)
    print("Is admin:", getattr(admin, "is_admin", False))
    print("Password hash:", admin.password_hash)
    print("Verify password 'AdminPass123':", admin.verify_password("AdminPass123"))


if __name__ == "__main__":
    create_admin()
