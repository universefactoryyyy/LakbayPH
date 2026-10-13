# database.py - creates the SQLite database, puts the starting data in it,
# and has all the functions that read and save data.
# All SQL uses ? placeholders, never values glued into the text.

import os
import random
import sqlite3
import helpers

DB_FILE = os.path.join(helpers.get_data_folder(), "lakbayph.db")

# The tables (converted from the MySQL file lakbayph_web.sql)
CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    Email TEXT UNIQUE,
    Phone TEXT UNIQUE,
    Password TEXT NOT NULL,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Address TEXT,
    BirthDate TEXT,
    Gender TEXT CHECK (Gender IN ('Male', 'Female', 'Other', 'Prefer not to say')),
    Role TEXT NOT NULL DEFAULT 'User' CHECK (Role IN ('Admin', 'User')),
    IsActive INTEGER NOT NULL DEFAULT 1,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (Email IS NOT NULL OR Phone IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS tourcategories (
    CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    CategoryName TEXT NOT NULL UNIQUE,
    CategoryType TEXT NOT NULL,
    IsActive INTEGER NOT NULL DEFAULT 1,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tourpackages (
    PackageID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    PackageType TEXT NOT NULL,
    Price REAL NOT NULL CHECK (Price >= 0),
    Description TEXT NOT NULL,
    Duration INTEGER NOT NULL CHECK (Duration >= 1),
    DurationNights INTEGER NOT NULL DEFAULT 0,
    CategoryID INTEGER NOT NULL REFERENCES tourcategories (CategoryID),
    MaxSlots INTEGER NOT NULL DEFAULT 10 CHECK (MaxSlots >= 1),
    Status TEXT DEFAULT 'active',
    StartDate TEXT NOT NULL,
    EndDate TEXT NOT NULL,
    IsGroupPackage INTEGER NOT NULL DEFAULT 0,
    GroupSize INTEGER DEFAULT 1,
    IsActive INTEGER NOT NULL DEFAULT 1,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS packagedetails (
    PackageID INTEGER PRIMARY KEY REFERENCES tourpackages (PackageID) ON DELETE CASCADE,
    PackageType TEXT NOT NULL CHECK (PackageType IN ('Freediving', 'Domestic', 'International')),
    FlagSymbol TEXT,
    IdealFor TEXT,
    Inclusions TEXT,
    ImageFileName TEXT,
    Highlights TEXT
);

CREATE TABLE IF NOT EXISTS packageimages (
    ImageID INTEGER PRIMARY KEY AUTOINCREMENT,
    PackageID INTEGER NOT NULL REFERENCES tourpackages (PackageID) ON DELETE CASCADE,
    ImageFileName TEXT NOT NULL,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (PackageID, ImageFileName)
);

CREATE TABLE IF NOT EXISTS packagelocations (
    PackageID INTEGER PRIMARY KEY REFERENCES tourpackages (PackageID) ON DELETE CASCADE,
    Location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS packageaddons (
    AddOnID INTEGER PRIMARY KEY AUTOINCREMENT,
    PackageID INTEGER NOT NULL REFERENCES tourpackages (PackageID) ON DELETE CASCADE,
    AddOnName TEXT NOT NULL,
    Price REAL NOT NULL CHECK (Price >= 0),
    Unit TEXT,
    IsActive INTEGER NOT NULL DEFAULT 1,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS promotypes (
    PromoTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    PromoTypeName TEXT NOT NULL UNIQUE CHECK (PromoTypeName IN ('PWD', 'SENIOR CITIZEN')),
    DiscountPercentage REAL NOT NULL DEFAULT 20,
    Description TEXT,
    IsActive INTEGER NOT NULL DEFAULT 1,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS promodiscounts (
    PromoID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL REFERENCES users (UserID) ON DELETE CASCADE,
    PromoTypeID INTEGER NOT NULL REFERENCES promotypes (PromoTypeID) ON DELETE CASCADE,
    DocumentNumber TEXT NOT NULL,
    Status TEXT NOT NULL DEFAULT 'Pending' CHECK (Status IN ('Pending', 'Approved', 'Rejected')),
    ValidatedBy INTEGER REFERENCES users (UserID) ON DELETE SET NULL,
    ValidationDate TEXT,
    ExpiryDate TEXT,
    Notes TEXT,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (UserID, PromoTypeID)
);

CREATE TABLE IF NOT EXISTS bookings (
    BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
    BookingReference TEXT NOT NULL UNIQUE,
    UserID INTEGER NOT NULL REFERENCES users (UserID) ON DELETE CASCADE,
    PackageID INTEGER NOT NULL REFERENCES tourpackages (PackageID) ON DELETE CASCADE,
    NumberOfPeople INTEGER NOT NULL DEFAULT 1 CHECK (NumberOfPeople >= 1),
    PromoID INTEGER REFERENCES promodiscounts (PromoID) ON DELETE SET NULL,
    TravelDate TEXT NOT NULL,
    EndDate TEXT NOT NULL,
    BookingDate TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Status TEXT NOT NULL DEFAULT 'Pending'
        CHECK (Status IN ('Pending', 'Confirmed', 'Completed', 'Cancelled')),
    Notes TEXT,
    UnitPrice REAL NOT NULL DEFAULT 0,
    DiscountAmount REAL NOT NULL DEFAULT 0,
    TotalAmount REAL NOT NULL DEFAULT 0,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookingpayments (
    BookingID INTEGER PRIMARY KEY REFERENCES bookings (BookingID) ON DELETE CASCADE,
    PaymentMethod TEXT NOT NULL DEFAULT 'Pay on Trip',
    PaymentStatus TEXT NOT NULL DEFAULT 'Pending'
        CHECK (PaymentStatus IN ('Pending', 'Paid', 'Refunded', 'Cancelled')),
    PaymentDate TEXT,
    TransactionReference TEXT,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookingaddons (
    BookingAddOnID INTEGER PRIMARY KEY AUTOINCREMENT,
    BookingID INTEGER NOT NULL REFERENCES bookings (BookingID) ON DELETE CASCADE,
    AddOnID INTEGER NOT NULL REFERENCES packageaddons (AddOnID) ON DELETE CASCADE,
    Quantity INTEGER NOT NULL DEFAULT 1 CHECK (Quantity >= 1),
    UnitPrice REAL NOT NULL,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookinghistory (
    HistoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    BookingID INTEGER NOT NULL REFERENCES bookings (BookingID) ON DELETE CASCADE,
    UserID INTEGER NOT NULL REFERENCES users (UserID) ON DELETE CASCADE,
    ActionType TEXT NOT NULL,
    ActionDate TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ActionDescription TEXT,
    PreviousStatus TEXT,
    NewStatus TEXT,
    ModifiedBy INTEGER REFERENCES users (UserID) ON DELETE SET NULL,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reviews (
    ReviewID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL REFERENCES users (UserID) ON DELETE CASCADE,
    BookingID INTEGER UNIQUE REFERENCES bookings (BookingID) ON DELETE SET NULL,
    PackageID INTEGER REFERENCES tourpackages (PackageID) ON DELETE SET NULL,
    Rating INTEGER NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    Comment TEXT,
    ReviewDate TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_bookings_date ON bookings (PackageID, TravelDate);
CREATE INDEX IF NOT EXISTS idx_bookings_user ON bookings (UserID);
CREATE INDEX IF NOT EXISTS idx_reviews_package ON reviews (PackageID);
"""


# ======================= Basic tools =======================

# Open a connection to the database file
def connect():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# Run a SELECT and return a list of dictionaries
def fetch_all(sql, values=()):
    connection = connect()
    try:
        rows = connection.execute(sql, values).fetchall()
    finally:
        connection.close()
    results = []
    for row in rows:
        results.append(dict(row))
    return results


# Run a SELECT and return only the first row (or None)
def fetch_one(sql, values=()):
    results = fetch_all(sql, values)
    if len(results) == 0:
        return None
    return results[0]


# Run one INSERT / UPDATE and save it. Returns the new row ID.
def run_change(sql, values=()):
    connection = connect()
    try:
        cursor = connection.execute(sql, values)
        connection.commit()
        return cursor.lastrowid
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# ======================= Create and seed =======================

# Create the tables, and on the first run put in the starting data
def setup_database():
    first_time = not os.path.exists(DB_FILE)
    connection = connect()
    try:
        connection.executescript(CREATE_TABLES)
        count = connection.execute("SELECT COUNT(*) FROM tourpackages").fetchone()[0]
        if count == 0:
            insert_seed_data(connection)
        update_old_data(connection)
        connection.commit()
        connection.close()
    except Exception:
        connection.close()
        # Do not leave a half-made database behind
        if first_time and os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        raise


# Insert the 36 packages and other data from assets/seed_data.sql
def insert_seed_data(connection):
    seed_file = open(helpers.resource_path(os.path.join("assets", "seed_data.sql")), encoding="utf-8")
    seed_sql = seed_file.read()
    seed_file.close()
    connection.executescript(seed_sql)

    # Fix: the old dates ended in 2025, so packages now run from today for one year
    start = helpers.date_to_text(helpers.today())
    end = helpers.date_to_text(helpers.one_year_from(helpers.today()))
    connection.execute("UPDATE tourpackages SET StartDate = ?, EndDate = ?", (start, end))

    # Fix: the admin password is saved as a salted hash, not plain text
    connection.execute(
        "INSERT INTO users (UserID, Username, Email, Password, FirstName, LastName, Role) "
        "VALUES (1, 'admin', 'admin@gmail.com', ?, 'Ken', 'Harold', 'Admin')",
        (helpers.hash_password("admin123"),))


# Bring a database made by an older version of the app up to date
def update_old_data(connection):
    # The old admin account becomes admin / admin@gmail.com / admin123
    connection.execute(
        "UPDATE users SET Username = 'admin', Email = 'admin@gmail.com', Password = ? "
        "WHERE Username = 'admin_ken' AND Role = 'Admin'",
        (helpers.hash_password("admin123"),))
    # Every main picture is also the first picture in the package's gallery
    connection.execute(
        "INSERT INTO packageimages (PackageID, ImageFileName) "
        "SELECT PackageID, ImageFileName FROM packagedetails "
        "WHERE ImageFileName IS NOT NULL AND ImageFileName <> '' "
        "AND PackageID NOT IN (SELECT PackageID FROM packageimages)")


# ======================= Packages =======================

# All package info in one SELECT with JOINs (instead of the MySQL views)
PACKAGE_SELECT = """
SELECT tp.*, pd.IdealFor, pd.Inclusions, pd.ImageFileName, pd.Highlights,
       pl.Location, tc.CategoryName,
       IFNULL(r.AvgRating, 0) AS AvgRating, IFNULL(r.ReviewCount, 0) AS ReviewCount,
       IFNULL(b.TotalBooked, 0) AS TotalBooked,
       (SELECT COUNT(*) FROM packageimages pi WHERE pi.PackageID = tp.PackageID) AS ImageCount
FROM tourpackages tp
LEFT JOIN packagedetails pd ON pd.PackageID = tp.PackageID
LEFT JOIN packagelocations pl ON pl.PackageID = tp.PackageID
LEFT JOIN tourcategories tc ON tc.CategoryID = tp.CategoryID
LEFT JOIN (SELECT PackageID, ROUND(AVG(Rating), 1) AS AvgRating, COUNT(*) AS ReviewCount
           FROM reviews GROUP BY PackageID) r ON r.PackageID = tp.PackageID
LEFT JOIN (SELECT PackageID, SUM(NumberOfPeople) AS TotalBooked
           FROM bookings WHERE Status <> 'Cancelled' GROUP BY PackageID) b
       ON b.PackageID = tp.PackageID
"""
ACTIVE_ONLY = " WHERE tp.IsActive = 1 AND tp.Status = 'active' "

# The sort choices. The ORDER BY text comes only from this list, never from the user.
SORT_OPTIONS = {
    "Newest": "tp.CreatedAt DESC, tp.PackageID DESC",
    "Price: Low to High": "tp.Price ASC, tp.PackageID",
    "Price: High to Low": "tp.Price DESC, tp.PackageID",
    "Most Booked": "TotalBooked DESC, AvgRating DESC, tp.PackageID",
    "Top Rated": "AvgRating DESC, ReviewCount DESC, tp.PackageID",
}


# All packages that users can see, sorted
def get_active_packages(sort_name="Newest"):
    order = SORT_OPTIONS.get(sort_name, SORT_OPTIONS["Newest"])
    return fetch_all(PACKAGE_SELECT + ACTIVE_ONLY + " ORDER BY " + order)


# Most booked first; if no bookings yet, best rated, then the first packages
def get_most_booked(limit):
    return fetch_all(PACKAGE_SELECT + ACTIVE_ONLY +
                     " ORDER BY TotalBooked DESC, AvgRating DESC, tp.PackageID LIMIT ?", (limit,))


# Newest packages first
def get_recent_packages(limit):
    return fetch_all(PACKAGE_SELECT + ACTIVE_ONLY +
                     " ORDER BY tp.CreatedAt DESC, tp.PackageID DESC LIMIT ?", (limit,))


# One package by its ID
def get_package(package_id):
    return fetch_one(PACKAGE_SELECT + " WHERE tp.PackageID = ?", (package_id,))


# Every package, also the deleted ones (for the admin)
def get_all_packages():
    return fetch_all(PACKAGE_SELECT + " ORDER BY tp.PackageID")


# All tour categories
def get_categories():
    return fetch_all("SELECT * FROM tourcategories WHERE IsActive = 1 ORDER BY CategoryID")


# The add-ons of a package that can still be chosen
def get_addons(package_id):
    return fetch_all("SELECT * FROM packageaddons WHERE PackageID = ? AND IsActive = 1 "
                     "ORDER BY AddOnID", (package_id,))


# ======================= Slots =======================

# How many people already booked this package on this travel date
def count_booked(connection, package_id, travel_date):
    row = connection.execute(
        "SELECT IFNULL(SUM(NumberOfPeople), 0) FROM bookings "
        "WHERE PackageID = ? AND TravelDate = ? AND Status IN ('Pending', 'Confirmed')",
        (package_id, travel_date)).fetchone()
    return row[0]


# How many slots are still free on a travel date
def get_slots_left(package_id, travel_date):
    connection = connect()
    try:
        package = connection.execute("SELECT MaxSlots FROM tourpackages WHERE PackageID = ?",
                                     (package_id,)).fetchone()
        booked = count_booked(connection, package_id, travel_date)
    finally:
        connection.close()
    return package[0] - booked


# ======================= Users =======================

# Find a user by email, phone number or username
def find_user_by_login(login_text):
    login = login_text.strip()
    if "@" in login:
        return fetch_one("SELECT * FROM users WHERE Email = ?", (login.lower(),))
    if helpers.is_valid_phone(login):
        return fetch_one("SELECT * FROM users WHERE Phone = ?", (helpers.normalize_phone(login),))
    return fetch_one("SELECT * FROM users WHERE Username = ? COLLATE NOCASE", (login,))


# One user by ID
def get_user(user_id):
    return fetch_one("SELECT * FROM users WHERE UserID = ?", (user_id,))


# Check if an email is already used by another user
def email_taken(email, user_id=0):
    row = fetch_one("SELECT UserID FROM users WHERE Email = ? AND UserID <> ?", (email, user_id))
    return row is not None


# Check if a phone is already used by another user
def phone_taken(phone, user_id=0):
    row = fetch_one("SELECT UserID FROM users WHERE Phone = ? AND UserID <> ?", (phone, user_id))
    return row is not None


# Make a username like "juandelacruz4821" that nobody else has
def make_username(first_name, last_name):
    base = ""
    for letter in (first_name + last_name).lower():
        if letter.isascii() and letter.isalnum():
            base = base + letter
    if base == "":
        base = "user"
    while True:
        username = base[:15] + str(random.randint(1000, 9999))
        if fetch_one("SELECT UserID FROM users WHERE Username = ?", (username,)) is None:
            return username


# Save a new user (email or phone can be None, but not both)
def create_user(first_name, last_name, email, phone, password):
    username = make_username(first_name, last_name)
    now = helpers.now_text()
    return run_change(
        "INSERT INTO users (Username, Email, Phone, Password, FirstName, LastName, Role, "
        "CreatedAt, UpdatedAt) VALUES (?, ?, ?, ?, ?, ?, 'User', ?, ?)",
        (username, email, phone, helpers.hash_password(password), first_name, last_name, now, now))


# Save changes to a user's profile
def update_profile(user_id, user):
    run_change(
        "UPDATE users SET FirstName = ?, LastName = ?, Email = ?, Phone = ?, Address = ?, "
        "Gender = ?, UpdatedAt = ? WHERE UserID = ?",
        (user["FirstName"], user["LastName"], user["Email"], user["Phone"],
         user["Address"], user["Gender"], helpers.now_text(), user_id))


# Save a new password (hashed)
def update_password(user_id, new_password):
    run_change("UPDATE users SET Password = ?, UpdatedAt = ? WHERE UserID = ?",
               (helpers.hash_password(new_password), helpers.now_text(), user_id))


# Check in the database (not just on screen) that this user is an active admin
def user_is_admin(user_id):
    user = get_user(user_id)
    return user is not None and user["Role"] == "Admin" and user["IsActive"] == 1


# ======================= Bookings =======================

# Booking info with package, payment, customer and review (instead of the MySQL views)
BOOKING_SELECT = """
SELECT b.*, tp.Title, tp.PackageType, tp.Duration, pl.Location, pd.ImageFileName,
       u.FirstName, u.LastName, u.Email, u.Phone,
       bp.PaymentMethod, bp.PaymentStatus, bp.PaymentDate, bp.TransactionReference,
       pt.PromoTypeName, r.ReviewID, r.Rating
FROM bookings b
JOIN tourpackages tp ON tp.PackageID = b.PackageID
JOIN users u ON u.UserID = b.UserID
LEFT JOIN packagelocations pl ON pl.PackageID = b.PackageID
LEFT JOIN packagedetails pd ON pd.PackageID = b.PackageID
LEFT JOIN bookingpayments bp ON bp.BookingID = b.BookingID
LEFT JOIN promodiscounts pr ON pr.PromoID = b.PromoID
LEFT JOIN promotypes pt ON pt.PromoTypeID = pr.PromoTypeID
LEFT JOIN reviews r ON r.BookingID = b.BookingID
"""


# Make a reference like LPH-20261008-0001 (number of bookings made today + 1)
def make_booking_reference(connection):
    prefix = "LPH-" + helpers.today().strftime("%Y%m%d") + "-"
    row = connection.execute("SELECT COUNT(*) FROM bookings WHERE BookingReference LIKE ?",
                             (prefix + "%",)).fetchone()
    return prefix + str(row[0] + 1).zfill(4)


# Write one line in the booking history
def add_history(connection, booking_id, user_id, action, description, old_status, new_status, modified_by):
    connection.execute(
        "INSERT INTO bookinghistory (BookingID, UserID, ActionType, ActionDate, ActionDescription, "
        "PreviousStatus, NewStatus, ModifiedBy) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (booking_id, user_id, action, helpers.now_text(), description, old_status, new_status, modified_by))


# Save the booking, payment, add-ons and history together.
# If anything fails, everything is undone (rollback).
def save_booking(booking, addons, payment):
    connection = connect()
    try:
        # Check the slots again right before saving
        package = connection.execute("SELECT MaxSlots FROM tourpackages WHERE PackageID = ?",
                                     (booking["PackageID"],)).fetchone()
        booked = count_booked(connection, booking["PackageID"], booking["TravelDate"])
        if booked + booking["NumberOfPeople"] > package[0]:
            raise ValueError("Sorry, only " + str(package[0] - booked) + " slot(s) are left on this date.")
        reference = make_booking_reference(connection)
        booking_id = insert_booking_row(connection, booking, reference)
        insert_payment_row(connection, booking_id, payment)
        for addon in addons:
            connection.execute("INSERT INTO bookingaddons (BookingID, AddOnID, Quantity, UnitPrice) "
                               "VALUES (?, ?, ?, ?)",
                               (booking_id, addon["AddOnID"], addon["Quantity"], addon["Price"]))
        add_history(connection, booking_id, booking["UserID"], "Created", "Booking created by customer",
                    None, "Pending", booking["UserID"])
        connection.commit()
        return booking_id
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# Insert the row in the bookings table
def insert_booking_row(connection, booking, reference):
    now = helpers.now_text()
    cursor = connection.execute(
        "INSERT INTO bookings (BookingReference, UserID, PackageID, NumberOfPeople, PromoID, "
        "TravelDate, EndDate, BookingDate, Status, Notes, UnitPrice, DiscountAmount, TotalAmount, "
        "CreatedAt, UpdatedAt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?, ?, ?, ?, ?, ?)",
        (reference, booking["UserID"], booking["PackageID"], booking["NumberOfPeople"],
         booking["PromoID"], booking["TravelDate"], booking["EndDate"], now, booking["Notes"],
         booking["UnitPrice"], booking["DiscountAmount"], booking["TotalAmount"], now, now))
    return cursor.lastrowid


# Insert the row in the bookingpayments table
def insert_payment_row(connection, booking_id, payment):
    now = helpers.now_text()
    payment_date = None
    if payment["PaymentStatus"] == "Paid":
        payment_date = now
    connection.execute(
        "INSERT INTO bookingpayments (BookingID, PaymentMethod, PaymentStatus, PaymentDate, "
        "TransactionReference, CreatedAt, UpdatedAt) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (booking_id, payment["PaymentMethod"], payment["PaymentStatus"], payment_date,
         payment["TransactionReference"], now, now))


# One booking with all its info
def get_booking(booking_id):
    return fetch_one(BOOKING_SELECT + " WHERE b.BookingID = ?", (booking_id,))


# The add-ons chosen in a booking
def get_booking_addons(booking_id):
    return fetch_all("SELECT ba.*, pa.AddOnName, pa.Unit FROM bookingaddons ba "
                     "JOIN packageaddons pa ON pa.AddOnID = ba.AddOnID "
                     "WHERE ba.BookingID = ? ORDER BY ba.BookingAddOnID", (booking_id,))


# All bookings of one user
def get_user_bookings(user_id):
    return fetch_all(BOOKING_SELECT + " WHERE b.UserID = ? ORDER BY b.TravelDate, b.BookingID",
                     (user_id,))


# All bookings (for the admin), or only one status
def get_all_bookings(status="All"):
    if status == "All":
        return fetch_all(BOOKING_SELECT + " ORDER BY b.BookingID DESC")
    return fetch_all(BOOKING_SELECT + " WHERE b.Status = ? ORDER BY b.BookingID DESC", (status,))


# Change a booking's status and write it in the history (one transaction)
def change_booking_status(booking_id, new_status, modified_by, description):
    connection = connect()
    try:
        row = connection.execute("SELECT Status, UserID FROM bookings WHERE BookingID = ?",
                                 (booking_id,)).fetchone()
        connection.execute("UPDATE bookings SET Status = ?, UpdatedAt = ? WHERE BookingID = ?",
                           (new_status, helpers.now_text(), booking_id))
        if new_status == "Cancelled":
            # A paid booking is refunded, an unpaid one is just cancelled
            connection.execute(
                "UPDATE bookingpayments SET PaymentStatus = CASE WHEN PaymentStatus = 'Paid' "
                "THEN 'Refunded' ELSE 'Cancelled' END, UpdatedAt = ? WHERE BookingID = ?",
                (helpers.now_text(), booking_id))
        add_history(connection, booking_id, row["UserID"], "Status Change", description,
                    row["Status"], new_status, modified_by)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# A customer cancels their own booking (only before the travel date)
def cancel_booking_for_user(booking_id, user_id):
    booking = get_booking(booking_id)
    if booking is None or booking["UserID"] != user_id:
        raise ValueError("This booking was not found.")
    if booking["Status"] not in ("Pending", "Confirmed"):
        raise ValueError("Only pending or confirmed bookings can be cancelled.")
    if helpers.text_to_date(booking["TravelDate"]) <= helpers.today():
        raise ValueError("You can only cancel before the travel date.")
    change_booking_status(booking_id, "Cancelled", user_id, "Cancelled by customer")


# Confirmed bookings whose end date has passed become Completed
def auto_complete_bookings():
    today_text = helpers.date_to_text(helpers.today())
    finished = fetch_all("SELECT BookingID FROM bookings WHERE Status = 'Confirmed' AND EndDate < ?",
                         (today_text,))
    for booking in finished:
        change_booking_status(booking["BookingID"], "Completed", None, "Trip finished (automatic)")


# The admin marks a booking as paid
def mark_payment_paid(booking_id, admin_id):
    connection = connect()
    try:
        row = connection.execute("SELECT Status, UserID FROM bookings WHERE BookingID = ?",
                                 (booking_id,)).fetchone()
        connection.execute("UPDATE bookingpayments SET PaymentStatus = 'Paid', PaymentDate = ?, "
                           "UpdatedAt = ? WHERE BookingID = ?",
                           (helpers.now_text(), helpers.now_text(), booking_id))
        add_history(connection, booking_id, row["UserID"], "Payment", "Payment marked as paid by admin",
                    row["Status"], row["Status"], admin_id)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# The history lines of a booking
def get_booking_history(booking_id):
    return fetch_all("SELECT * FROM bookinghistory WHERE BookingID = ? ORDER BY HistoryID",
                     (booking_id,))


# ======================= Reviews =======================

# Save a review (rating 1-5, once per completed booking)
def add_review(user_id, booking_id, rating, comment):
    rating = int(rating)
    if rating < 1 or rating > 5:
        raise ValueError("The rating must be from 1 to 5.")
    booking = get_booking(booking_id)
    if booking is None or booking["UserID"] != user_id:
        raise ValueError("This booking was not found.")
    if booking["Status"] != "Completed":
        raise ValueError("You can only review a completed trip.")
    if booking["ReviewID"] is not None:
        raise ValueError("You already reviewed this booking.")
    now = helpers.now_text()
    run_change("INSERT INTO reviews (UserID, BookingID, PackageID, Rating, Comment, ReviewDate, "
               "CreatedAt, UpdatedAt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               (user_id, booking_id, booking["PackageID"], rating, comment, now, now, now))


# The reviews of one package, newest first
def get_package_reviews(package_id):
    return fetch_all("SELECT r.*, u.FirstName, u.LastName FROM reviews r "
                     "JOIN users u ON u.UserID = r.UserID WHERE r.PackageID = ? "
                     "ORDER BY r.ReviewDate DESC", (package_id,))


# The newest reviews of all packages (for the home page)
def get_latest_reviews(limit):
    return fetch_all("SELECT r.*, u.FirstName, u.LastName, tp.Title FROM reviews r "
                     "JOIN users u ON u.UserID = r.UserID "
                     "LEFT JOIN tourpackages tp ON tp.PackageID = r.PackageID "
                     "ORDER BY r.ReviewDate DESC LIMIT ?", (limit,))


# ======================= Discounts (PWD / Senior Citizen) =======================

# The discount types (PWD and SENIOR CITIZEN)
def get_promo_types():
    return fetch_all("SELECT * FROM promotypes WHERE IsActive = 1 ORDER BY PromoTypeID")


# The discount requests of one user
def get_user_promos(user_id):
    return fetch_all("SELECT pd.*, pt.PromoTypeName, pt.DiscountPercentage FROM promodiscounts pd "
                     "JOIN promotypes pt ON pt.PromoTypeID = pd.PromoTypeID "
                     "WHERE pd.UserID = ? ORDER BY pd.PromoTypeID", (user_id,))


# The user's request for one discount type (or None)
def get_user_promo(user_id, promo_type_id):
    return fetch_one("SELECT pd.*, pt.PromoTypeName, pt.DiscountPercentage FROM promodiscounts pd "
                     "JOIN promotypes pt ON pt.PromoTypeID = pd.PromoTypeID "
                     "WHERE pd.UserID = ? AND pd.PromoTypeID = ?", (user_id, promo_type_id))


# Send an ID number for approval (a rejected request can be sent again)
def submit_promo_request(user_id, promo_type_id, document_number):
    old_request = get_user_promo(user_id, promo_type_id)
    now = helpers.now_text()
    if old_request is None:
        run_change("INSERT INTO promodiscounts (UserID, PromoTypeID, DocumentNumber, Status, "
                   "CreatedAt, UpdatedAt) VALUES (?, ?, ?, 'Pending', ?, ?)",
                   (user_id, promo_type_id, document_number, now, now))
    elif old_request["Status"] == "Rejected":
        run_change("UPDATE promodiscounts SET DocumentNumber = ?, Status = 'Pending', ValidatedBy = NULL, "
                   "ValidationDate = NULL, UpdatedAt = ? WHERE PromoID = ?",
                   (document_number, now, old_request["PromoID"]))
    else:
        raise ValueError("You already have a " + old_request["Status"].lower() + " request for this discount.")


# All discount requests (for the admin), or only one status
def get_promo_requests(status="All"):
    sql = ("SELECT pd.*, pt.PromoTypeName, u.FirstName, u.LastName, u.Email, u.Phone "
           "FROM promodiscounts pd JOIN promotypes pt ON pt.PromoTypeID = pd.PromoTypeID "
           "JOIN users u ON u.UserID = pd.UserID ")
    if status == "All":
        return fetch_all(sql + "ORDER BY pd.PromoID DESC")
    return fetch_all(sql + "WHERE pd.Status = ? ORDER BY pd.PromoID DESC", (status,))


# The admin approves or rejects a discount request
def set_promo_status(promo_id, status, admin_id):
    now = helpers.now_text()
    run_change("UPDATE promodiscounts SET Status = ?, ValidatedBy = ?, ValidationDate = ?, "
               "UpdatedAt = ? WHERE PromoID = ?", (status, admin_id, now, now, promo_id))


# ======================= Admin: packages =======================

# Save a package into tourpackages, packagedetails and packagelocations together.
# package_id None means a new package. Returns the package ID.
def save_package(package, addons, package_id=None):
    connection = connect()
    try:
        if package_id is None:
            package_id = insert_package_rows(connection, package)
        else:
            update_package_rows(connection, package, package_id)
        save_addon_rows(connection, package_id, addons)
        connection.commit()
        return package_id
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# The values of tourpackages in the same order as the SQL below
def package_values(package):
    return (package["Title"], package["PackageType"], package["Price"], package["Description"],
            package["Duration"], package["DurationNights"], package["CategoryID"],
            package["MaxSlots"], package["Status"], package["StartDate"], package["EndDate"],
            package["IsGroupPackage"], package["GroupSize"], package["IsActive"])


# Insert a new package in the 3 tables
def insert_package_rows(connection, package):
    now = helpers.now_text()
    cursor = connection.execute(
        "INSERT INTO tourpackages (Title, PackageType, Price, Description, Duration, DurationNights, "
        "CategoryID, MaxSlots, Status, StartDate, EndDate, IsGroupPackage, GroupSize, IsActive, "
        "CreatedAt, UpdatedAt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        package_values(package) + (now, now))
    package_id = cursor.lastrowid
    connection.execute(
        "INSERT INTO packagedetails (PackageID, PackageType, IdealFor, Inclusions, Highlights) "
        "VALUES (?, ?, ?, ?, ?)",
        (package_id, package["PackageType"], package["IdealFor"], package["Inclusions"],
         package["Highlights"]))
    connection.execute("INSERT INTO packagelocations (PackageID, Location) VALUES (?, ?)",
                       (package_id, package["Location"]))
    return package_id


# Update a package in the 3 tables
def update_package_rows(connection, package, package_id):
    connection.execute(
        "UPDATE tourpackages SET Title = ?, PackageType = ?, Price = ?, Description = ?, Duration = ?, "
        "DurationNights = ?, CategoryID = ?, MaxSlots = ?, Status = ?, StartDate = ?, EndDate = ?, "
        "IsGroupPackage = ?, GroupSize = ?, IsActive = ?, UpdatedAt = ? WHERE PackageID = ?",
        package_values(package) + (helpers.now_text(), package_id))
    connection.execute(
        "UPDATE packagedetails SET PackageType = ?, IdealFor = ?, Inclusions = ?, "
        "Highlights = ? WHERE PackageID = ?",
        (package["PackageType"], package["IdealFor"], package["Inclusions"],
         package["Highlights"], package_id))
    connection.execute("UPDATE packagelocations SET Location = ? WHERE PackageID = ?",
                       (package["Location"], package_id))


# Add, change or remove the add-ons of a package.
# Removed add-ons are only hidden (IsActive = 0) because old bookings use them.
def save_addon_rows(connection, package_id, addons):
    for addon in addons:
        if addon["AddOnID"] is not None and addon["Removed"]:
            connection.execute("UPDATE packageaddons SET IsActive = 0 WHERE AddOnID = ?",
                               (addon["AddOnID"],))
        elif addon["AddOnID"] is not None:
            connection.execute("UPDATE packageaddons SET AddOnName = ?, Price = ?, Unit = ? "
                               "WHERE AddOnID = ?",
                               (addon["AddOnName"], addon["Price"], addon["Unit"], addon["AddOnID"]))
        elif not addon["Removed"]:
            connection.execute("INSERT INTO packageaddons (PackageID, AddOnName, Price, Unit, CreatedAt) "
                               "VALUES (?, ?, ?, ?, ?)",
                               (package_id, addon["AddOnName"], addon["Price"], addon["Unit"],
                                helpers.now_text()))


# Soft delete: hide the package (old bookings still point to it)
def soft_delete_package(package_id):
    run_change("UPDATE tourpackages SET IsActive = 0, UpdatedAt = ? WHERE PackageID = ?",
               (helpers.now_text(), package_id))


# Make a picture the main (cover) picture of a package
def set_package_image(package_id, file_name):
    run_change("UPDATE packagedetails SET ImageFileName = ? WHERE PackageID = ?", (file_name, package_id))


# The main picture file names of all packages
def get_image_file_names():
    return fetch_all("SELECT PackageID, ImageFileName FROM packagedetails ORDER BY PackageID")


# All pictures of a package, the main picture first
def get_package_images(package_id):
    return fetch_all(
        "SELECT pi.* FROM packageimages pi JOIN packagedetails pd ON pd.PackageID = pi.PackageID "
        "WHERE pi.PackageID = ? ORDER BY (pi.ImageFileName = pd.ImageFileName) DESC, pi.ImageID",
        (package_id,))


# Add pictures to a package (one transaction). The first one becomes the main
# picture if the package has none. Pictures it already has are skipped.
def add_package_images(package_id, file_names):
    connection = connect()
    try:
        for file_name in file_names:
            connection.execute("INSERT OR IGNORE INTO packageimages (PackageID, ImageFileName, CreatedAt) "
                               "VALUES (?, ?, ?)", (package_id, file_name, helpers.now_text()))
        if len(file_names) > 0:
            connection.execute("UPDATE packagedetails SET ImageFileName = ? WHERE PackageID = ? "
                               "AND (ImageFileName IS NULL OR ImageFileName = '')",
                               (file_names[0], package_id))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# Remove a picture from a package. If it was the main picture, the next one
# becomes the main picture (or none if it was the last).
def remove_package_image(package_id, file_name):
    connection = connect()
    try:
        connection.execute("DELETE FROM packageimages WHERE PackageID = ? AND ImageFileName = ?",
                           (package_id, file_name))
        next_image = connection.execute("SELECT ImageFileName FROM packageimages WHERE PackageID = ? "
                                        "ORDER BY ImageID LIMIT 1", (package_id,)).fetchone()
        new_cover = None
        if next_image is not None:
            new_cover = next_image[0]
        connection.execute("UPDATE packagedetails SET ImageFileName = ? WHERE PackageID = ? AND ImageFileName = ?",
                           (new_cover, package_id, file_name))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# Change the file name of a picture (used when Import Folder finds fdbasic.png for fdbasic.jpg)
def rename_package_image(package_id, old_name, new_name):
    connection = connect()
    try:
        connection.execute("UPDATE OR IGNORE packageimages SET ImageFileName = ? WHERE PackageID = ? AND ImageFileName = ?",
                           (new_name, package_id, old_name))
        connection.execute("UPDATE packagedetails SET ImageFileName = ? WHERE PackageID = ? AND ImageFileName = ?",
                           (new_name, package_id, old_name))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# ======================= Admin: dashboard =======================

# Numbers for the dashboard boxes
def get_dashboard_stats():
    stats = {}
    stats["TotalBookings"] = fetch_one("SELECT COUNT(*) AS N FROM bookings")["N"]
    stats["Revenue"] = fetch_one(
        "SELECT IFNULL(SUM(b.TotalAmount), 0) AS N FROM bookings b "
        "JOIN bookingpayments bp ON bp.BookingID = b.BookingID "
        "WHERE bp.PaymentStatus = 'Paid' AND b.Status <> 'Cancelled'")["N"]
    stats["ActivePackages"] = fetch_one(
        "SELECT COUNT(*) AS N FROM tourpackages WHERE IsActive = 1 AND Status = 'active'")["N"]
    stats["PendingBookings"] = fetch_one(
        "SELECT COUNT(*) AS N FROM bookings WHERE Status = 'Pending'")["N"]
    stats["PendingDiscounts"] = fetch_one(
        "SELECT COUNT(*) AS N FROM promodiscounts WHERE Status = 'Pending'")["N"]
    return stats


# How many bookings have each status, like {"Pending": 3, "Confirmed": 1}
def get_booking_counts():
    counts = {}
    for row in fetch_all("SELECT Status, COUNT(*) AS N FROM bookings GROUP BY Status"):
        counts[row["Status"]] = row["N"]
    return counts


# How many discount requests have each status
def get_promo_counts():
    counts = {}
    for row in fetch_all("SELECT Status, COUNT(*) AS N FROM promodiscounts GROUP BY Status"):
        counts[row["Status"]] = row["N"]
    return counts


# The newest bookings (for the dashboard)
def get_recent_bookings(limit):
    return fetch_all(BOOKING_SELECT + " ORDER BY b.BookingID DESC LIMIT ?", (limit,))


# Number of bookings (not cancelled) for each package type, for the bar chart
def get_bookings_per_type():
    return fetch_all("SELECT tp.PackageType, COUNT(b.BookingID) AS Total FROM tourpackages tp "
                     "LEFT JOIN bookings b ON b.PackageID = tp.PackageID AND b.Status <> 'Cancelled' "
                     "GROUP BY tp.PackageType ORDER BY tp.PackageType")
