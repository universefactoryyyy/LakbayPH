# helpers.py - colors, formatting, validation, images and small tools
# that are used by all the other files.

import os
import sys
import hashlib
import datetime
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps, ImageEnhance

# ---------------- Colors (defined once, used everywhere) ----------------
TEAL = "#00CFE0"
DARK_TEAL = "#0B4F5C"
DEEP_TEAL = "#06343D"
LIGHT_TEAL = "#E6FAFC"
WHITE = "#FFFFFF"
GRAY = "#6B7B80"
LIGHT_GRAY = "#F3F6F7"
BORDER = "#D5E3E6"
RED = "#E05555"
GREEN = "#2E9E5B"
GOLD = "#F5B301"

# ---------------- Fonts ----------------
FONT = "Segoe UI"
TITLE_FONT = (FONT, 20, "bold")
HEADING_FONT = (FONT, 14, "bold")
NORMAL_FONT = (FONT, 10)
BOLD_FONT = (FONT, 10, "bold")
SMALL_FONT = (FONT, 9)
BIG_PRICE_FONT = (FONT, 16, "bold")
MONO_FONT = ("Consolas", 10)

# ---------------- Fixed lists ----------------
PACKAGE_TYPES = ["Freediving", "Domestic", "International"]
PAYMENT_METHODS = ["Pay on Trip", "GCash", "Maya", "Card", "Bank Transfer"]
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DIGITS = "0123456789"

# ---------------- Screen scaling ----------------
# 1.0 on a normal screen, 1.25 when Windows is set to 125%, and so on.
# main.py sets it after the window is made.
SCALE = 1.0


# Change a size in pixels so it matches the Windows scaling
def px(size):
    return int(size * SCALE)


# ---------------- App state ----------------
# The user that is logged in (a dictionary), or None for guests
current_user = None
# main.py puts its show_page function here so every page can switch pages
show_page_function = None


# Remember who is logged in
def log_in_user(user):
    global current_user
    current_user = user


# Forget the logged in user
def log_out_user():
    global current_user
    current_user = None


# Switch to another page (the real work is done by show_page in main.py)
def go_to(page_name, data=None):
    show_page_function(page_name, data)


# ---------------- Files and folders ----------------

# Find a file that is bundled with the app (works inside the .exe too)
def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_folder = sys._MEIPASS
    else:
        base_folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_folder, relative_path)


# The writable folder for the database: %APPDATA%/LakbayPH
def get_data_folder():
    appdata = os.getenv("APPDATA")
    if appdata is None:
        appdata = os.path.expanduser("~")
    folder = os.path.join(appdata, "LakbayPH")
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder


# The writable folder for uploaded package pictures
def get_images_folder():
    folder = os.path.join(get_data_folder(), "images")
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder


# ---------------- Money and text ----------------

# Show a number as pesos, e.g. 28000 -> "₱28,000" and 99.5 -> "₱99.50"
def peso(amount):
    text = format(float(amount), ",.2f")
    if text.endswith(".00"):
        text = text[:-3]
    return "₱" + text


# Read a whole number from text (None if it is not a number)
def read_int(text):
    try:
        return int(str(text).strip())
    except ValueError:
        return None


# Read a number with decimals from text, e.g. "28,000.50" (None if not a number)
def read_float(text):
    try:
        return float(str(text).strip().replace(",", ""))
    except ValueError:
        return None


# Turn an empty string into None (for optional database columns)
def none_if_empty(text):
    text = text.strip()
    if text == "":
        return None
    return text


# Make "3D/2N" from the duration in days and nights
def duration_text(days, nights):
    if nights == 0:
        return str(days) + "D Day Tour"
    return str(days) + "D/" + str(nights) + "N"


# Make star text like "★★★★☆" from a rating
def stars_text(rating):
    full = int(round(rating))
    return "★" * full + "☆" * (5 - full)


