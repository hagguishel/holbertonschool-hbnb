from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request

authorizations = {
        'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Enter 'Bearer' followed by your JWT token"
    }
}
api = Namespace('users', description='User operations', authorizations=authorizations, security='Bearer Auth')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user_id = get_jwt_identity()
        return {'message': f'Hello, user {current_user_id}'}, 200

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 409

        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'message': 'User registered successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        requester_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)

        if not is_admin and str(requester_id) != str(user_id):
            return {'error': 'Unauthorized'}, 403

        if not is_admin:
            if "email" in user_data or "password" in user_data:
                return {'error': 'You cannot modify email or password.'}, 400

        email = user_data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)

            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400


        try:
            updated_user = facade.update_user(user_id, user_data, is_admin=is_admin)
            res = updated_user.to_dict()
            res ["message"] = "User updated successfully"
            return res, 200

        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/admin/')
class AdminUserCreateUser(Resource):
    @jwt_required()
    def post(self):
        """Admin-only user creation"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.get_json()
        email = user_data.get('email')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        user_data['is_admin'] = True

        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'message': 'User created by admin'}, 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/check-admin/')
class CheckAdmin(Resource):
    @jwt_required()
    def get(self):
        is_admin = get_jwt().get("is_admin", False)
        return {"is_admin": is_admin}, 200
