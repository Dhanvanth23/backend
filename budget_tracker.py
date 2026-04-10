"""
Budget Tracker Module — Multi-Track System
Users create named tracks, each with its own income, expenses, and budget limit.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud import firestore
import logging

budget_bp = Blueprint('budget', __name__, url_prefix='/api')

# Collection names
TRACKS_COLLECTION = 'tracks'
EXPENSES_COLLECTION = 'expenses'
INCOME_COLLECTION = 'income'

# Global variables to be initialized
db = None
login_required = None
get_current_user = None

def init_budget_tracker(firestore_db, auth_module):
    """Initialize budget tracker module"""
    global db, login_required, get_current_user
    db = firestore_db
    login_required = auth_module.login_required
    get_current_user = auth_module.get_current_user


# ═══════════════════════════════════════════════════
#  AUTO-MIGRATION: old data → "Default" track
# ═══════════════════════════════════════════════════

def ensure_migration(user_id):
    """
    Check if user has any tracks.  If not, create a 'Default' track
    and re-parent all existing expenses / income under it.
    Called once per session (on first tracks list request).
    """
    tracks_ref = db.collection(TRACKS_COLLECTION)
    existing = list(
        tracks_ref.where(filter=FieldFilter('user_id', '==', user_id))
        .limit(1).stream()
    )
    if existing:
        return  # already migrated

    # Check if there is any legacy data worth migrating
    has_expenses = list(
        db.collection(EXPENSES_COLLECTION)
        .where(filter=FieldFilter('user_id', '==', user_id))
        .limit(1).stream()
    )
    has_income = list(
        db.collection(INCOME_COLLECTION)
        .where(filter=FieldFilter('user_id', '==', user_id))
        .limit(1).stream()
    )

    if not has_expenses and not has_income:
        return  # nothing to migrate

    # Create "Default" track
    budget_limit = 0.0
    # Try to pull the latest budget amount from old budgets collection
    try:
        old_budgets = list(
            db.collection('budgets')
            .where(filter=FieldFilter('user_id', '==', user_id))
            .order_by('year', direction=firestore.Query.DESCENDING)
            .limit(1).stream()
        )
        if old_budgets:
            budget_limit = float(old_budgets[0].to_dict().get('allocated_amount', 0))
    except Exception:
        pass

    track_ref = db.collection(TRACKS_COLLECTION).document()
    track_data = {
        'user_id': user_id,
        'name': 'Default',
        'budget_limit': budget_limit,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    track_ref.set(track_data)
    track_id = track_ref.id
    logging.info(f"Created Default track {track_id} for user {user_id}")

    # Assign all orphan expenses to this track
    batch = db.batch()
    count = 0
    for doc in db.collection(EXPENSES_COLLECTION).where(
        filter=FieldFilter('user_id', '==', user_id)
    ).stream():
        if not doc.to_dict().get('track_id'):
            batch.update(doc.reference, {'track_id': track_id})
            count += 1
            if count % 400 == 0:   # Firestore batch limit ~500
                batch.commit()
                batch = db.batch()

    # Assign all orphan income to this track
    for doc in db.collection(INCOME_COLLECTION).where(
        filter=FieldFilter('user_id', '==', user_id)
    ).stream():
        if not doc.to_dict().get('track_id'):
            batch.update(doc.reference, {'track_id': track_id})
            count += 1
            if count % 400 == 0:
                batch.commit()
                batch = db.batch()

    if count % 400 != 0:
        batch.commit()

    logging.info(f"Migrated {count} documents to Default track for user {user_id}")


# ═══════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════

def track_to_dict(doc):
    """Convert Firestore track document to dictionary"""
    data = doc.to_dict()
    data['id'] = doc.id
    if 'created_at' in data and data['created_at']:
        data['created_at'] = data['created_at'].isoformat()
    if 'updated_at' in data and data['updated_at']:
        data['updated_at'] = data['updated_at'].isoformat()
    data.pop('user_id', None)
    return data

def expense_to_dict(doc):
    """Convert Firestore expense document to dictionary"""
    data = doc.to_dict()
    data['id'] = doc.id
    if isinstance(data.get('date'), datetime):
        data['date'] = data['date'].date().isoformat()
    elif hasattr(data.get('date'), 'date'):
        data['date'] = data['date'].date().isoformat()
    if 'created_at' in data and data['created_at']:
        data['created_at'] = data['created_at'].isoformat()
    if 'updated_at' in data and data['updated_at']:
        data['updated_at'] = data['updated_at'].isoformat()
    data.pop('user_id', None)
    return data

def income_to_dict(doc):
    """Convert Firestore income document to dictionary"""
    data = doc.to_dict()
    data['id'] = doc.id
    if isinstance(data.get('date'), datetime):
        data['date'] = data['date'].date().isoformat()
    elif hasattr(data.get('date'), 'date'):
        data['date'] = data['date'].date().isoformat()
    if 'created_at' in data and data['created_at']:
        data['created_at'] = data['created_at'].isoformat()
    if 'updated_at' in data and data['updated_at']:
        data['updated_at'] = data['updated_at'].isoformat()
    data.pop('user_id', None)
    return data

def get_track_summary(user_id, track_id):
    """Compute summary numbers for a single track."""
    total_income = 0.0
    total_expenses = 0.0

    for doc in db.collection(INCOME_COLLECTION).where(
        filter=FieldFilter('user_id', '==', user_id)
    ).where(filter=FieldFilter('track_id', '==', track_id)).stream():
        total_income += float(doc.to_dict().get('amount', 0))

    for doc in db.collection(EXPENSES_COLLECTION).where(
        filter=FieldFilter('user_id', '==', user_id)
    ).where(filter=FieldFilter('track_id', '==', track_id)).stream():
        total_expenses += float(doc.to_dict().get('amount', 0))

    return {
        'total_income': round(total_income, 2),
        'total_expenses': round(total_expenses, 2),
    }


# ═══════════════════════════════════════════════════
#  TRACK ROUTES
# ═══════════════════════════════════════════════════

# --- List all tracks ---
@budget_bp.route('/tracks/', methods=['GET'])
def list_tracks():
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(_list_tracks)()

def _list_tracks():
    try:
        user_id = get_current_user()
        ensure_migration(user_id)

        tracks_ref = db.collection(TRACKS_COLLECTION)
        query = tracks_ref.where(filter=FieldFilter('user_id', '==', user_id))
        docs = list(query.stream())

        # Sort by created_at descending in Python (avoids composite index requirement)
        docs.sort(key=lambda d: d.to_dict().get('created_at', datetime.min), reverse=True)

        tracks = []
        for doc in docs:
            t = track_to_dict(doc)
            summary = get_track_summary(user_id, doc.id)
            t['total_income'] = summary['total_income']
            t['total_expenses'] = summary['total_expenses']
            t['total_available'] = round(t.get('budget_limit', 0) + summary['total_income'], 2)
            t['remaining'] = round(t['total_available'] - summary['total_expenses'], 2)
            pct = 0
            if t['total_available'] > 0:
                pct = round(summary['total_expenses'] / t['total_available'] * 100, 2)
            t['used_percentage'] = min(pct, 100)
            tracks.append(t)

        return jsonify(tracks), 200
    except Exception as e:
        logging.error(f"Error listing tracks: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# --- Create track ---
@budget_bp.route('/tracks/', methods=['POST'])
def create_track():
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(_create_track)()

def _create_track():
    try:
        user_id = get_current_user()
        data = request.get_json()

        name = (data.get('name') or '').strip()
        if not name:
            return jsonify({'error': 'Track name is required'}), 400

        budget_limit = 0.0
        if data.get('budget_limit') is not None:
            try:
                budget_limit = float(data['budget_limit'])
                if budget_limit < 0:
                    return jsonify({'error': 'Budget limit cannot be negative'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid budget limit'}), 400

        track_data = {
            'user_id': user_id,
            'name': name,
            'budget_limit': budget_limit,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        doc_ref = db.collection(TRACKS_COLLECTION).document()
        doc_ref.set(track_data)
        result = track_to_dict(doc_ref.get())
        result['total_income'] = 0
        result['total_expenses'] = 0
        result['total_available'] = budget_limit
        result['remaining'] = budget_limit
        result['used_percentage'] = 0

        return jsonify(result), 201
    except Exception as e:
        logging.error(f"Error creating track: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# --- Get single track with dashboard ---
@budget_bp.route('/tracks/<track_id>/', methods=['GET'])
def get_track(track_id):
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(lambda: _get_track(track_id))()

def _get_track(track_id):
    try:
        user_id = get_current_user()
        doc = db.collection(TRACKS_COLLECTION).document(track_id).get()
        if not doc.exists:
            return jsonify({'error': 'Track not found'}), 404
        if doc.to_dict().get('user_id') != user_id:
            return jsonify({'error': 'Access denied'}), 403

        t = track_to_dict(doc)
        summary = get_track_summary(user_id, track_id)
        t['total_income'] = summary['total_income']
        t['total_expenses'] = summary['total_expenses']
        t['total_available'] = round(t.get('budget_limit', 0) + summary['total_income'], 2)
        t['remaining'] = round(t['total_available'] - summary['total_expenses'], 2)
        pct = 0
        if t['total_available'] > 0:
            pct = round(summary['total_expenses'] / t['total_available'] * 100, 2)
        t['used_percentage'] = min(pct, 100)
        return jsonify(t), 200
    except Exception as e:
        logging.error(f"Error getting track: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# --- Update track ---
@budget_bp.route('/tracks/<track_id>/', methods=['PUT'])
def update_track(track_id):
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(lambda: _update_track(track_id))()

def _update_track(track_id):
    try:
        user_id = get_current_user()
        doc_ref = db.collection(TRACKS_COLLECTION).document(track_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({'error': 'Track not found'}), 404
        if doc.to_dict().get('user_id') != user_id:
            return jsonify({'error': 'Access denied'}), 403

        data = request.get_json()
        update = {'updated_at': datetime.utcnow()}

        name = (data.get('name') or '').strip()
        if name:
            update['name'] = name

        if data.get('budget_limit') is not None:
            try:
                bl = float(data['budget_limit'])
                if bl < 0:
                    return jsonify({'error': 'Budget limit cannot be negative'}), 400
                update['budget_limit'] = bl
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid budget limit'}), 400

        doc_ref.update(update)
        result = track_to_dict(doc_ref.get())
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error updating track: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# --- Delete track ---
@budget_bp.route('/tracks/<track_id>/', methods=['DELETE'])
def delete_track(track_id):
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(lambda: _delete_track(track_id))()

def _delete_track(track_id):
    try:
        user_id = get_current_user()
        doc_ref = db.collection(TRACKS_COLLECTION).document(track_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({'error': 'Track not found'}), 404
        if doc.to_dict().get('user_id') != user_id:
            return jsonify({'error': 'Access denied'}), 403

        # Delete all expenses in this track
        batch = db.batch()
        count = 0
        for edoc in db.collection(EXPENSES_COLLECTION).where(
            filter=FieldFilter('track_id', '==', track_id)
        ).stream():
            batch.delete(edoc.reference)
            count += 1
            if count % 400 == 0:
                batch.commit()
                batch = db.batch()

        # Delete all income in this track
        for idoc in db.collection(INCOME_COLLECTION).where(
            filter=FieldFilter('track_id', '==', track_id)
        ).stream():
            batch.delete(idoc.reference)
            count += 1
            if count % 400 == 0:
                batch.commit()
                batch = db.batch()

        batch.commit()
        doc_ref.delete()

        return jsonify({'message': 'Track and all its data deleted'}), 200
    except Exception as e:
        logging.error(f"Error deleting track: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════
#  EXPENSE ROUTES (track-aware)
# ═══════════════════════════════════════════════════

@budget_bp.route('/expenses/', methods=['GET'])
def get_expenses():
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(_get_expenses)()

def _get_expenses():
    try:
        user_id = get_current_user()
        track_id = request.args.get('track_id')
        category = request.args.get('category')

        query = db.collection(EXPENSES_COLLECTION).where(
            filter=FieldFilter('user_id', '==', user_id)
        )

        if track_id:
            query = query.where(filter=FieldFilter('track_id', '==', track_id))
        if category:
            query = query.where(filter=FieldFilter('category', '==', category))

        docs = list(query.stream())
        docs.sort(key=lambda d: d.to_dict().get('date', datetime.min), reverse=True)
        expenses = [expense_to_dict(doc) for doc in docs]
        return jsonify(expenses), 200
    except Exception as e:
        logging.error(f"Error in get_expenses: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@budget_bp.route('/expenses/', methods=['POST'])
def create_expense():
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(_create_expense)()

def _create_expense():
    try:
        user_id = get_current_user()
        data = request.get_json()

        # Validate track_id
        track_id = data.get('track_id')
        if not track_id:
            return jsonify({'error': 'track_id is required'}), 400

        # Verify track belongs to user
        track_doc = db.collection(TRACKS_COLLECTION).document(track_id).get()
        if not track_doc.exists or track_doc.to_dict().get('user_id') != user_id:
            return jsonify({'error': 'Invalid track'}), 400

        required_fields = ['amount', 'category', 'date', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400

        try:
            expense_date = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        valid_categories = ['food', 'transportation', 'shopping', 'entertainment',
                          'utilities', 'healthcare', 'education', 'travel', 'lend', 'other']
        if data['category'] not in valid_categories:
            return jsonify({'error': 'Invalid category'}), 400

        expense_data = {
            'user_id': user_id,
            'track_id': track_id,
            'amount': amount,
            'category': data['category'],
            'date': expense_date,
            'description': data['description'].strip(),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        doc_ref = db.collection(EXPENSES_COLLECTION).document()
        doc_ref.set(expense_data)
        result = expense_to_dict(doc_ref.get())
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@budget_bp.route('/expenses/<expense_id>/', methods=['PUT'])
def update_expense(expense_id):
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(lambda: _update_expense(expense_id))()

def _update_expense(expense_id):
    try:
        user_id = get_current_user()
        doc_ref = db.collection(EXPENSES_COLLECTION).document(expense_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({'error': 'Expense not found'}), 404
        if doc.to_dict().get('user_id') != user_id:
            return jsonify({'error': 'Access denied'}), 403

        data = request.get_json()

        required_fields = ['amount', 'category', 'date', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400

        try:
            expense_date = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

        valid_categories = ['food', 'transportation', 'shopping', 'entertainment',
                          'utilities', 'healthcare', 'education', 'travel', 'lend', 'other']
        if data['category'] not in valid_categories:
            return jsonify({'error': 'Invalid category'}), 400

        update_data = {
            'amount': amount,
            'category': data['category'],
            'date': expense_date,
            'description': data['description'].strip(),
            'updated_at': datetime.utcnow()
        }

        doc_ref.update(update_data)
        result = expense_to_dict(doc_ref.get())
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@budget_bp.route('/expenses/<expense_id>/', methods=['DELETE'])
def delete_expense(expense_id):
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(lambda: _delete_expense(expense_id))()

def _delete_expense(expense_id):
    try:
        user_id = get_current_user()
        doc_ref = db.collection(EXPENSES_COLLECTION).document(expense_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({'error': 'Expense not found'}), 404
        if doc.to_dict().get('user_id') != user_id:
            return jsonify({'error': 'Access denied'}), 403
        doc_ref.delete()
        return jsonify({'message': 'Expense deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════
#  INCOME ROUTES (track-aware)
# ═══════════════════════════════════════════════════

@budget_bp.route('/income/', methods=['GET'])
def get_income():
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(_get_income)()

def _get_income():
    try:
        user_id = get_current_user()
        track_id = request.args.get('track_id')

        query = db.collection(INCOME_COLLECTION).where(
            filter=FieldFilter('user_id', '==', user_id)
        )

        if track_id:
            query = query.where(filter=FieldFilter('track_id', '==', track_id))

        docs = list(query.stream())
        docs.sort(key=lambda d: d.to_dict().get('date', datetime.min), reverse=True)
        income_entries = [income_to_dict(doc) for doc in docs]
        return jsonify(income_entries), 200
    except Exception as e:
        logging.error(f"Error in get_income: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@budget_bp.route('/income/', methods=['POST'])
def add_income():
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(_add_income)()

def _add_income():
    try:
        user_id = get_current_user()
        data = request.get_json()

        # Validate track_id
        track_id = data.get('track_id')
        if not track_id:
            return jsonify({'error': 'track_id is required'}), 400

        track_doc = db.collection(TRACKS_COLLECTION).document(track_id).get()
        if not track_doc.exists or track_doc.to_dict().get('user_id') != user_id:
            return jsonify({'error': 'Invalid track'}), 400

        required_fields = ['amount', 'source', 'date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400

        try:
            income_date = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        income_data = {
            'user_id': user_id,
            'track_id': track_id,
            'amount': amount,
            'source': data['source'].strip(),
            'date': income_date,
            'description': data.get('description', '').strip(),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }

        doc_ref = db.collection(INCOME_COLLECTION).document()
        doc_ref.set(income_data)
        result = income_to_dict(doc_ref.get())
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@budget_bp.route('/income/<income_id>/', methods=['PUT'])
def update_income(income_id):
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(lambda: _update_income(income_id))()

def _update_income(income_id):
    try:
        user_id = get_current_user()
        doc_ref = db.collection(INCOME_COLLECTION).document(income_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({'error': 'Income entry not found'}), 404
        if doc.to_dict().get('user_id') != user_id:
            return jsonify({'error': 'Access denied'}), 403

        data = request.get_json()

        required_fields = ['amount', 'source', 'date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({'error': 'Amount must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400

        try:
            income_date = datetime.strptime(data['date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

        update_data = {
            'amount': amount,
            'source': data['source'].strip(),
            'date': income_date,
            'description': data.get('description', '').strip(),
            'updated_at': datetime.utcnow()
        }

        doc_ref.update(update_data)
        result = income_to_dict(doc_ref.get())
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@budget_bp.route('/income/<income_id>/', methods=['DELETE'])
def delete_income(income_id):
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(lambda: _delete_income(income_id))()

def _delete_income(income_id):
    try:
        user_id = get_current_user()
        doc_ref = db.collection(INCOME_COLLECTION).document(income_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({'error': 'Income entry not found'}), 404
        if doc.to_dict().get('user_id') != user_id:
            return jsonify({'error': 'Access denied'}), 403
        doc_ref.delete()
        return jsonify({'message': 'Income entry deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════
#  LANGUAGE PREFERENCE
# ═══════════════════════════════════════════════════

@budget_bp.route('/user/update-language', methods=['POST'])
def update_language():
    if login_required is None:
        return jsonify({'error': 'Module not initialized'}), 500
    return login_required(_update_language)()

def _update_language():
    """Update user's language preference"""
    try:
        user_id = get_current_user()
        data = request.get_json()
        lang = data.get('language', 'en')
        if lang not in ['en', 'ta']:
            return jsonify({'error': 'Invalid language'}), 400
        user_ref = db.collection('users').document(user_id)
        user_ref.update({'language': lang})
        return jsonify({'message': 'Language updated successfully', 'language': lang}), 200
    except Exception as e:
        logging.error(f"Error updating language: {str(e)}")
        return jsonify({'error': str(e)}), 500