# Split "a, b (c, d), e" into ["a", "b (c, d)", "e"].
# Commas inside ( ) are kept. If the text has new lines, split by line.
def split_list_text(text):
    if text is None:
        return []
    if "\n" in text:
        pieces = text.split("\n")
    else:
        pieces = split_by_comma(text)
    items = []
    for piece in pieces:
        if piece.strip() != "":
            items.append(piece.strip())
    return items


# Split text by commas that are not inside parentheses
def split_by_comma(text):
    pieces = []
    current = ""
    depth = 0
    for letter in text:
        if letter == "(":
            depth = depth + 1
        elif letter == ")":
            depth = depth - 1
        if letter == "," and depth <= 0:
            pieces.append(current)
            current = ""
        else:
            current = current + letter
    pieces.append(current)
    return pieces


# ---------------- Validation ----------------

# Check if every letter of the text is a digit 0-9
def only_digits(text):
    if text == "":
        return False
    for letter in text:
        if letter not in DIGITS:
            return False
    return True


# Check the email format: name@domain.com
def is_valid_email(email):
    email = email.strip()
    if email.count("@") != 1 or " " in email:
        return False
    parts = email.split("@")
    name = parts[0]
    domain = parts[1]
    if name == "" or "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    return True


# Remove spaces and dashes from a phone number
def clean_phone(phone):
    return phone.strip().replace(" ", "").replace("-", "")


# Check a PH mobile number: 09XXXXXXXXX or +639XXXXXXXXX
def is_valid_phone(phone):
    phone = clean_phone(phone)
    if phone.startswith("+639"):
        rest = phone[4:]
    elif phone.startswith("09"):
        rest = phone[2:]
    else:
        return False
    return len(rest) == 9 and only_digits(rest)


# Save every phone the same way (09XXXXXXXXX) so duplicates are found
def normalize_phone(phone):
    phone = clean_phone(phone)
    if phone.startswith("+63"):
        phone = "0" + phone[3:]
    return phone


# Password: at least 8 characters with at least one letter and one number
def is_valid_password(password):
    if len(password) < 8:
        return False
    has_letter = False
    has_number = False
    for letter in password:
        if letter.isalpha():
            has_letter = True
        if letter in DIGITS:
            has_number = True
    return has_letter and has_number


# ---------------- Passwords ----------------

# Hash a password with a salt. The result looks like "salt$hash".
def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return salt + "$" + hashed


# Check a typed password against the saved "salt$hash"
def check_password(password, saved_hash):
    if saved_hash is None or "$" not in saved_hash:
        return False
    salt = saved_hash.split("$")[0]
    return hash_password(password, salt) == saved_hash


# ---------------- Price computation ----------------

# Compute the price summary of a booking.
# addons is a list of dictionaries that have "Price" and "Quantity".
def compute_total(price, people, addons, discount_percent):
    base = float(price) * int(people)
    addon_total = 0.0
    for addon in addons:
        addon_total = addon_total + float(addon["Price"]) * int(addon["Quantity"])
    subtotal = base + addon_total
    discount = round(subtotal * float(discount_percent) / 100, 2)
    total = round(subtotal - discount, 2)
    return {"Base": base, "AddOns": addon_total, "Subtotal": subtotal,
            "Discount": discount, "Total": total}


# ---------------- Dates ----------------

# Today's date
def today():
    return datetime.date.today()


# Current date and time as text for the database
def now_text():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# date -> "2026-10-08"
def date_to_text(date_value):
    return date_value.strftime("%Y-%m-%d")


