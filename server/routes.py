import logging
from flask import  make_response, Blueprint, jsonify, request
from server.models import db, Hotel, Guest, Booking
from functools import wraps

bp = Blueprint('app', __name__)

@bp.route('/')
def index():
    return 'Welcome to TravelEase'

from flask import Blueprint, jsonify, request, make_response
from server.models import db, Guest

@bp.route('/register', methods=['OPTIONS', 'POST'])
def register():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    if request.method == 'POST':
        logging.info('Received POST request to /register')
        logging.info('Request JSON: %s', request.json)

        try:
            data = request.get_json()
            logging.info('Parsed JSON data: %s', data)

            new_guest = Guest(
                firstName=data['firstName'],
                secondName=data['secondName'],
                email=data['email'],
                password=data['password'],
                mobile=data['mobile']
            )

            db.session.add(new_guest)
            db.session.commit()
            response = jsonify({'message': 'User registered successfully'})
            response.headers['Access-Control-Allow-Origin'] = '*'
            logging.info('Response JSON: %s', response.get_data(as_text=True))
            return response, 201
        except Exception as e:
            db.session.rollback()
            logging.error('Error: %s', str(e))
            response = jsonify({'error': str(e)})
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response, 500        

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    guest = Guest.query.filter_by(email=data['email']).first()
    if guest and guest.password == data['password']:
        return jsonify({'message': 'User logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/guests', methods=['POST'])
def create_guest():
    data = request.get_json()
    new_guest = Guest(
        firstName=data['first_name'],
        secondName=data['second_name'],
        email=data['email'],
        password=data['password'],
        mobile=data.get('mobile'),
        role=data.get('role', 'guest')
    )
    try:
        db.session.add(new_guest)
        db.session.commit()
        return jsonify(new_guest.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/guests', methods=['GET'])
def get_all_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests])

@bp.route('/guests/<int:guest_id>', methods=['GET'])
def get_guest(guest_id):
    guest = Guest.query.get_or_404(guest_id)
    return jsonify(guest.to_dict())

