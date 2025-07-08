DROP DATABASE IF EXISTS hbnb_db;
CREATE DATABASE hbnb_db;
USE hbnb_db;

CREATE TABLE IF NOT EXISTS User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255)NOT NULL,
    last_name VARCHAR(255)NOT NULL,
    email VARCHAR(255)NOT NULL UNIQUE,
    password VARCHAR(255)NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255)NOT NULL,
    description TEXT,
    price DECIMAL(10, 2)NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36)NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK(rating BETWEEN 1 AND 5),
    user_id CHAR(36)NOT NULL,
    place_id CHAR(36)NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    CONSTRAINT user_review UNIQUE (user_id, place_id)
);

CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255)NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id CHAR(36)NOT NULL,
    amenity_id CHAR(36)NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE
);

INSERT INTO User (id, first_name, last_name, email, password, is_admin) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$zq9uFNmKH/0K6gI0Qhce6u/6ydXDGc0Rra8VjDoA3Uuk5IWUZDPmC', TRUE);

INSERT INTO Amenity (id, name) VALUES
('f3aef1eb-4ff7-40f6-92e6-136ebee15632', 'WiFi'),
('b8760c1e-07b5-4d4a-89de-23c51c98b812', 'Swimming Pool'),
('dc2a5eb9-6b33-4967-81a2-62b69754bc81', 'Air Conditioning');
