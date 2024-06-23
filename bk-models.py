from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    secondName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15))
    role = db.Column(db.String(20), default='guest', nullable=False)

    def __repr__(self):
        return f'<Guest {self.firstName} {self.secondName}>'

    def to_dict(self):
        return {
            'id': self.id,
            'firstName': self.firstName,
            'secondName': self.secondName,
            'email': self.email,
            'mobile': self.mobile,
            'role': self.role
        }


guests_hotels = db.Table('guests_hotels',
    db.Column('guest_id', db.Integer, db.ForeignKey('guests.id'), primary_key=True),
    db.Column('hotel_id', db.Integer, db.ForeignKey('hotels.id'), primary_key=True),

)

class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    daily_rate = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    additional_info = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'daily_rate': self.daily_rate,
            'rating': self.rating,
            'additional_info': self.additional_info,
            'image': self.image
        }


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    date_of_arrival = db.Column(db.Date, nullable=False)
    date_of_departure = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="pending")
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    guest_email = db.Column(db.String(100), nullable=False)
    guest_mobile = db.Column(db.String(15))
    total_amount = db.Column(db.Float, nullable=False)

    def get_all(cls):
        return cls.query.all()

    def find_by_id(cls, booking_id):
        return cls.query.filter_by(id=booking_id).first()

    def to_dict(self):
        return {
            'id': self.id,
            'date_of_arrival': self.date_of_arrival,
            'date_of_departure': self.date_of_departure,
            'status': self.status,
            'hotel_id': self.hotel_id,
            'guest_id': self.guest_id,
            'guest_email': self.guest_email,
            'guest_mobile': self.guest_mobile,
            'total_amount': self.total_amount
        }

    def __repr__(self):
        return f'<Booking {self.id}>'