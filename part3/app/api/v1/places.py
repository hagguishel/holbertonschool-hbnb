from flask_restx import Namespace, Resource, fields
from app.services import facade
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.Nested(user_model, readonly=True, description='Owner details'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')

    def post(self):
        """Register a new place"""
        user_id = get_jwt_identity()
        print("DEBUG - user_id from JWT", user_id)

        if isinstance(user_id, dict):
            user_id = user_id.get('id') or user_id.get('sub')

        place_data = api.payload
        if 'owner_id' in place_data:
            return{'error': 'You cannot modify the owner_id'}, 400

        place_data.pop("owner", None)

        if "name" in place_data:
            place_data['title'] = place_data.pop("name")

        if not user_id:
            return {'error': 'Invalid user ID'}, 400

        place_data['owner_id'] = user_id
        db_user = facade.user_repo.get_by_attribute('id', user_id)

        if not db_user:
            return {'error': 'Invalid user'}, 400

        try:
            new_place = facade.create_place(place_data)
            res = new_place.to_dict_full()
            res["message"] = "Place created successfully"
            return res, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict_full() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict_full(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()

    def put(self, place_id):
        """Update a place's information"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and str(place.owner.id) != str(user_id):
            return {'error': 'Unauthorized: You are not the owner of this place'}, 403

        place_data = api.payload

        if 'owner_id' in place_data:
            return {'error': 'You cannot modify the owner_id'}, 400

        try:
            facade.update_place(place_id, place_data)
            updated_place = facade.get_place(place_id)
            res = updated_place.to_dict_full()
            res["message"] = "Place updated successfully"
            return res, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect([amenity_model])
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')

    def post(self, place_id):
        amenities_data = api.payload
        if not amenities_data or len(amenities_data) == 0:
            return {'error': 'Invalid input data'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        for amenity in amenities_data:
            a = facade.get_amenity(amenity['id'])
            if not a:
                return {'error': 'Invalid input data'}, 400
            place.add_amenity(a)

        db.session.add(place)
        db.session.commit()
        db.session.refresh(place)

        return {'message': 'Amenities added successfully'}, 200

@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')

    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200
