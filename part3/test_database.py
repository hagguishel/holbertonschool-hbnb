import pytest
import pymysql

# Connexion avec les bons identifiants
@pytest.fixture
def db_connection():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root",  # Remplace si besoin
        database="hbnb_db"
    )
    yield conn
    conn.close()


def test_tables_exist(db_connection):
    cursor = db_connection.cursor()
    tables = ["User", "Place", "Review", "Amenity", "Place_Amenity"]
    for table in tables:
        cursor.execute(f"SHOW TABLES LIKE '{table}';")
        assert cursor.fetchone() is not None, f"Table '{table}' should exist"


def test_admin_user_exists(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM User WHERE email='admin@hbnb.io';")
    assert cursor.fetchone() is not None, "Admin user should exist"


def test_place_owner_fk(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SHOW CREATE TABLE Place;")
    result = cursor.fetchone()[1]
    assert "FOREIGN KEY (`owner_id`) REFERENCES `User` (`id`)" in result, "Place.owner_id should reference User(id)"


def test_review_unique_constraint(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SHOW CREATE TABLE Review;")
    result = cursor.fetchone()[1]
    assert "UNIQUE KEY `user_review` (`user_id`,`place_id`)" in result or "UNIQUE (`user_id`,`place_id`)" in result, \
        "Review should have a unique constraint on (user_id, place_id)"


def test_place_amenity_composite_pk(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SHOW CREATE TABLE Place_Amenity;")
    result = cursor.fetchone()[1]
    assert "PRIMARY KEY (`place_id`,`amenity_id`)" in result, "Place_Amenity should have composite primary key (place_id, amenity_id)"
