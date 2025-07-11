DELETE FROM Place_Amenity;
DELETE FROM Review;
DELETE FROM Place;
DELETE FROM Amenity;
DELETE FROM User;

-- Insertion d’un utilisateur admin
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('user-1', 'Julien', 'Pulon', 'julien.pulon@example.com', 'admin123', TRUE);

-- Insertion d’un lieu (Place)
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES ('place-1', 'Appartement lumineux', 'Appartement moderne avec balcon', 95.00, 48.853, 2.349, 'user-1');

-- Insertion de commodités (Amenity)
INSERT INTO Amenity (id, name)
VALUES 
  ('amenity-1', 'WiFi'),
  ('amenity-2', 'Machine à café'),
  ('amenity-3', 'Jacuzzi');

-- Association entre un lieu et ses commodités (many-to-many)
INSERT INTO Place_Amenity (place_id, amenity_id)
VALUES 
  ('place-1', 'amenity-1'),
  ('place-1', 'amenity-3');

-- Insertion d’un avis utilisateur
INSERT INTO Review (id, text, rating, user_id, place_id)
VALUES ('review-1', 'Appartement très propre et bien situé, je recommande !', 5, 'user-1', 'place-1');
