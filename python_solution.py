import sqlite3

conn = sqlite3.connect("travel_agency.db")
c = conn.cursor()

# 1) Створення таблиць
c.execute("""CREATE TABLE IF NOT EXISTS client (
    id_client INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone_number TEXT,
    passport_information TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS tour (
    id_tour INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    duration INTEGER,
    base_price REAL
)""")

c.execute("""CREATE TABLE IF NOT EXISTS booking (
    id_booking INTEGER PRIMARY KEY,
    status TEXT CHECK(status IN ('pending', 'confirmed', 'cancelled')),
    total_price REAL,
    booking_date TEXT,
    tour_id INTEGER,
    client_id INTEGER,
    FOREIGN KEY (tour_id) REFERENCES tour(id_tour),
    FOREIGN KEY (client_id) REFERENCES client(id_client)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS payment (
    id_payment INTEGER PRIMARY KEY,
    payment_method TEXT CHECK(payment_method IN ('card', 'cash', 'transfer')),
    amount REAL,
    payment_date TEXT,
    booking_id INTEGER,
    FOREIGN KEY (booking_id) REFERENCES booking(id_booking)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS hotel (
    id_hotel INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    star_rating TEXT CHECK(star_rating IN ('1', '2', '3', '4', '5')),
    contact_info TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS country (
    id_country INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20),
    visa_required BOOLEAN
)""")

c.execute("""CREATE TABLE IF NOT EXISTS tour_country (
    id_tour_country INTEGER PRIMARY KEY AUTOINCREMENT,
    tour_id INTEGER,
    country_id INTEGER,
    FOREIGN KEY (tour_id) REFERENCES tour(id_tour),
    FOREIGN KEY (country_id) REFERENCES country(id_country)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS tour_hotel (
    id_tour_hotel INTEGER PRIMARY KEY AUTOINCREMENT,
    tour_id INTEGER,
    hotel_id INTEGER,
    FOREIGN KEY (tour_id) REFERENCES tour(id_tour),
    FOREIGN KEY (hotel_id) REFERENCES hotel(id_hotel)
)""")

# 2) Заповнення таблиць даними
# Клієнти
c.execute("""INSERT INTO client (first_name, last_name, email, phone_number, passport_information) VALUES 
('Марина', 'Сидоренко', 'marina.sydorenko@example.com', '+380931122334', 'CD987654'),
('Віктор', 'Мельник', 'viktor.melnyk@example.com', '+380671234567', 'EF321789'),
('Наталія', 'Шевченко', 'natalia.shevchenko@example.com', '+380991234567', 'GH876543')""")

# Країни
c.execute("""INSERT INTO country (name, visa_required) VALUES 
('Італія', 1),
('Іспанія', 1),
('Франція', 1)""")

# Готелі
c.execute("""INSERT INTO hotel (name, address, star_rating, contact_info) VALUES 
('Bella Roma', 'Rome, Italy', '3', '+390612345678'),
('Costa del Sol', 'Malaga, Spain', '4', '+34951123456'),
('Eiffel View', 'Paris, France', '5', '+33123456789')""")

# Тури
c.execute("""INSERT INTO tour (title, description, duration, base_price) VALUES 
('Скарби Італії', 'Екскурсія Римом, Флоренцією та Венецією', 120, 950.00),
('Іспанські канікули', 'Тиждень у Барселоні та Мадриді', 168, 870.00),
('Французька класика', 'Париж, Лувр, Версаль', 96, 980.00)""")

# Тури та країни
c.execute("""INSERT INTO tour_country (tour_id, country_id) VALUES 
(1, 1),
(2, 2),
(3, 3)""")

# Тури та готелі
c.execute("""INSERT INTO tour_hotel (tour_id, hotel_id) VALUES 
(1, 1),
(2, 2),
(3, 3)""")

# Бронювання
c.execute("""INSERT INTO booking (status, total_price, booking_date, tour_id, client_id) VALUES 
('confirmed', 950.00, '2025-07-12 10:00:00', 1, 1),
('pending', 870.00, '2025-08-15 09:00:00', 2, 2),
('confirmed', 980.00, '2025-09-20 11:15:00', 3, 3)""")

# Платежі
c.execute("""INSERT INTO payment (payment_method, amount, payment_date, booking_id) VALUES 
('card', 950.00, '2025-07-13 09:30:00', 1),
('transfer', 870.00, '2025-08-16 10:00:00', 2),
('transfer', 980.00, '2025-09-21 13:00:00', 3)""")

# SELECT запити
print("\n1. SELECT запити")

Kate, [19.11.2025 22:43]
# Усі підтверджені бронювання з іменами клієнтів і назвами турів
print("\n 1) Усі підтверджені бронювання з клієнтами й турами")
c.execute("""
SELECT booking.id_booking, client.first_name, client.last_name, tour.title, booking.total_price
FROM booking
JOIN client ON booking.client_id = client.id_client
JOIN tour ON booking.tour_id = tour.id_tour
WHERE booking.status = 'confirmed'
""")
confirmed_bookings = c.fetchall()
print(confirmed_bookings)

#Тури з готелями, які мають рейтинг 4 зірки
print("\n2) Тури з готелями  які мають рейтинг 4 зірки")
c.execute("""
SELECT tour.title, hotel.name, hotel.star_rating
FROM tour
JOIN tour_hotel ON tour.id_tour = tour_hotel.tour_id
JOIN hotel ON tour_hotel.hotel_id = hotel.id_hotel
WHERE hotel.star_rating = '4'
""")
tours_4star = c.fetchall()
print(tours_4star)


# 4) UPDATE запити
# Один підтверджений запис змінити на pending
c.execute("UPDATE booking SET status = 'pending' WHERE id_booking = 1")

# Змінити рейтинг готелю з 4 зірок на 5
c.execute("UPDATE hotel SET star_rating = '5' WHERE star_rating = '4'")

conn.commit()

# 5) SELECT запити після змін
print("\n2. SELECT після UPDATE")

print("\n1) Підтверджені бронювання після змін")
c.execute("""
SELECT booking.id_booking, client.first_name, client.last_name, tour.title, booking.status
FROM booking
JOIN client ON booking.client_id = client.id_client
JOIN tour ON booking.tour_id = tour.id_tour
WHERE booking.status = 'confirmed'
""")
print(c.fetchall())

print("\n2) Тури з готелями 4 зірки після змін")
c.execute("""
SELECT tour.title, hotel.name, hotel.star_rating
FROM tour
JOIN tour_hotel ON tour.id_tour = tour_hotel.tour_id
JOIN hotel ON tour_hotel.hotel_id = hotel.id_hotel
WHERE hotel.star_rating = '4'
""")
print(c.fetchall())

conn.close()