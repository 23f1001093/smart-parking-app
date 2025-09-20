from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, ParkingLot, ParkingSpot, Reservation
from functools import wraps
from datetime import datetime

api = Blueprint('api', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- Authentication ---
@api.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already taken'}), 409
    hashed_password = generate_password_hash(password, method='scrypt')
    new_user = User(email=email, password_hash=hashed_password, username=username, role='user')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['user_role'] = user.role
        return jsonify({'message': 'Login successful', 'user_id': user.id, 'role': user.role}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@api.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

@api.route('/me', methods=['GET'])
@login_required
def get_current_user():
    user = User.query.get(session['user_id'])
    return jsonify(user.serialize()), 200

# --- Admin: Parking Lot Management ---
@api.route('/admin/parkinglots', methods=['GET'])
@admin_required
def list_parking_lots():
    lots = ParkingLot.query.all()
    return jsonify([lot.serialize() for lot in lots]), 200

@api.route('/admin/parkinglots', methods=['POST'])
@admin_required
def create_parking_lot():
    data = request.json
    lot = ParkingLot(
        prime_location_name=data['prime_location_name'],
        address=data.get('address'),
        pin_code=data.get('pin_code'),
        price=data['price'],
        number_of_spots=data['number_of_spots']
    )
    db.session.add(lot)
    db.session.flush()
    for _ in range(lot.number_of_spots):
        spot = ParkingSpot(lot_id=lot.id, status='A')
        db.session.add(spot)
    db.session.commit()
    return jsonify(lot.serialize()), 201

@api.route('/admin/parkinglots/<int:lot_id>', methods=['PUT'])
@admin_required
def edit_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.json
    if 'prime_location_name' in data:
        lot.prime_location_name = data['prime_location_name']
    if 'address' in data:
        lot.address = data['address']
    if 'pin_code' in data:
        lot.pin_code = data['pin_code']
    if 'price' in data:
        lot.price = data['price']
    if 'number_of_spots' in data:
        current_occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
        if current_occupied > 0:
            return jsonify({'message': 'Cannot change spot count while spots are occupied'}), 400
        ParkingSpot.query.filter_by(lot_id=lot.id).delete()
        db.session.flush()
        for _ in range(data['number_of_spots']):
            spot = ParkingSpot(lot_id=lot.id, status='A')
            db.session.add(spot)
        lot.number_of_spots = data['number_of_spots']
    db.session.commit()
    return jsonify(lot.serialize()), 200

@api.route('/admin/parkinglots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
    if occupied > 0:
        return jsonify({'message': 'Cannot delete, spots are occupied'}), 400
    db.session.delete(lot)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200

@api.route('/admin/users', methods=['GET'])
@admin_required
def list_users():
    users = User.query.filter_by(role='user').all()
    return jsonify([u.serialize() for u in users]), 200

@api.route('/admin/reservations', methods=['GET'])
@admin_required
def list_reservations():
    reservations = Reservation.query.all()
    return jsonify([r.serialize() for r in reservations]), 200

# --- Admin: Spots status and details by lot ---
@api.route('/admin/parkinglots/<int:lot_id>/spots', methods=['GET'])
@admin_required
def get_spots_in_lot(lot_id):
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    out = []
    for spot in spots:
        d = spot.serialize()
        if spot.status == 'O':
            res = Reservation.query.filter_by(spot_id=spot.id, leaving_timestamp=None).first()
            if res:
                d['vehicle_number'] = res.vehicle_number
                d['user_id'] = res.user_id
        out.append(d)
    return jsonify(out), 200

# --- User: Parking Lot View & Reserve ---
@api.route('/parkinglots', methods=['GET'])
@login_required
def user_list_parkinglots():
    lots = ParkingLot.query.all()
    output = []
    for lot in lots:
        available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        out = lot.serialize()
        out['available_spots'] = available_spots
        output.append(out)
    return jsonify(output), 200

@api.route('/parkinglots/<int:lot_id>/reserve', methods=['POST'])
@login_required
def reserve_parking_spot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spot = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').first()
    if not spot:
        return jsonify({'message': 'No spots available'}), 400
    spot.status = 'O'
    data = request.json or {}
    vehicle_number = data.get('vehicle_number')
    remarks = data.get('remarks')
    new_reservation = Reservation(
        user_id=session['user_id'],
        spot_id=spot.id,
        parking_timestamp=datetime.utcnow(),
        parking_cost=lot.price,
        vehicle_number=vehicle_number,
        remarks=remarks
    )
    db.session.add(new_reservation)
    db.session.commit()
    return jsonify({
        'message': 'Spot reserved',
        'reservation_id': new_reservation.id,
        'spot_id': spot.id
    }), 201

@api.route('/reservations/<int:reservation_id>/release', methods=['POST'])
@login_required
def release_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.user_id != session['user_id']:
        return jsonify({'message': 'Unauthorized'}), 403
    if reservation.leaving_timestamp:
        return jsonify({'message': 'Already released'}), 400
    reservation.leaving_timestamp = datetime.utcnow()
    spot = ParkingSpot.query.get(reservation.spot_id)
    spot.status = 'A'
    db.session.commit()
    return jsonify({'message': 'Spot released'}), 200

@api.route('/my/reservations', methods=['GET'])
@login_required
def get_user_reservations():
    user_id = session['user_id']
    reservations = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_timestamp.desc()).all()
    return jsonify([r.serialize() for r in reservations]), 200

# --- Async Export Example using Celery batch job ---
from tasks import export_user_reservations
@api.route('/my/export', methods=['POST'])
@login_required
def trigger_export():
    user_id = session['user_id']
    email = request.json.get("email")
    export_user_reservations.delay(user_id, email)
    return jsonify({'message': 'Your export job has started. You will receive an alert when done.'}), 202

# --- Simple Caching Example ---
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=1)

@api.route('/cached/parkinglots', methods=['GET'])
@login_required
def cached_lots():
    cache_key = "parkinglots"
    cached = r.get(cache_key)
    if cached:
        return jsonify(eval(cached.decode('utf-8')))
    lots = ParkingLot.query.all()
    out = [lot.serialize() for lot in lots]
    r.setex(cache_key, 30, str(out))
    return jsonify(out), 200