@bp.route('/guests/<int:guest_id>', methods=['PUT'])
def update_guest(guest_id):
    guest = Guest.query.get_or_404(guest_id)
    data = request.get_json()
    guest.firstName = data.get('first_name', guest.firstName)
    guest.secondName = data.get('second_name', guest.secondName)
    guest.email = data.get('email', guest.email)
    guest.password = data.get('password', guest.password)
    guest.mobile = data.get('mobile', guest.mobile)
    guest.role = data.get('role', guest.role)
    try:
        db.session.commit()
        return jsonify(guest.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/guests/<int:guest_id>', methods=['DELETE'])
def delete_guest(guest_id):
    guest = Guest.query.get_or_404(guest_id)
    try:
        db.session.delete(guest)
        db.session.commit()
        return jsonify({'message': 'Guest deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/hotels', methods=['POST'])
def create_hotel():
    data = request.get_json()
    new_hotel = Hotel(
        name=data['name'],
        location=data['location'],
        daily_rate=data['daily_rate'],
        rating=data['rating'],
        additional_info=data.get('additional_info'),
        image=data.get('image')
    )
    try:
        db.session.add(new_hotel)
        db.session.commit()
        return jsonify(new_hotel.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/hotels', methods=['GET'])
def get_all_hotels():
    try:
        hotels = Hotel.query.all()
        return jsonify([hotel.to_dict() for hotel in hotels])
    except Exception as e:
        print(f"Error fetching hotels: {e}")
        return jsonify({"error": "An error occurred while fetching hotels"}), 500

@bp.route('/hotels/<int:hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    return jsonify(hotel.to_dict())

@bp.route('/hotels/<int:hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    data = request.get_json()
    hotel.name = data.get('name', hotel.name)
    hotel.location = data.get('location', hotel.location)
    hotel.daily_rate = data.get('daily_rate', hotel.daily_rate)
    hotel.rating = data.get('rating', hotel.rating)
    hotel.additional_info = data.get('additional_info', hotel.additional_info)
    hotel.image = data.get('image', hotel.image)
    try:
        db.session.commit()
        return jsonify(hotel.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/hotels/<int:hotel_id>', methods=['DELETE'])
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    try:
        db.session.delete(hotel)
        db.session.commit()
        return jsonify({'message': 'Hotel deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()

    required_fields = ['date_of_arrival', 'date_of_departure', 'hotel_id', 'guest_id', 'total_amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    new_booking = Booking(
        date_of_arrival=data['date_of_arrival'],
        date_of_departure=data['date_of_departure'],
        status=data.get('status', 'pending'),
        hotel_id=data['hotel_id'],
        guest_id=data['guest_id'],
        total_amount=data['total_amount']
    )

    try:

        db.session.add(new_booking)
        db.session.commit()

        return jsonify(new_booking.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Unexpected error: ' + str(e)}), 500
    
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.current_user.role != 'admin':
            return jsonify({'error': 'Access denied'}), 403  # Forbidden
        return func(*args, **kwargs)
    return wrapper

@bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return jsonify({'message': 'Welcome, Admin!'})

@bp.route('/guest/dashboard')
def guest_dashboard():
    return jsonify({'message': 'Welcome, Guest!'})

@bp.route('/bookings', methods=['GET'])
def get_all_bookings():
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings])

@bp.route('/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return jsonify(booking.to_dict())

@bp.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    data = request.get_json()
    booking.date_of_arrival = data.get('date_of_arrival', booking.date_of_arrival)
    booking.date_of_departure = data.get('date_of_departure', booking.date_of_departure)
    booking.status = data.get('status', booking.status)
    booking.hotel_id = data.get('hotel_id', booking.hotel_id)
    booking.guest_id = data.get('guest_id', booking.guest_id)
    try:
        db.session.commit()
        return jsonify(booking.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    try:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Booking deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/bookings-details', methods=['GET'])
def get_booking_details():
    try:
        bookings = Booking.query.join(Guest, Booking.guest_id == Guest.id) \
                                .join(Hotel, Booking.hotel_id == Hotel.id) \
                                .add_columns(
                                    Booking.id,
                                    Booking.date_of_arrival,
                                    Booking.date_of_departure,
                                    Booking.status,
                                    Guest.firstName,
                                    Guest.secondName,
                                    Hotel.name.label('hotel_name'),
                                    Booking.total_amount
                                ).all()

        # Transform the query result into JSON format
        booking_details = []
        for booking in bookings:
            booking_details.append({
                'id': booking.id,
                'date_of_arrival': booking.date_of_arrival,
                'date_of_departure': booking.date_of_departure,
                'status': booking.status,
                'guest': {
                    'firstName': booking.firstName,
                    'secondName': booking.secondName
                },
                'hotel': {
                    'name': booking.hotel_name
                },
                'total_amount': booking.total_amount
            })

        return jsonify(booking_details), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@bp.route('/guests/<int:guest_id>/bookings', methods=['GET'])
def get_guest_bookings(guest_id):
    try:
        guest = Guest.query.get_or_404(guest_id, description=f"Guest with id {guest_id} not found")
        bookings = Booking.query.filter_by(guest_id=guest_id).all()

        bookings_list = [booking.to_dict() for booking in bookings]
        return jsonify(bookings_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@bp.route('/guests/<int:guest_id>/booked_hotels_count', methods=['GET'])
def get_guest_booked_hotels_count(guest_id):
    guest = Guest.query.get_or_404(guest_id, description=f"Guest with id {guest_id} not found")
    
    bookings = Booking.query.filter_by(guest_id=guest_id).all()
    booked_hotels = [booking.hotel.name for booking in bookings]
    response_data = {
        'guest_id': guest.id,
        'guest_name': f"{guest.firstName} {guest.secondName}",
        'booked_hotels_count': len(booked_hotels),
        'booked_hotels': booked_hotels
    }

    return jsonify(response_data), 200