# "2026-10-08" -> date (or None if the text is wrong)
def text_to_date(text):
    try:
        return datetime.datetime.strptime(str(text)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


# "2026-10-08" -> "Oct 08, 2026"
def nice_date(text):
    date_value = text_to_date(text)
    if date_value is None:
        return str(text)
    return date_value.strftime("%b %d, %Y")


# Add a number of days to a date
def add_days(date_value, days):
    return date_value + datetime.timedelta(days=days)


# The same date one year later (Feb 29 becomes Feb 28)
def one_year_from(date_value):
    try:
        return date_value.replace(year=date_value.year + 1)
    except ValueError:
        return date_value.replace(year=date_value.year + 1, day=28)


# Make 3 Spinboxes (month, day, year) and return their variables
def make_date_spinboxes(parent, start_date, bg=WHITE):
    month_var = StringVar()
    day_var = StringVar()
    year_var = StringVar()
    Spinbox(parent, values=MONTH_NAMES, textvariable=month_var, width=5,
            state="readonly", wrap=True, font=NORMAL_FONT).pack(side=LEFT)
    Spinbox(parent, from_=1, to=31, textvariable=day_var, width=3,
            state="readonly", wrap=True, font=NORMAL_FONT).pack(side=LEFT, padx=2)
    Spinbox(parent, from_=2020, to=2040, textvariable=year_var, width=5,
            state="readonly", font=NORMAL_FONT).pack(side=LEFT)
    date_vars = (month_var, day_var, year_var)
    # Set the values after making the Spinboxes (a Spinbox resets them when it is made)
    set_date_spinboxes(date_vars, start_date)
    return date_vars


# Show a date in the 3 Spinboxes
def set_date_spinboxes(date_vars, date_value):
    date_vars[0].set(MONTH_NAMES[date_value.month - 1])
    date_vars[1].set(str(date_value.day))
    date_vars[2].set(str(date_value.year))


# Read the 3 Spinbox variables back into a date (None if not a real date)
def read_date_spinboxes(date_vars):
    try:
        month = MONTH_NAMES.index(date_vars[0].get()) + 1
        return datetime.date(int(date_vars[2].get()), month, int(date_vars[1].get()))
    except ValueError:
        return None


# ---------------- Images ----------------

# Pictures already loaded, so we do not load them again (and Tkinter keeps them)
image_cache = {}


# Find the picture file: uploaded folder first, then bundled assets, else placeholder
def find_image_path(file_name):
    if file_name:
        uploaded = os.path.join(get_images_folder(), file_name)
        if os.path.exists(uploaded):
            return uploaded
        bundled = resource_path(os.path.join("assets", "images", file_name))
        if os.path.exists(bundled):
            return bundled
    return resource_path(os.path.join("assets", "placeholder.jpg"))


# Load a picture, crop it to the size we want, and return a Tkinter image
def load_image(file_name, width, height, dark=False):
    key = (file_name, width, height, dark)
    if key in image_cache:
        return image_cache[key]
    try:
        picture = Image.open(find_image_path(file_name)).convert("RGB")
        picture = ImageOps.fit(picture, (width, height))
    except Exception:
        picture = Image.new("RGB", (width, height), TEAL)
    if dark:
        picture = ImageEnhance.Brightness(picture).enhance(0.55)
    photo = ImageTk.PhotoImage(picture)
    image_cache[key] = photo
    return photo


# Forget loaded pictures (after an admin uploads new ones)
def clear_image_cache():
    image_cache.clear()


# Load the round LakbayPH logo (keeps its see-through corners)
def load_logo(size):
    key = ("logo", size)
    if key in image_cache:
        return image_cache[key]
    try:
        picture = Image.open(resource_path(os.path.join("assets", "logo.png"))).convert("RGBA")
        picture = picture.resize((size, size), Image.LANCZOS)
    except Exception:
        picture = Image.new("RGBA", (size, size), TEAL)
    photo = ImageTk.PhotoImage(picture)
    image_cache[key] = photo
    return photo


# ---------------- Window and widget tools ----------------

# Put a window in the middle of the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 3
    window.geometry(str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y))


# A flat teal button
def teal_button(parent, text, command, width=None):
    button = Button(parent, text=text, command=command, bg=TEAL, fg=WHITE,
                    activebackground=DARK_TEAL, activeforeground=WHITE,
                    relief=FLAT, font=BOLD_FONT, cursor="hand2", padx=14, pady=5)
    if width is not None:
        button.config(width=width)
    return button


