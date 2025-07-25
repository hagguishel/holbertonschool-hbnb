from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        user_id = get_jwt_identity()
        if isinstance(user_id, dict):
            user_id = user_id.get('id') or user_id.get('sub')

        is_admin = get_jwt().get('is_admin', False)

        review_data = api.payload
        review_data["user_id"] = user_id

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400

        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 400

        if not is_admin and place.owner.id == user.id:
            return {'error': 'You cannot review your own place'}, 400

        for r in place.reviews:
            if str(r.user.id) == str(user_id):
                return{'error': 'You have already reviewed this place'}, 400
        try:
            new_review = facade.create_review(review_data)
            res = new_review.to_dict()
            res["message"] = "Review created successfully"
            return res, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [review.to_dict() for review in facade.get_all_reviews()], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        user_id = get_jwt_identity()
        if isinstance(user_id, dict):
            user_id = user_id.get('id') or  user_id.get('sub')

        is_admin = get_jwt().get("is_admin", False)

        if not is_admin and str(review.user.id) != str(user_id):
            return {'error': 'Unauthorized'}, 403

        try:
            facade.update_review(review_id, review_data)
            updated_review = facade.get_review(review_id)
            res = updated_review.to_dict()
            res["message"] = "Review updated successfully"
            return res, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        user_id= get_jwt_identity()
        if isinstance(user_id, dict):
            user_id = user_id.get('id') or user_id.get('sub')

        is_admin = get_jwt().get("is_admin", False)

        if not is_admin and str(review.user.id) != str(user_id):
            return {'error': 'Unauthorized'}, 403

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
