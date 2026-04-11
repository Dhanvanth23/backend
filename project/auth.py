"""
Authentication Module
Handles user registration, login, logout, and session management
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
import hashlib
import secrets
import re
import functools
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import logging

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

# Global variables to be initialized
db = None

def init_auth(firestore_db):
    """Initialize auth module"""
    global db
    db = firestore_db

# Helper Functions
def hash_pin(pin):
    """Hash PIN using SHA-256"""
    return hashlib.sha256(pin.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username format"""
    return len(username) >= 3 and len(username) <= 50

def validate_pin(pin):
    """Validate PIN format"""
    return len(pin) >= 4 and pin.isdigit()

# Middleware
def login_required(f):
    """Decorator to require login"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current user ID from session"""
    return session.get('user_id')

@auth_bp.route('/auth/check-session', methods=['GET'])
def check_session():
    """Check if user is authenticated and return user info"""
    try:
        if 'user_id' not in session:
            return jsonify({'authenticated': False}), 200
        
        user_id = session.get('user_id')
        user_doc = db.collection('users').document(user_id).get()
        
        if not user_doc.exists:
            session.clear()
            return jsonify({'authenticated': False}), 200
        
        user_data = user_doc.to_dict()
        
        return jsonify({
            'authenticated': True,
            'user_id': user_id,
            'username': user_data.get('username'),
            'language': user_data.get('language', 'en')  # RETURN LANGUAGE
        }), 200
        
    except Exception as e:
        logging.error(f'Error checking session: {str(e)}')
        return jsonify({'authenticated': False}), 200

# Routes
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'pin']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        pin = data['pin']
        
        # Validate inputs
        if not validate_username(username):
            return jsonify({'error': 'Username must be 3-50 characters'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not validate_pin(pin):
            return jsonify({'error': 'PIN must be at least 4 digits'}), 400
        
        # Check if user already exists
        users_ref = db.collection('users')
        
        # Check username
        username_query = users_ref.where(filter=FieldFilter('username', '==', username)).limit(1).get()
        if username_query:
            return jsonify({'error': 'Username already exists'}), 409
        
        # Check email
        email_query = users_ref.where(filter=FieldFilter('email', '==', email)).limit(1).get()
        if email_query:
            return jsonify({'error': 'Email already exists'}), 409
        
        # Hash the PIN
        hashed_pin = hash_pin(pin)
        
        # Create user document
        user_data = {
            'username': username,
            'email': email,
            'pin_hash': hashed_pin,  # Changed from 'pin' to 'pin_hash'
            'created_at': datetime.now(),
            'language': 'en'
        }
        
        user_ref = db.collection('users').document()
        user_ref.set(user_data)
        
        logging.info(f'New user registered: {username}')
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_ref.id
        }), 201
        
    except Exception as e:
        logging.error(f'Error in register: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'pin' not in data:
            return jsonify({'error': 'Missing username or PIN'}), 400
        
        username = data['username'].strip()
        pin = data['pin']
        
        # Find user by username
        users_ref = db.collection('users')
        query = users_ref.where(filter=FieldFilter('username', '==', username)).limit(1).get()
        
        if not query:
            return jsonify({'error': 'Invalid username or PIN'}), 401
        
        user_doc = query[0]
        user_data = user_doc.to_dict()
        
        # Verify PIN
        hashed_pin = hash_pin(pin)
        if user_data.get('pin_hash') != hashed_pin:
            return jsonify({'error': 'Invalid username or PIN'}), 401
        
        # Create session
        session['user_id'] = user_doc.id
        session['username'] = user_data['username']
        session.permanent = True
        
        logging.info(f'User logged in: {username}')
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user_doc.id,
                'username': user_data['username'],
                'email': user_data['email']
            }
        }), 200
        
    except Exception as e:
        logging.error(f'Error in login: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout user"""
    try:
        # Clear the session
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/me', methods=['GET'])
@login_required
def get_current_user_info():
    """Get current user information"""
    try:
        user_id = get_current_user()
        user_doc = db.collection('users').document(user_id).get()
        
        if not user_doc.exists:
            session.clear()
            return jsonify({'error': 'User not found'}), 404
        
        user_data = user_doc.to_dict()
        
        return jsonify({
            'id': user_doc.id,
            'username': user_data.get('username'),
            'email': user_data.get('email'),
            'created_at': user_data.get('created_at').isoformat() if user_data.get('created_at') else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/change-pin', methods=['POST'])
@login_required
def change_pin():
    """Change user PIN"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        
        if 'old_pin' not in data or 'new_pin' not in data:
            return jsonify({'error': 'Missing old PIN or new PIN'}), 400
        
        old_pin = data['old_pin']
        new_pin = data['new_pin']
        
        if not validate_pin(new_pin):
            return jsonify({'error': 'New PIN must be at least 4 digits'}), 400
        
        # Get user document
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = user_doc.to_dict()
        
        # Verify old PIN
        old_pin_hash = hash_pin(old_pin)
        if user_data['pin_hash'] != old_pin_hash:
            return jsonify({'error': 'Incorrect old PIN'}), 401
        
        # Update PIN
        new_pin_hash = hash_pin(new_pin)
        user_ref.update({
            'pin_hash': new_pin_hash,
            'updated_at': datetime.utcnow()
        })
        
        return jsonify({'message': 'PIN changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Delete user account"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        
        if 'pin' not in data:
            return jsonify({'error': 'PIN is required'}), 400
        
        pin = data['pin']
        
        # Get user document
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = user_doc.to_dict()
        
        # Verify PIN
        pin_hash = hash_pin(pin)
        if user_data['pin_hash'] != pin_hash:
            return jsonify({'error': 'Incorrect PIN'}), 401
        
        # Delete user data (you might want to delete related data too)
        # For now, just delete the user document
        user_ref.delete()
        
        # Clear session
        session.clear()
        
        return jsonify({'message': 'Account deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500