# A white button with teal text
def light_button(parent, text, command, width=None):
    button = Button(parent, text=text, command=command, bg=WHITE, fg=DARK_TEAL,
                    activebackground=LIGHT_TEAL, relief=SOLID, bd=1,
                    font=BOLD_FONT, cursor="hand2", padx=12, pady=4)
    if width is not None:
        button.config(width=width)
    return button


# A label with the usual font and white background
def text_label(parent, text, font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE, wrap=0):
    return Label(parent, text=text, font=font, fg=fg, bg=bg,
                 wraplength=wrap, justify=LEFT, anchor="w")


# A label on top and an Entry under it (for forms). Returns the Entry.
def form_entry(parent, label_text, variable, secret=False, width=34, bg=WHITE):
    Label(parent, text=label_text, font=BOLD_FONT, fg=DARK_TEAL, bg=bg, anchor="w").pack(fill=X, pady=(8, 2))
    entry = Entry(parent, textvariable=variable, width=width, font=NORMAL_FONT,
                  relief=SOLID, bd=1)
    if secret:
        entry.config(show="*")
    entry.pack(fill=X, ipady=4)
    return entry


# A Menubutton that lets you pick one choice from a list
def make_choice_menu(parent, variable, choices, command=None, width=22):
    button = Menubutton(parent, textvariable=variable, relief=SOLID, bd=1, bg=WHITE,
                        fg=DARK_TEAL, font=NORMAL_FONT, width=width, anchor="w",
                        indicatoron=True, cursor="hand2", padx=6, pady=3)
    menu = Menu(button, tearoff=0)
    for choice in choices:
        menu.add_radiobutton(label=choice, value=choice, variable=variable, command=command)
    button["menu"] = menu
    return button


# A LabelFrame with the LakbayPH look
def make_box(parent, title, bg=WHITE):
    return LabelFrame(parent, text="  " + title + "  ", font=BOLD_FONT, fg=DARK_TEAL, bg=bg,
                      padx=px(14), pady=px(10), relief=GROOVE, bd=2)


# Show a friendly error box
def show_error(message, error=None):
    if error is not None:
        message = message + "\n\nDetails: " + str(error)
    messagebox.showerror("LakbayPH", message)


# ---------------- Scrolling pages ----------------

# The canvas of the page that is shown now (the mouse wheel scrolls it)
scroll_canvas = None


# Make a page that scrolls. Returns the frame where you put the widgets.
def make_scroll_area(parent, bg=WHITE):
    global scroll_canvas
    canvas = Canvas(parent, bg=bg, highlightthickness=0, yscrollincrement=20)
    scrollbar = Scrollbar(parent, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    inner = Frame(canvas, bg=bg)
    canvas.create_window(0, 0, window=inner, anchor="nw", tags="inner")
    # Update the scroll size when the content or the window changes
    inner.bind("<Configure>", on_inner_resize)
    canvas.bind("<Configure>", on_canvas_resize)
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    scroll_canvas = canvas
    return inner


# The content changed size: update the scroll region
def on_inner_resize(event):
    canvas = event.widget.master
    canvas.configure(scrollregion=canvas.bbox("all"))


# The window changed size: make the content as wide as the canvas
def on_canvas_resize(event):
    event.widget.itemconfig("inner", width=event.width)


# Scroll the page with the mouse wheel
def on_mouse_wheel(event):
    if scroll_canvas is None or not scroll_canvas.winfo_exists():
        return
    try:
        # Listboxes and Text boxes scroll by themselves
        if event.widget.winfo_class() in ("Listbox", "Text"):
            return
        if event.widget.winfo_toplevel() != scroll_canvas.winfo_toplevel():
            return
    except Exception:
        return
    if scroll_canvas.yview() == (0.0, 1.0):
        return
    scroll_canvas.yview_scroll(int(-event.delta / 120) * 3, "units")
