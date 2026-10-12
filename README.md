# LakbayPH - Travel Services (Desktop App)

A travel booking app for Windows made with **Python 3 + Tkinter** and **SQLite**.
Customers can browse 36 tour packages, sign up with their email or phone, book a trip
step by step, and write reviews. Admins can manage packages (with pictures), bookings
and PWD / Senior Citizen discount requests.

## Files

| File | What it does |
|------|--------------|
| `main.py` | Starts the app, makes the window, switches pages (`show_page`) |
| `database.py` | Creates the SQLite database, adds the starting data, all the queries |
| `user_pages.py` | Home, destinations, details, log in / sign up, booking, my bookings, profile, contact, blog |
| `admin_pages.py` | Dashboard, packages (create / read / update / delete + pictures), bookings, discount requests |
| `helpers.py` | Colors, peso format, validation, password hashing, dates, pictures, scrolling |
| `test_lakbayph.py` | Tests for the price computation and the email / phone / password checks |
| `assets/` | `logo.png`, `logo.ico`, `placeholder.jpg`, default package pictures, `seed_data.sql` |
| `build.bat` | Makes `dist\LakbayPH.exe` |

## How to run (from the source code)

1. Install Python 3 from python.org (check "Add Python to PATH").
2. Install Pillow (used to show the pictures):

   ```
   python -m pip install pillow
   ```

3. Start the app:

   ```
   python main.py
   ```

On the first run the database is created and the 36 packages from `lakbayph_web.sql`
are added automatically.

## Run the tests

```
python test_lakbayph.py
```

## Make the .exe

Double-click `build.bat` (or run it in a Command Prompt). It:

1. installs Pillow and PyInstaller if they are missing,
2. runs the tests,
3. runs PyInstaller with `--onefile --windowed`, the logo icon, and the `assets` folder bundled inside.

The result is **`dist\LakbayPH.exe`**. Copy only this file to any Windows 10/11 PC; Python is
not needed there.

## Default admin login

| Email | Password |
|-------|----------|
| `adminken@email.com` | `lphttken` |

The admin uses the same Log In page and is sent to the Admin Panel.

## Where the data is saved

Everything that changes is saved in your user folder, not next to the .exe:

```
%APPDATA%\LakbayPH\lakbayph.db     <- the database
%APPDATA%\LakbayPH\images\         <- pictures uploaded by the admin
```

(Paste `%APPDATA%\LakbayPH` in the File Explorer address bar to open it.)
To **start over with fresh data**, close the app and delete that folder.

## Package pictures

- The `assets\images` folder has simple drawn pictures for all 36 packages, so the app never
  looks empty.
- To use real photos, open **Admin Panel > Packages** and click **Import Folder**. Choose the
  folder with your photos; every file whose name matches a package (`fdbasic.jpg`,
  `domboracay.png`, `intnewyork.jpeg`, ...) is copied in. The same name with another picture
  type (for example `fdbasic.png`) also works.
- **Upload Image** changes the picture of one package (png / jpg / jpeg).
- If a picture is missing, `placeholder.jpg` is shown.

## Windows SmartScreen warning

The .exe is not signed with a paid code-signing certificate, so the first time you open it
Windows may show **"Windows protected your PC"**. Click **More info** and then **Run anyway**.
This is normal for school projects and other unsigned apps.

## Changes from the original MySQL database

- **SQLite** instead of MySQL, so no server is needed. The MySQL views were replaced by normal
  SELECT queries with JOINs.
- **Sign up with email OR phone**: both are optional but unique, and at least one is required.
  Phones are saved as `09XXXXXXXXX`, so `+639...` and `09...` count as the same number.
  The username is made automatically.
- **Passwords** are saved as a salted SHA-256 hash (`salt$hash`), never as plain text.
- **Dates**: on the first run every package runs from today until one year from today.
  Travel dates must be inside this range and not in the past.
- **Ratings** must be 1 to 5, and there is one review per booking.
- **Slots** are counted per travel date: the people in Pending / Confirmed bookings on that
  date cannot be more than MaxSlots.
- `bookings` also saves `UnitPrice`, `DiscountAmount` and `TotalAmount`, so old receipts do not
  change when the admin changes a price later.
- A booking, its payment, add-ons and history are saved together. If one part fails,
  nothing is saved.
- Payments other than "Pay on Trip" are **simulated**: a fake transaction reference is made and
  no card numbers are ever asked or saved.
- Deleting a package only hides it (`IsActive = 0`), so old bookings still work.
