from server.models import db, Guest, Hotel, Booking
from datetime import date
from app import create_app

app, db = create_app()

def seed():
    with app.app_context():  
        guest1 = Guest(
            id=1,
            firstName='John',
            secondName='Doe',
            email='jd2@example.com',
            password='password123',
            mobile='0711987654',
            role='admin' 
        )
        guest2 = Guest(
            id=2,
            firstName='Jane',
            secondName='Smith',
            email='js2@example.com',
            password='password456',
            mobile='0701123456',
            role='admin'
        )
        
        db.session.add(guest1)
        db.session.add(guest2)
        db.session.commit()

        # Create hotels
        hotel1 = Hotel(
            id=1,
            name='Luxury Hotel',
            location='City Center',
            daily_rate=200.0,
            rating=4.5,
            additional_info='Luxury amenities included.',
            image='luxury_hotel.jpg'
        )
        hotel2 = Hotel(
            id=2,
            name='Budget Inn',
            location='Suburb',
            daily_rate=80.0,
            rating=3.8,
            additional_info='Affordable accommodation with basic amenities.',
            image='budget_inn.jpg'
        )

        db.session.add(hotel1)
        db.session.add(hotel2)
        db.session.commit()

        # Create bookings
        booking1 = Booking(
            id=1,
            date_of_arrival=date(2024, 7, 1),
            date_of_departure=date(2024, 7, 5),
            status='confirmed',
            hotel_id=hotel1.id,
            guest_id=guest1.id
        )
        booking2 = Booking(
            id=2,
            date_of_arrival=date(2024, 8, 10),
            date_of_departure=date(2024, 8, 15),
            status='pending',
            hotel_id=hotel2.id,
            guest_id=guest2.id
        )

        db.session.add(booking1)
        db.session.add(booking2)
        db.session.commit()

        print("Data seeded successfully.")

if __name__ == '__main__':
    seed()
