# user_pages.py - the pages that customers see:
# home, destinations, package details, log in / sign up, booking,
# my bookings, profile, contact and blog.

import random
from tkinter import *
from tkinter import messagebox, filedialog
import helpers
import database
from helpers import *

# The page to open after logging in, e.g. ("booking", {"package_id": 5})
after_login = None

# The booking that is being made right now (filled in step by step)
booking = {}

# Widgets of the current booking step, form or page
step_vars = {}
search = {}
filters = {}
login_form = {}
signup_form = {}
profile_form = {}
review_form = {}
slot_check = {}

# Hero banner
hero_canvas = None
hero_button = None
hero_packages = []
hero_index = 0
hero_timer = None
HERO_WIDTH = 1060
HERO_HEIGHT = 430

# Destinations page
results_frame = None
search_info = {"date": None, "people": 1}
MAX_PRICE = 150000

# My Bookings tab: "Upcoming", "Completed" or "Cancelled"
my_bookings_tab = "Upcoming"

STATUS_COLORS = {"Pending": GOLD, "Confirmed": GREEN, "Completed": DARK_TEAL, "Cancelled": RED}
STEP_NAMES = ["Date & People", "Add-ons", "Discount", "Summary & Payment"]


# ======================= Top bar =======================

# Build the top bar: logo, links, and the log in buttons (or the user's name)
def build_top_bar(window, page_name):
    bar = Frame(window, bg=WHITE)
    bar.pack(side=TOP, fill=X)
    Frame(window, bg=BORDER, height=1).pack(side=TOP, fill=X)
    inner = Frame(bar, bg=WHITE)
    inner.pack(fill=X, padx=px(24), pady=px(8))

    # Logo and name (click to go home)
    logo = Label(inner, image=load_logo(px(38)), bg=WHITE, cursor="hand2")
    logo.pack(side=LEFT)
    name = Label(inner, text="LakbayPH", font=(FONT, 17, "bold"), fg=DARK_TEAL, bg=WHITE, cursor="hand2")
    name.pack(side=LEFT, padx=(px(6), px(30)))
    logo.bind("<Button-1>", on_logo_click)
    name.bind("<Button-1>", on_logo_click)

    # Page links
    links = [("Home", "home"), ("Destinations", "destinations"), ("Contact Us", "contact"), ("Blog", "blog")]
    for link in links:
        make_nav_link(inner, link[0], link[1], page_name).pack(side=LEFT, padx=px(4))

    build_user_buttons(inner, page_name)


# Clicking the logo goes to the home page
def on_logo_click(event):
    helpers.go_to("home")


# A flat link in the top bar (teal when it is the open page)
def make_nav_link(parent, text, target_page, page_name):
    color = DARK_TEAL
    if target_page == page_name:
        color = TEAL
    return Button(parent, text=text, font=(FONT, 11, "bold"), fg=color, bg=WHITE, relief=FLAT,
                  activebackground=WHITE, activeforeground=TEAL, cursor="hand2", bd=0,
                  command=lambda: helpers.go_to(target_page))


# Right side of the top bar: Sign Up / Log In, or the user's menu
def build_user_buttons(parent, page_name):
    user = helpers.current_user
    if user is None:
        teal_button(parent, "Log In", go_to_login).pack(side=RIGHT)
        make_nav_link(parent, "Sign Up", "signup", page_name).pack(side=RIGHT, padx=px(10))
        return
    light_button(parent, "Log Out", log_out).pack(side=RIGHT)
    if user["Role"] == "Admin":
        teal_button(parent, "Admin Panel", go_to_admin).pack(side=RIGHT, padx=px(8))
    make_nav_link(parent, "My Bookings", "my_bookings", page_name).pack(side=RIGHT, padx=px(6))

    # The user's name opens a small menu
    menu_button = Menubutton(parent, text="Hi, " + user["FirstName"] + " ▾", font=(FONT, 11, "bold"),
                             fg=TEAL, bg=WHITE, activebackground=WHITE, cursor="hand2", relief=FLAT)
    menu = Menu(menu_button, tearoff=0)
    menu.add_command(label="My Profile", command=go_to_profile)
    menu.add_command(label="My Bookings", command=go_to_my_bookings)
    menu.add_separator()
    menu.add_command(label="Log Out", command=log_out)
    menu_button["menu"] = menu
    menu_button.pack(side=RIGHT, padx=px(6))


# Open the log in page
def go_to_login():
    helpers.go_to("login")


# Open the admin panel
def go_to_admin():
    helpers.go_to("admin_dashboard")


# Open the profile page
def go_to_profile():
    helpers.go_to("profile")


# Open the My Bookings page
def go_to_my_bookings():
    helpers.go_to("my_bookings")


# Open the destinations page
def go_to_destinations():
    helpers.go_to("destinations")


# Log out and go back to the home page
def log_out():
    global after_login
    helpers.log_out_user()
    booking.clear()
    after_login = None
    helpers.go_to("home")


# ======================= Shared widgets =======================

# A big centered title with a small teal line under it
def add_section_title(parent, title, subtitle=""):
    box = Frame(parent, bg=WHITE)
    box.pack(pady=(px(30), px(12)))
    Label(box, text=title, font=(FONT, 20, "bold"), fg=DARK_TEAL, bg=WHITE).pack()
    if subtitle != "":
        Label(box, text=subtitle, font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack()
    Frame(box, bg=TEAL, width=px(60), height=3).pack(pady=px(6))


# One package card: photo, title, location, duration, type, stars, price, button
def make_package_card(parent, package):
    card = Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    photo = load_image(package["ImageFileName"], px(240), px(150))
    Label(card, image=photo, bg=WHITE).pack()
    body = Frame(card, bg=WHITE, padx=px(10), pady=px(8))
    body.pack(fill=BOTH, expand=True)
    Label(body, text=package["Title"], font=(FONT, 11, "bold"), fg=DARK_TEAL, bg=WHITE,
          wraplength=px(220), justify=LEFT, anchor="nw", height=2).pack(fill=X)
    Label(body, text=str(package["Location"]), font=SMALL_FONT, fg=GRAY, bg=WHITE,
          anchor="w", wraplength=px(220), justify=LEFT).pack(fill=X)
    info = duration_text(package["Duration"], package["DurationNights"]) + "   |   " + package["PackageType"]
    Label(body, text=info, font=SMALL_FONT, fg=DARK_TEAL, bg=WHITE, anchor="w").pack(fill=X, pady=(px(4), 0))
    Label(body, text=rating_text(package), font=SMALL_FONT, fg=GOLD, bg=WHITE, anchor="w").pack(fill=X)
    price_row = Frame(body, bg=WHITE)
    price_row.pack(fill=X, pady=(px(4), px(6)))
    Label(price_row, text=peso(package["Price"]), font=(FONT, 13, "bold"), fg=TEAL, bg=WHITE).pack(side=LEFT)
    Label(price_row, text=" / person", font=SMALL_FONT, fg=GRAY, bg=WHITE).pack(side=LEFT, pady=(px(4), 0))
    teal_button(body, "View Details", lambda: helpers.go_to("details", package["PackageID"])).pack(fill=X)
    return card


# "★★★★☆ 4.2 (5)" or "No reviews yet"
def rating_text(package):
    if package["ReviewCount"] == 0:
        return "☆☆☆☆☆  No reviews yet"
    return stars_text(package["AvgRating"]) + "  " + str(package["AvgRating"]) + " (" + str(package["ReviewCount"]) + ")"


# Show package cards in rows of 4
def show_card_grid(parent, packages, columns=4):
    grid = Frame(parent, bg=WHITE)
    grid.pack(pady=px(6))
    number = 0
    for package in packages:
        card = make_package_card(grid, package)
        card.grid(row=number // columns, column=number % columns, padx=px(8), pady=px(8), sticky="nsew")
        number = number + 1
    return grid


# The dark footer at the bottom of the user pages
def build_footer(parent):
    footer = Frame(parent, bg=DEEP_TEAL, pady=px(26))
    footer.pack(fill=X, pady=(px(40), 0))
    columns = Frame(footer, bg=DEEP_TEAL)
    columns.pack()
    about = Frame(columns, bg=DEEP_TEAL)
    about.grid(row=0, column=0, sticky="n", padx=px(40))
    Label(about, text="LakbayPH", font=(FONT, 15, "bold"), fg=TEAL, bg=DEEP_TEAL).pack(anchor="w")
    Label(about, text="Your travel partner for freediving, domestic\nand international tours.",
          font=SMALL_FONT, fg=WHITE, bg=DEEP_TEAL, justify=LEFT).pack(anchor="w")
    links = Frame(columns, bg=DEEP_TEAL)
    links.grid(row=0, column=1, sticky="n", padx=px(40))
    Label(links, text="Quick Links", font=BOLD_FONT, fg=TEAL, bg=DEEP_TEAL).pack(anchor="w")
    for link in [("Home", "home"), ("Destinations", "destinations"), ("Contact Us", "contact"), ("Blog", "blog")]:
        make_footer_link(links, link[0], link[1]).pack(anchor="w")
    contact = Frame(columns, bg=DEEP_TEAL)
    contact.grid(row=0, column=2, sticky="n", padx=px(40))
    Label(contact, text="Contact", font=BOLD_FONT, fg=TEAL, bg=DEEP_TEAL).pack(anchor="w")
    for line in ["hello@lakbayph.com", "+63 917 000 0000", "Batangas City, Philippines"]:
        Label(contact, text=line, font=SMALL_FONT, fg=WHITE, bg=DEEP_TEAL).pack(anchor="w")
    Label(footer, text="© 2026 LakbayPH - Travel Services. All rights reserved.",
          font=SMALL_FONT, fg="#8FB5BC", bg=DEEP_TEAL).pack(pady=(px(18), 0))


# A small white link in the footer
def make_footer_link(parent, text, target_page):
    return Button(parent, text=text, font=SMALL_FONT, fg=WHITE, bg=DEEP_TEAL, relief=FLAT, bd=0,
                  activebackground=DEEP_TEAL, activeforeground=TEAL, cursor="hand2",
                  command=lambda: helpers.go_to(target_page))


# ======================= Home page =======================

# The home page: hero, search bar, most booked, recently added, categories, reviews
def show_home_page(parent, data):
    page = make_scroll_area(parent)
    build_hero(page)
    build_search_bar(page)
    add_section_title(page, "Most Booked", "Our travelers' favorite trips")
    show_card_grid(page, database.get_most_booked(4))
    add_section_title(page, "Recently Added", "Fresh trips you can book now")
    show_card_grid(page, database.get_recent_packages(4))
    build_category_buttons(page)
    build_home_reviews(page)
    build_footer(page)


# The big photo banner with text, thumbnails and dots
def build_hero(parent):
    global hero_canvas, hero_button, hero_packages, hero_index
    stop_hero_timer()
    hero_packages = database.get_most_booked(4)
    hero_index = 0
    hero_canvas = Canvas(parent, width=px(HERO_WIDTH), height=px(HERO_HEIGHT),
                         highlightthickness=0, bg=DEEP_TEAL)
    hero_canvas.pack()
    hero_button = Button(hero_canvas, text="FIND OUT MORE", command=open_hero_package, bg=TEAL, fg=WHITE,
                         relief=FLAT, font=(FONT, 11, "bold"), padx=px(22), pady=px(8), cursor="hand2",
                         activebackground=WHITE, activeforeground=DARK_TEAL)
    # Clicking a thumbnail or a dot changes the photo
    hero_canvas.tag_bind("pick", "<Button-1>", on_hero_pick)
    if len(hero_packages) > 0:
        draw_hero()
        start_hero_timer()


# Draw everything on the hero canvas for the current photo
def draw_hero():
    hero_canvas.delete("all")
    package = hero_packages[hero_index]
    photo = load_image(package["ImageFileName"], px(HERO_WIDTH), px(HERO_HEIGHT), dark=True)
    hero_canvas.create_image(0, 0, image=photo, anchor="nw")
    draw_social_column()
    draw_hero_text(package)
    draw_hero_thumbnails()
    draw_hero_dots()


# The thin column of social icons on the left
def draw_social_column():
    hero_canvas.create_rectangle(0, 0, px(52), px(HERO_HEIGHT), fill=DEEP_TEAL, outline="")
    hero_canvas.create_text(px(26), px(70), text="FOLLOW US", angle=90, fill=WHITE, font=(FONT, 8, "bold"))
    hero_canvas.create_line(px(26), px(125), px(26), px(165), fill=TEAL, width=2)
    y = px(200)
    for icon in ["f", "ig", "X", "▶"]:
        hero_canvas.create_oval(px(12), y - px(14), px(40), y + px(14), outline=WHITE)
        hero_canvas.create_text(px(26), y, text=icon, fill=WHITE, font=(FONT, 9, "bold"))
        y = y + px(44)


# "Say yes TO YOUR VACATION", the package name and the button
def draw_hero_text(package):
    left = px(110)
    hero_canvas.create_text(left, px(115), text="Say yes", font=("Segoe Script", 40), fill=WHITE, anchor="w")
    hero_canvas.create_text(left, px(190), text="TO YOUR VACATION", font=(FONT, 38, "bold"),
                            fill=WHITE, anchor="w")
    hero_canvas.create_text(left, px(245), text=package["Title"] + "   •   " + str(package["Location"]),
                            font=(FONT, 13, "bold"), fill=TEAL, anchor="w")
    hero_canvas.create_text(left, px(275), text="From " + peso(package["Price"]) + " / person   •   " +
                            duration_text(package["Duration"], package["DurationNights"]),
                            font=(FONT, 12), fill=WHITE, anchor="w")
    hero_canvas.create_window(left, px(335), window=hero_button, anchor="w")


# The 4 small photos on the right
def draw_hero_thumbnails():
    x = px(HERO_WIDTH - 172)
    y = px(48)
    number = 0
    for package in hero_packages:
        photo = load_image(package["ImageFileName"], px(140), px(78))
        hero_canvas.create_image(x, y, image=photo, anchor="nw", tags=("pick", "pick_" + str(number)))
        if number == hero_index:
            hero_canvas.create_rectangle(x - 3, y - 3, x + px(140) + 2, y + px(78) + 2, outline=TEAL, width=3)
        y = y + px(88)
        number = number + 1


# The dots at the bottom (the teal one is the current photo)
def draw_hero_dots():
    x = px(HERO_WIDTH) // 2 - (len(hero_packages) - 1) * px(11)
    y = px(HERO_HEIGHT - 24)
    for number in range(len(hero_packages)):
        color = WHITE
        if number == hero_index:
            color = TEAL
        hero_canvas.create_oval(x - px(6), y - px(6), x + px(6), y + px(6), fill=color, outline=WHITE,
                                tags=("pick", "pick_" + str(number)))
        x = x + px(22)


# A thumbnail or a dot was clicked: show that photo
def on_hero_pick(event):
    global hero_index
    for tag in hero_canvas.gettags("current"):
        if tag.startswith("pick_"):
            hero_index = int(tag[5:])
    draw_hero()


# Change the photo every 5 seconds
def start_hero_timer():
    global hero_timer
    hero_timer = hero_canvas.after(5000, next_hero_photo)


# Stop the old timer (when the home page is made again)
def stop_hero_timer():
    global hero_timer
    if hero_timer is not None:
        try:
            hero_canvas.after_cancel(hero_timer)
        except Exception:
            pass
        hero_timer = None


# Show the next photo (stops when the home page is closed)
def next_hero_photo():
    global hero_index
    if hero_canvas is None or not hero_canvas.winfo_exists():
        return
    hero_index = (hero_index + 1) % len(hero_packages)
    draw_hero()
    start_hero_timer()


# FIND OUT MORE opens the package in the banner
def open_hero_package():
    helpers.go_to("details", hero_packages[hero_index]["PackageID"])


# The search bar under the hero
def build_search_bar(parent):
    box = Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1, padx=px(16), pady=px(12))
    box.pack(pady=(px(16), 0))
    search["keyword"] = StringVar()
    search["type"] = StringVar(value="All")
    search["people"] = StringVar(value="1")
    add_search_label(box, "Destination", 0)
    keyword_entry = Entry(box, textvariable=search["keyword"], width=20, font=NORMAL_FONT, relief=SOLID, bd=1)
    keyword_entry.grid(row=1, column=0, padx=px(8), ipady=3)
    keyword_entry.bind("<Return>", on_search_enter)
    add_search_label(box, "Package Type", 1)
    types = Frame(box, bg=WHITE)
    types.grid(row=1, column=1, padx=px(8))
    for name in ["All"] + PACKAGE_TYPES:
        Radiobutton(types, text=name, value=name, variable=search["type"], bg=WHITE, fg=DARK_TEAL,
                    activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT)
    add_search_label(box, "Travel Date", 2)
    date_box = Frame(box, bg=WHITE)
    date_box.grid(row=1, column=2, padx=px(8))
    search["date"] = make_date_spinboxes(date_box, helpers.today())
    add_search_label(box, "People", 3)
    Spinbox(box, from_=1, to=50, textvariable=search["people"], width=4, font=NORMAL_FONT).grid(row=1, column=3, padx=px(8))
    teal_button(box, "SEARCH", run_search).grid(row=0, column=4, rowspan=2, padx=(px(10), 0), sticky="ns")


# A small gray label above a search field
def add_search_label(parent, text, column):
    Label(parent, text=text, font=SMALL_FONT, fg=GRAY, bg=WHITE).grid(row=0, column=column, sticky="w", padx=px(8))


# Pressing Enter in the search box also searches
def on_search_enter(event):
    run_search()


# Read the search bar and open the destinations page with the results
def run_search():
    travel_date = read_date_spinboxes(search["date"])
    if travel_date is None:
        messagebox.showwarning("Search", "Please choose a real date.")
        return
    if travel_date < helpers.today():
        messagebox.showwarning("Search", "The travel date cannot be in the past.")
        return
    people = read_int(search["people"].get())
    if people is None or people < 1:
        messagebox.showwarning("Search", "Please enter how many people are going (1 or more).")
        return
    helpers.go_to("destinations", {"keyword": search["keyword"].get().strip(), "type": search["type"].get(),
                                   "date": travel_date, "people": people})


# Buttons for every tour category, grouped by package type
def build_category_buttons(parent):
    add_section_title(parent, "Browse by Category", "Pick the kind of trip you like")
    box = Frame(parent, bg=WHITE)
    box.pack()
    categories = database.get_categories()
    row_number = 0
    for package_type in PACKAGE_TYPES:
        Label(box, text=package_type, font=BOLD_FONT, fg=TEAL, bg=WHITE, width=12,
              anchor="e").grid(row=row_number, column=0, padx=px(6), pady=px(4))
        column = 1
        for category in categories:
            if category["CategoryType"] == package_type:
                make_category_button(box, category).grid(row=row_number, column=column, padx=px(4),
                                                         pady=px(4), sticky="ew")
                column = column + 1
        row_number = row_number + 1


# One category button (opens destinations filtered by that category)
def make_category_button(parent, category):
    return light_button(parent, category["CategoryName"],
                        lambda: helpers.go_to("destinations", {"category": category["CategoryName"]}))


# The newest reviews from travelers
def build_home_reviews(parent):
    add_section_title(parent, "What Travelers Say", "Reviews from our customers")
    reviews = database.get_latest_reviews(3)
    if len(reviews) == 0:
        Label(parent, text="No reviews yet. Book a trip and be the first to share your experience!",
              font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack()
        return
    row = Frame(parent, bg=WHITE)
    row.pack()
    for review in reviews:
        make_review_card(row, review).pack(side=LEFT, padx=px(8), anchor="n")


# One review card for the home page
def make_review_card(parent, review):
    card = Frame(parent, bg=LIGHT_TEAL, padx=px(16), pady=px(14))
    Label(card, text=stars_text(review["Rating"]), font=(FONT, 14), fg=GOLD, bg=LIGHT_TEAL).pack(anchor="w")
    comment = review["Comment"]
    if comment is None or comment.strip() == "":
        comment = "(No comment)"
    Label(card, text="\"" + comment + "\"", font=NORMAL_FONT, fg=DARK_TEAL, bg=LIGHT_TEAL,
          wraplength=px(290), justify=LEFT, width=36, anchor="w").pack(anchor="w", pady=px(6))
    Label(card, text=review["FirstName"] + " " + review["LastName"][:1] + ".  •  " + str(review["Title"]),
          font=SMALL_FONT, fg=GRAY, bg=LIGHT_TEAL, wraplength=px(290), justify=LEFT).pack(anchor="w")
    return card


# ======================= Contact Us and Blog =======================

# A simple contact page with our details and a message form
def show_contact_page(parent, data):
    page = make_scroll_area(parent)
    add_section_title(page, "Contact Us", "We usually reply within one day")
    columns = Frame(page, bg=WHITE)
    columns.pack(pady=px(10))
    info = make_box(columns, "Our Office")
    info.grid(row=0, column=0, sticky="n", padx=px(12))
    for line in ["LakbayPH - Travel Services", "Batangas City, Philippines", "",
                 "Email: hello@lakbayph.com", "Phone: +63 917 000 0000", "", "Open Monday to Saturday, 8 AM - 6 PM"]:
        text_label(info, line).pack(anchor="w")
    form = make_box(columns, "Send us a message")
    form.grid(row=0, column=1, sticky="n", padx=px(12))
    step_vars.clear()
    step_vars["name"] = StringVar()
    step_vars["email"] = StringVar()
    form_entry(form, "Your name", step_vars["name"])
    form_entry(form, "Your email or phone", step_vars["email"])
    Label(form, text="Message", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w", pady=(8, 2))
    step_vars["message"] = Text(form, width=40, height=6, font=NORMAL_FONT, relief=SOLID, bd=1, wrap=WORD)
    step_vars["message"].pack()
    teal_button(form, "Send Message", send_contact_message).pack(fill=X, pady=(px(10), 0))
    build_footer(page)


# Check the contact form and thank the user
def send_contact_message():
    message = step_vars["message"].get("1.0", END).strip()
    if step_vars["name"].get().strip() == "" or step_vars["email"].get().strip() == "" or message == "":
        messagebox.showwarning("Contact Us", "Please fill in your name, email or phone, and message.")
        return
    messagebox.showinfo("Contact Us", "Thank you, " + step_vars["name"].get().strip() + "! We got your message.")
    helpers.go_to("contact")


# A few travel tips for the blog page
BLOG_POSTS = [
    ("5 Tips for Your First Freediving Trip", "fdbasic.jpg",
     "Relax and breathe slowly before every dive. Never dive alone, always listen to your instructor, "
     "and drink plenty of water. Start with a day tour before trying a multi-day course."),
    ("Island Hopping in Palawan on a Budget", "dompalawan.jpg",
     "Travel during the shoulder months, join group tours, and bring your own snorkel and dry bag. "
     "Book your Underground River permit early because slots run out quickly."),
    ("First Time in Japan? Read This", "inttokyo.png",
     "Get a JR Pass before you fly, carry some cash, and learn a few polite words like arigatou. "
     "Trains are always on time, so plan your days around the train schedule."),
]


# The blog page with short travel articles
def show_blog_page(parent, data):
    page = make_scroll_area(parent)
    add_section_title(page, "LakbayPH Blog", "Travel tips and stories")
    for post in BLOG_POSTS:
        card = Frame(page, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        card.pack(pady=px(8))
        Label(card, image=load_image(post[1], px(280), px(170)), bg=WHITE).pack(side=LEFT)
        body = Frame(card, bg=WHITE, padx=px(18), pady=px(14))
        body.pack(side=LEFT, fill=BOTH)
        Label(body, text=post[0], font=HEADING_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
        Label(body, text="By the LakbayPH Team", font=SMALL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w")
        Label(body, text=post[2], font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE, wraplength=px(520),
              justify=LEFT).pack(anchor="w", pady=px(8))
        light_button(body, "See trips", go_to_destinations).pack(anchor="w")
    build_footer(page)


# ======================= Destinations =======================

# All active packages with filters and sorting
def show_destinations_page(parent, data):
    global results_frame
    page = make_scroll_area(parent)
    add_section_title(page, "Destinations", "Find your next adventure")
    make_filter_vars(data)
    build_filter_panel(page)
    results_frame = Frame(page, bg=WHITE)
    results_frame.pack(fill=X)
    apply_filters()
    build_footer(page)


# Make the filter variables (and fill them from the search bar or category button)
def make_filter_vars(data):
    filters["keyword"] = StringVar(value="")
    filters["type"] = StringVar(value="All")
    filters["category"] = StringVar(value="All Categories")
    filters["sort"] = StringVar(value="Newest")
    filters["min"] = IntVar(value=0)
    filters["max"] = IntVar(value=MAX_PRICE)
    search_info["date"] = None
    search_info["people"] = 1
    if data is None:
        return
    if "keyword" in data:
        filters["keyword"].set(data["keyword"])
    if "type" in data:
        filters["type"].set(data["type"])
    if "category" in data:
        filters["category"].set(data["category"])
    if "date" in data:
        search_info["date"] = data["date"]
        search_info["people"] = data["people"]


# The box with all the filter widgets
def build_filter_panel(parent):
    box = make_box(parent, "Filter packages")
    box.pack(padx=px(40), fill=X)
    row1 = Frame(box, bg=WHITE)
    row1.pack(fill=X, pady=px(4))
    Label(row1, text="Keyword:", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    keyword_entry = Entry(row1, textvariable=filters["keyword"], width=24, font=NORMAL_FONT, relief=SOLID, bd=1)
    keyword_entry.pack(side=LEFT, padx=(px(6), px(24)), ipady=2)
    keyword_entry.bind("<Return>", on_filter_enter)
    Label(row1, text="Type:", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    for name in ["All"] + PACKAGE_TYPES:
        Radiobutton(row1, text=name, value=name, variable=filters["type"], command=apply_filters,
                    bg=WHITE, fg=DARK_TEAL, activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT)
    build_filter_row_2(box)


# Second row: category, sort, price range and the buttons
def build_filter_row_2(box):
    row2 = Frame(box, bg=WHITE)
    row2.pack(fill=X, pady=px(4))
    category_names = ["All Categories"]
    for category in database.get_categories():
        category_names.append(category["CategoryName"])
    Label(row2, text="Category:", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    make_choice_menu(row2, filters["category"], category_names, apply_filters, 20).pack(side=LEFT, padx=(px(6), px(18)))
    Label(row2, text="Sort by:", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    make_choice_menu(row2, filters["sort"], list(database.SORT_OPTIONS.keys()), apply_filters, 17).pack(side=LEFT, padx=(px(6), px(18)))
    row3 = Frame(box, bg=WHITE)
    row3.pack(fill=X, pady=px(4))
    Label(row3, text="Price from ₱", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    Scale(row3, from_=0, to=MAX_PRICE, resolution=5000, orient=HORIZONTAL, variable=filters["min"],
          length=px(220), bg=WHITE, highlightthickness=0, font=SMALL_FONT).pack(side=LEFT)
    Label(row3, text="  to ₱", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    Scale(row3, from_=0, to=MAX_PRICE, resolution=5000, orient=HORIZONTAL, variable=filters["max"],
          length=px(220), bg=WHITE, highlightthickness=0, font=SMALL_FONT).pack(side=LEFT)
    light_button(row3, "Reset", reset_filters).pack(side=RIGHT)
    teal_button(row3, "Apply", apply_filters).pack(side=RIGHT, padx=px(6))


# Pressing Enter in the keyword box applies the filters
def on_filter_enter(event):
    apply_filters()


# Put every filter back to the start
def reset_filters():
    filters["keyword"].set("")
    filters["type"].set("All")
    filters["category"].set("All Categories")
    filters["sort"].set("Newest")
    filters["min"].set(0)
    filters["max"].set(MAX_PRICE)
    search_info["date"] = None
    apply_filters()


# Show only the packages that match the filters
def apply_filters():
    for widget in results_frame.winfo_children():
        widget.destroy()
    try:
        packages = database.get_active_packages(filters["sort"].get())
        matches = []
        for package in packages:
            if package_matches(package) and package_is_available(package):
                matches.append(package)
    except Exception as error:
        show_error("Could not load the packages.", error)
        return
    show_results_header(len(matches))
    if len(matches) == 0:
        Label(results_frame, text="No packages match your filters. Try changing them.",
              font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(pady=px(30))
        return
    show_card_grid(results_frame, matches)


# Check one package against the keyword, type, category and price filters
def package_matches(package):
    keyword = filters["keyword"].get().strip().lower()
    if keyword != "":
        words = package["Title"] + " " + str(package["Location"]) + " " + package["PackageType"] + " "
        words = words + str(package["CategoryName"]) + " " + package["Description"]
        if keyword not in words.lower():
            return False
    if filters["type"].get() != "All" and package["PackageType"] != filters["type"].get():
        return False
    if filters["category"].get() != "All Categories" and package["CategoryName"] != filters["category"].get():
        return False
    if package["Price"] < filters["min"].get() or package["Price"] > filters["max"].get():
        return False
    return True


# When a date was searched: is the package open that day with enough slots?
def package_is_available(package):
    travel_date = search_info["date"]
    if travel_date is None:
        return True
    if check_travel_date(package, travel_date) != "":
        return False
    slots = database.get_slots_left(package["PackageID"], date_to_text(travel_date))
    return slots >= search_info["people"]


# "12 packages found" and the searched date (with a button to clear it)
def show_results_header(count):
    header = Frame(results_frame, bg=WHITE)
    header.pack(fill=X, padx=px(48), pady=(px(14), 0))
    text = str(count) + " package(s) found"
    if search_info["date"] is not None:
        text = text + " for " + str(search_info["people"]) + " people on " + search_info["date"].strftime("%b %d, %Y")
    Label(header, text=text, font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    if search_info["date"] is not None:
        light_button(header, "Show all dates", clear_search_date).pack(side=LEFT, padx=px(10))


# Stop filtering by the searched date
def clear_search_date():
    search_info["date"] = None
    apply_filters()


# Check a travel date for a package. Returns "" if OK, or the problem.
def check_travel_date(package, travel_date):
    if travel_date is None:
        return "Please choose a real date."
    if travel_date < helpers.today():
        return "The travel date cannot be in the past."
    start = text_to_date(package["StartDate"])
    end = text_to_date(package["EndDate"])
    if travel_date < start or travel_date > end:
        return "This package is only available from " + nice_date(package["StartDate"]) + " to " + nice_date(package["EndDate"]) + "."
    return ""


# The first date that can be booked (today, or the start date if later)
def first_travel_date(package):
    start = text_to_date(package["StartDate"])
    if start is None or start < helpers.today():
        return helpers.today()
    return start


# ======================= Package details =======================

# The full page of one package
def show_details_page(parent, package_id):
    package = database.get_package(package_id)
    if package is None or package["IsActive"] != 1:
        messagebox.showwarning("LakbayPH", "Sorry, this package is not available.")
        helpers.go_to("destinations")
        return
    page = make_scroll_area(parent)
    build_details_top(page, package)
    build_details_lists(page, package)
    build_details_addons(page, package)
    build_slots_checker(page, package)
    build_details_reviews(page, package)
    build_footer(page)


# Big photo on the left, main info and Book Now on the right
def build_details_top(page, package):
    top = Frame(page, bg=WHITE)
    top.pack(pady=px(20))
    Label(top, image=load_image(package["ImageFileName"], px(620), px(390)), bg=WHITE).grid(row=0, column=0, sticky="n")
    info = Frame(top, bg=LIGHT_TEAL, padx=px(22), pady=px(18))
    info.grid(row=0, column=1, sticky="nsew", padx=(px(18), 0))
    Label(info, text=package["PackageType"].upper() + "  •  " + str(package["CategoryName"]),
          font=(FONT, 9, "bold"), fg=TEAL, bg=LIGHT_TEAL).pack(anchor="w")
    Label(info, text=package["Title"], font=(FONT, 18, "bold"), fg=DARK_TEAL, bg=LIGHT_TEAL,
          wraplength=px(360), justify=LEFT).pack(anchor="w", pady=(px(4), px(6)))
    add_info_line(info, "Location", str(package["Location"]))
    add_info_line(info, "Duration", duration_text(package["Duration"], package["DurationNights"]))
    add_info_line(info, "Ideal for", str(package["IdealFor"]))
    add_info_line(info, "Slots", str(package["MaxSlots"]) + " people per travel date")
    Label(info, text=rating_text(package), font=NORMAL_FONT, fg=GOLD, bg=LIGHT_TEAL).pack(anchor="w", pady=px(6))
    Label(info, text=peso(package["Price"]), font=(FONT, 22, "bold"), fg=TEAL, bg=LIGHT_TEAL).pack(anchor="w")
    Label(info, text="per person", font=SMALL_FONT, fg=GRAY, bg=LIGHT_TEAL).pack(anchor="w")
    teal_button(info, "BOOK NOW", lambda: book_now(package["PackageID"])).pack(fill=X, pady=(px(12), px(6)))
    light_button(info, "Back to Destinations", go_to_destinations).pack(fill=X)


# One "Label: value" line in the details box
def add_info_line(parent, title, value):
    row = Frame(parent, bg=LIGHT_TEAL)
    row.pack(anchor="w", fill=X, pady=1)
    Label(row, text=title + ":", font=BOLD_FONT, fg=DARK_TEAL, bg=LIGHT_TEAL, width=9, anchor="nw").pack(side=LEFT, anchor="n")
    Label(row, text=value, font=NORMAL_FONT, fg=DARK_TEAL, bg=LIGHT_TEAL, wraplength=px(270),
          justify=LEFT).pack(side=LEFT, anchor="w")


# Description, Inclusions and Highlights (as bullet lists)
def build_details_lists(page, package):
    box = Frame(page, bg=WHITE)
    box.pack(fill=X, padx=px(48))
    Label(box, text="About this trip", font=HEADING_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    Label(box, text=package["Description"], font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE,
          wraplength=px(980), justify=LEFT).pack(anchor="w", pady=(0, px(10)))
    columns = Frame(box, bg=WHITE)
    columns.pack(fill=X)
    inclusions = make_box(columns, "Inclusions")
    inclusions.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, px(8)))
    add_bullet_list(inclusions, split_list_text(package["Inclusions"]))
    highlights = make_box(columns, "Highlights")
    highlights.pack(side=LEFT, fill=BOTH, expand=True, padx=(px(8), 0))
    add_bullet_list(highlights, split_list_text(package["Highlights"]))


# Show a list of items with bullets
def add_bullet_list(parent, items):
    if len(items) == 0:
        Label(parent, text="(None listed)", font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w")
    for item in items:
        Label(parent, text="•  " + item, font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE,
              wraplength=px(440), justify=LEFT).pack(anchor="w", pady=1)


# The optional add-ons of the package
def build_details_addons(page, package):
    box = make_box(page, "Optional Add-ons")
    box.pack(fill=X, padx=px(48), pady=(px(14), 0))
    addons = database.get_addons(package["PackageID"])
    if len(addons) == 0:
        Label(box, text="This package has no add-ons.", font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w")
    for addon in addons:
        text = "•  " + addon["AddOnName"] + "  -  " + peso(addon["Price"]) + " " + str(addon["Unit"] or "")
        Label(box, text=text, font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")


# Pick a date and see how many slots are left on that day
def build_slots_checker(page, package):
    box = make_box(page, "Check available slots")
    box.pack(fill=X, padx=px(48), pady=(px(14), 0))
    Label(box, text="Travel dates: " + nice_date(package["StartDate"]) + " to " + nice_date(package["EndDate"]) +
          ".  Up to " + str(package["MaxSlots"]) + " people can join on each date.",
          font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    row = Frame(box, bg=WHITE)
    row.pack(anchor="w", pady=px(6))
    slot_check["package"] = package
    slot_check["date"] = make_date_spinboxes(row, first_travel_date(package))
    light_button(row, "Check", check_slots).pack(side=LEFT, padx=px(10))
    slot_check["result"] = Label(row, text="", font=BOLD_FONT, bg=WHITE)
    slot_check["result"].pack(side=LEFT)
    check_slots()


# Count the slots left on the chosen date
def check_slots():
    package = slot_check["package"]
    travel_date = read_date_spinboxes(slot_check["date"])
    problem = check_travel_date(package, travel_date)
    if problem != "":
        slot_check["result"].config(text=problem, fg=RED)
        return
    slots = database.get_slots_left(package["PackageID"], date_to_text(travel_date))
    if slots <= 0:
        slot_check["result"].config(text="Fully booked on " + nice_date(date_to_text(travel_date)) + ".", fg=RED)
    else:
        slot_check["result"].config(text=str(slots) + " of " + str(package["MaxSlots"]) + " slots left on " +
                                    nice_date(date_to_text(travel_date)) + ".", fg=GREEN)


# The reviews of this package
def build_details_reviews(page, package):
    box = make_box(page, "Reviews (" + str(package["ReviewCount"]) + ")")
    box.pack(fill=X, padx=px(48), pady=(px(14), 0))
    reviews = database.get_package_reviews(package["PackageID"])
    if len(reviews) == 0:
        Label(box, text="No reviews yet.", font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w")
    for review in reviews:
        row = Frame(box, bg=WHITE)
        row.pack(fill=X, pady=px(4))
        Label(row, text=stars_text(review["Rating"]), font=(FONT, 12), fg=GOLD, bg=WHITE).pack(anchor="w")
        Label(row, text=review["FirstName"] + " " + review["LastName"] + "  •  " + nice_date(review["ReviewDate"]),
              font=SMALL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w")
        if review["Comment"]:
            Label(row, text=review["Comment"], font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE,
                  wraplength=px(950), justify=LEFT).pack(anchor="w")


# Book Now: guests log in first, then come back to this booking
def book_now(package_id):
    global after_login
    if helpers.current_user is None:
        after_login = ("booking", {"package_id": package_id})
        messagebox.showinfo("LakbayPH", "Please log in (or sign up) first to book this trip.")
        helpers.go_to("login")
        return
    helpers.go_to("booking", {"package_id": package_id})


# ======================= Log in and Sign up =======================

# A white card in the middle of a light page (for the log in and sign up forms)
def make_form_card(parent, title, subtitle):
    page = make_scroll_area(parent, LIGHT_TEAL)
    card = Frame(page, bg=WHITE, padx=px(36), pady=px(26), highlightbackground=BORDER, highlightthickness=1)
    card.pack(pady=px(36))
    Label(card, image=load_logo(px(56)), bg=WHITE).pack()
    Label(card, text=title, font=TITLE_FONT, fg=DARK_TEAL, bg=WHITE).pack()
    Label(card, text=subtitle, font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(pady=(0, px(6)))
    return card


# The log in page (email or phone + password)
def show_login_page(parent, data):
    card = make_form_card(parent, "Welcome back!", "Log in with your email or phone number")
    login_form["login"] = StringVar()
    login_form["password"] = StringVar()
    login_form["show"] = IntVar(value=0)
    first_entry = form_entry(card, "Email or phone number", login_form["login"])
    login_form["password_entry"] = form_entry(card, "Password", login_form["password"], secret=True)
    login_form["password_entry"].bind("<Return>", on_login_enter)
    Checkbutton(card, text="Show password", variable=login_form["show"], command=toggle_login_password,
                bg=WHITE, fg=DARK_TEAL, activebackground=WHITE, font=SMALL_FONT).pack(anchor="w", pady=px(4))
    teal_button(card, "LOG IN", check_login).pack(fill=X, pady=(px(8), px(10)))
    row = Frame(card, bg=WHITE)
    row.pack()
    Label(row, text="No account yet?", font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(side=LEFT)
    make_nav_link(row, "Sign Up", "signup", "").pack(side=LEFT)
    first_entry.focus_set()


# Show or hide the typed password
def toggle_login_password():
    if login_form["show"].get() == 1:
        login_form["password_entry"].config(show="")
    else:
        login_form["password_entry"].config(show="*")


# Pressing Enter in the password box logs in
def on_login_enter(event):
    check_login()


# Check the email/phone and password, then log the user in
def check_login():
    login = login_form["login"].get().strip()
    password = login_form["password"].get()
    if login == "" or password == "":
        messagebox.showwarning("Log In", "Please enter your email or phone number and your password.")
        return
    try:
        user = database.find_user_by_login(login)
    except Exception as error:
        show_error("Could not check your account.", error)
        return
    if user is None or not helpers.check_password(password, user["Password"]):
        messagebox.showwarning("Log In", "Wrong email/phone number or password.")
        return
    if user["IsActive"] != 1:
        messagebox.showwarning("Log In", "This account is disabled. Please contact LakbayPH.")
        return
    helpers.log_in_user(user)
    go_after_login()


# After logging in: admins go to the admin panel, others go back to what they were doing
def go_after_login():
    global after_login
    if helpers.current_user["Role"] == "Admin":
        after_login = None
        helpers.go_to("admin_dashboard")
        return
    if after_login is not None:
        next_page = after_login
        after_login = None
        helpers.go_to(next_page[0], next_page[1])
        return
    helpers.go_to("home")


# The sign up page
def show_signup_page(parent, data):
    card = make_form_card(parent, "Create an account", "Use your email OR your phone number (one is enough)")
    names = Frame(card, bg=WHITE)
    names.pack(fill=X)
    for key in ["first", "last", "email", "phone", "password", "confirm"]:
        signup_form[key] = StringVar()
    left = Frame(names, bg=WHITE)
    left.pack(side=LEFT, fill=X, expand=True, padx=(0, px(6)))
    right = Frame(names, bg=WHITE)
    right.pack(side=LEFT, fill=X, expand=True, padx=(px(6), 0))
    form_entry(left, "First name", signup_form["first"], width=16).focus_set()
    form_entry(right, "Last name", signup_form["last"], width=16)
    form_entry(card, "Email (optional if you give a phone)", signup_form["email"])
    form_entry(card, "Phone: 09XXXXXXXXX or +639XXXXXXXXX (optional if you give an email)", signup_form["phone"])
    form_entry(card, "Password (8+ characters, with a letter and a number)", signup_form["password"], secret=True)
    form_entry(card, "Confirm password", signup_form["confirm"], secret=True)
    teal_button(card, "CREATE ACCOUNT", save_signup).pack(fill=X, pady=(px(14), px(10)))
    row = Frame(card, bg=WHITE)
    row.pack()
    Label(row, text="Already have an account?", font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(side=LEFT)
    make_nav_link(row, "Log In", "login", "").pack(side=LEFT)


# Check the email and phone. Returns "" if OK, or the problem.
def check_contact(email, phone, user_id):
    if email == "" and phone == "":
        return "Please enter your email or your phone number (one is enough)."
    if email != "" and not is_valid_email(email):
        return "Please enter a valid email, like juan@email.com."
    if phone != "" and not is_valid_phone(phone):
        return "Please enter a valid PH mobile number: 09XXXXXXXXX or +639XXXXXXXXX."
    if email != "" and database.email_taken(email.lower(), user_id):
        return "This email is already registered. Please log in instead."
    if phone != "" and database.phone_taken(normalize_phone(phone), user_id):
        return "This phone number is already registered. Please log in instead."
    return ""


# Check the sign up form. Returns "" if OK, or the problem.
def check_signup_form(first, last, email, phone, password, confirm):
    if first == "" or last == "":
        return "Please enter your first and last name."
    problem = check_contact(email, phone, 0)
    if problem != "":
        return problem
    if not is_valid_password(password):
        return "The password needs at least 8 characters with at least one letter and one number."
    if password != confirm:
        return "The two passwords do not match."
    return ""


# Save the new account and log in
def save_signup():
    first = signup_form["first"].get().strip()
    last = signup_form["last"].get().strip()
    email = signup_form["email"].get().strip()
    phone = signup_form["phone"].get().strip()
    password = signup_form["password"].get()
    try:
        problem = check_signup_form(first, last, email, phone, password, signup_form["confirm"].get())
        if problem != "":
            messagebox.showwarning("Sign Up", problem)
            return
        email_value = none_if_empty(email.lower())
        phone_value = None
        if phone != "":
            phone_value = normalize_phone(phone)
        user_id = database.create_user(first, last, email_value, phone_value, password)
        user = database.get_user(user_id)
    except Exception as error:
        show_error("Could not create your account.", error)
        return
    helpers.log_in_user(user)
    messagebox.showinfo("Sign Up", "Welcome to LakbayPH, " + first + "!\nYour username is " + user["Username"] + ".")
    go_after_login()


# ======================= Booking (4 steps) =======================

# Start a new booking for a package
def start_booking(package_id):
    package = database.get_package(package_id)
    if package is None or package["IsActive"] != 1:
        raise ValueError("This package is not available.")
    booking.clear()
    booking["Package"] = package
    booking["Step"] = 1
    booking["TravelDate"] = first_travel_date(package)
    booking["EndDate"] = add_days(booking["TravelDate"], package["Duration"] - 1)
    booking["People"] = 1
    booking["Notes"] = ""
    booking["AddOns"] = []
    for addon in database.get_addons(package_id):
        addon["Quantity"] = 0
        booking["AddOns"].append(addon)
    booking["PromoTypeID"] = 0
    booking["PromoID"] = None
    booking["PromoName"] = ""
    booking["DiscountPercent"] = 0
    booking["PaymentMethod"] = "Pay on Trip"


# The booking page. data has "package_id" when a new booking starts.
def show_booking_page(parent, data):
    if helpers.current_user is None:
        helpers.go_to("login")
        return
    if data is not None:
        start_booking(data["package_id"])
    if "Package" not in booking:
        helpers.go_to("home")
        return
    page = make_scroll_area(parent)
    step = booking["Step"]
    header = Frame(page, bg=WHITE)
    header.pack(fill=X, padx=px(48), pady=(px(20), 0))
    Label(header, text="Booking: " + booking["Package"]["Title"], font=TITLE_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    Label(header, text="Step " + str(step) + " of 4  -  " + STEP_NAMES[step - 1], font=HEADING_FONT,
          fg=TEAL, bg=WHITE).pack(anchor="w")
    draw_step_bar(page, step)
    body = Frame(page, bg=WHITE)
    body.pack(fill=X, padx=px(48), pady=px(6))
    step_vars.clear()
    if step == 1:
        build_step_1(body)
    elif step == 2:
        build_step_2(body)
    elif step == 3:
        build_step_3(body)
    else:
        build_step_4(body)
    build_step_buttons(page, step)


# The 4 circles that show how far the user is
def draw_step_bar(parent, step):
    canvas = Canvas(parent, width=px(820), height=px(56), bg=WHITE, highlightthickness=0)
    canvas.pack(pady=px(10))
    for number in range(4):
        x = px(110) + number * px(200)
        color = BORDER
        if number < step:
            color = TEAL
        if number > 0:
            canvas.create_line(x - px(184), px(16), x - px(16), px(16), fill=color, width=3)
        canvas.create_oval(x - px(14), px(2), x + px(14), px(30), fill=color, outline="")
        canvas.create_text(x, px(16), text=str(number + 1), fill=WHITE, font=BOLD_FONT)
        canvas.create_text(x, px(44), text=STEP_NAMES[number], fill=DARK_TEAL, font=SMALL_FONT)


# Back and Next buttons under the step
def build_step_buttons(page, step):
    row = Frame(page, bg=WHITE)
    row.pack(fill=X, padx=px(48), pady=px(16))
    if step == 1:
        light_button(row, "Cancel", cancel_booking_steps).pack(side=LEFT)
    else:
        light_button(row, "< Back", go_back_step).pack(side=LEFT)
    if step < 4:
        teal_button(row, "Next >", go_next_step).pack(side=RIGHT)


# Leave the booking and go back to the package
def cancel_booking_steps():
    package_id = booking["Package"]["PackageID"]
    booking.clear()
    helpers.go_to("details", package_id)


# Go back one step
def go_back_step():
    booking["Step"] = booking["Step"] - 1
    helpers.go_to("booking")


# Check and save the current step, then go to the next one
def go_next_step():
    step = booking["Step"]
    try:
        if step == 1:
            ok = save_step_1()
        elif step == 2:
            ok = save_step_2()
        else:
            ok = save_step_3()
    except Exception as error:
        show_error("Something went wrong.", error)
        return
    if ok:
        booking["Step"] = step + 1
        helpers.go_to("booking")


# ----- Step 1: travel date, people and notes -----
def build_step_1(body):
    package = booking["Package"]
    box = make_box(body, "When are you going?")
    box.pack(fill=X, pady=px(6))
    Label(box, text="Choose a date from " + nice_date(package["StartDate"]) + " to " + nice_date(package["EndDate"]) +
          ". The trip is " + duration_text(package["Duration"], package["DurationNights"]) + ".",
          font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    row = Frame(box, bg=WHITE)
    row.pack(anchor="w", pady=px(8))
    step_vars["date"] = make_date_spinboxes(row, booking["TravelDate"])
    light_button(row, "Check slots", show_step_1_slots).pack(side=LEFT, padx=px(10))
    step_vars["slots_label"] = Label(row, text="", font=BOLD_FONT, bg=WHITE)
    step_vars["slots_label"].pack(side=LEFT)
    people_box = make_box(body, "How many people?")
    people_box.pack(fill=X, pady=px(6))
    step_vars["people"] = StringVar(value=str(booking["People"]))
    Spinbox(people_box, from_=1, to=package["MaxSlots"], textvariable=step_vars["people"], width=5,
            font=NORMAL_FONT).pack(side=LEFT)
    Label(people_box, text="   " + peso(package["Price"]) + " per person", font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(side=LEFT)
    notes_box = make_box(body, "Notes for our team (optional)")
    notes_box.pack(fill=X, pady=px(6))
    step_vars["notes"] = Text(notes_box, height=4, width=80, font=NORMAL_FONT, relief=SOLID, bd=1, wrap=WORD)
    step_vars["notes"].insert("1.0", booking["Notes"])
    step_vars["notes"].pack(fill=X)
    show_step_1_slots()


# Show the slots left and the end date for the chosen date
def show_step_1_slots():
    package = booking["Package"]
    travel_date = read_date_spinboxes(step_vars["date"])
    problem = check_travel_date(package, travel_date)
    if problem != "":
        step_vars["slots_label"].config(text=problem, fg=RED)
        return
    slots = database.get_slots_left(package["PackageID"], date_to_text(travel_date))
    end_date = add_days(travel_date, package["Duration"] - 1)
    text = str(slots) + " slot(s) left   •   Trip ends " + end_date.strftime("%b %d, %Y")
    color = GREEN
    if slots <= 0:
        text = "Fully booked on this date. Please choose another date."
        color = RED
    step_vars["slots_label"].config(text=text, fg=color)


# Check step 1 and save it in the booking
def save_step_1():
    package = booking["Package"]
    travel_date = read_date_spinboxes(step_vars["date"])
    problem = check_travel_date(package, travel_date)
    if problem != "":
        messagebox.showwarning("Step 1", problem)
        return False
    people = read_int(step_vars["people"].get())
    if people is None or people < 1:
        messagebox.showwarning("Step 1", "Please enter how many people are going (1 or more).")
        return False
    slots = database.get_slots_left(package["PackageID"], date_to_text(travel_date))
    if people > slots:
        messagebox.showwarning("Step 1", "Only " + str(max(slots, 0)) + " slot(s) are left on this date.")
        return False
    booking["TravelDate"] = travel_date
    booking["EndDate"] = add_days(travel_date, package["Duration"] - 1)
    booking["People"] = people
    booking["Notes"] = step_vars["notes"].get("1.0", END).strip()[:500]
    return True


# ----- Step 2: add-ons with a live total -----
def build_step_2(body):
    box = make_box(body, "Choose add-ons (optional)")
    box.pack(fill=X, pady=px(6))
    step_vars["addon_vars"] = []
    if len(booking["AddOns"]) == 0:
        Label(box, text="This package has no add-ons. Click Next to continue.", font=NORMAL_FONT,
              fg=GRAY, bg=WHITE).pack(anchor="w")
    row_number = 0
    for addon in booking["AddOns"]:
        Label(box, text=addon["AddOnName"], font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).grid(row=row_number, column=0, sticky="w", pady=px(3))
        Label(box, text=peso(addon["Price"]) + " " + str(addon["Unit"] or ""), font=NORMAL_FONT, fg=GRAY,
              bg=WHITE).grid(row=row_number, column=1, sticky="w", padx=px(20))
        quantity = StringVar(value=str(addon["Quantity"]))
        spinbox = Spinbox(box, from_=0, to=20, textvariable=quantity, width=4, font=NORMAL_FONT, command=update_live_total)
        spinbox.grid(row=row_number, column=2)
        spinbox.bind("<KeyRelease>", on_quantity_typed)
        step_vars["addon_vars"].append(quantity)
        row_number = row_number + 1
    step_vars["total_label"] = Label(body, text="", font=(FONT, 13, "bold"), fg=TEAL, bg=WHITE, justify=LEFT)
    step_vars["total_label"].pack(anchor="w", pady=px(10))
    update_live_total()


# Typing a quantity also updates the total
def on_quantity_typed(event):
    update_live_total()


# Read the quantities from the Spinboxes (None if one is wrong)
def read_addon_quantities():
    quantities = []
    for quantity in step_vars["addon_vars"]:
        number = read_int(quantity.get())
        if number is None or number < 0 or number > 20:
            return None
        quantities.append(number)
    return quantities


# Recompute the total every time a quantity changes
def update_live_total():
    package = booking["Package"]
    quantities = read_addon_quantities()
    if quantities is None:
        step_vars["total_label"].config(text="Please enter quantities from 0 to 20.", fg=RED)
        return
    chosen = []
    number = 0
    for addon in booking["AddOns"]:
        chosen.append({"Price": addon["Price"], "Quantity": quantities[number]})
        number = number + 1
    totals = compute_total(package["Price"], booking["People"], chosen, 0)
    text = "Base: " + peso(package["Price"]) + " x " + str(booking["People"]) + " = " + peso(totals["Base"])
    text = text + "\nAdd-ons: " + peso(totals["AddOns"]) + "\nTotal so far: " + peso(totals["Subtotal"])
    step_vars["total_label"].config(text=text, fg=TEAL)


# Check step 2 and save the quantities
def save_step_2():
    quantities = read_addon_quantities()
    if quantities is None:
        messagebox.showwarning("Step 2", "Please enter add-on quantities from 0 to 20.")
        return False
    number = 0
    for addon in booking["AddOns"]:
        addon["Quantity"] = quantities[number]
        number = number + 1
    return True


# ----- Step 3: PWD / Senior Citizen discount -----
def build_step_3(body):
    user_id = helpers.current_user["UserID"]
    box = make_box(body, "PWD / Senior Citizen discount (20%)")
    box.pack(fill=X, pady=px(6))
    Label(box, text="The 20% discount is only applied after an admin approves your ID.",
          font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w", pady=(0, px(6)))
    step_vars["choice"] = IntVar(value=booking["PromoTypeID"])
    Radiobutton(box, text="No discount", value=0, variable=step_vars["choice"], command=on_discount_choice,
                bg=WHITE, fg=DARK_TEAL, activebackground=WHITE, font=NORMAL_FONT).pack(anchor="w")
    chosen_request = None
    for promo_type in database.get_promo_types():
        request = database.get_user_promo(user_id, promo_type["PromoTypeID"])
        label = promo_name(promo_type["PromoTypeName"]) + "   (" + describe_promo_status(request) + ")"
        Radiobutton(box, text=label, value=promo_type["PromoTypeID"], variable=step_vars["choice"],
                    command=on_discount_choice, bg=WHITE, fg=DARK_TEAL, activebackground=WHITE,
                    font=NORMAL_FONT).pack(anchor="w")
        if promo_type["PromoTypeID"] == booking["PromoTypeID"]:
            chosen_request = request
    if booking["PromoTypeID"] != 0:
        build_discount_request_row(body, chosen_request)


# "SENIOR CITIZEN" -> "Senior Citizen", "PWD" stays "PWD"
def promo_name(promo_type_name):
    if promo_type_name == "PWD":
        return "PWD"
    return promo_type_name.title()


# A short text for the status of a discount request
def describe_promo_status(request):
    if request is None:
        return "not requested yet"
    if request["Status"] == "Approved":
        return "Approved - 20% will be applied"
    if request["Status"] == "Pending":
        return "waiting for admin approval, not applied yet"
    return "Rejected - you can send your ID again"


# Show the ID number form if the user has no request (or it was rejected)
def build_discount_request_row(body, request):
    if request is not None and request["Status"] != "Rejected":
        return
    box = make_box(body, "Send your ID number for approval")
    box.pack(fill=X, pady=px(6))
    step_vars["document"] = StringVar()
    Label(box, text="ID number:", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    Entry(box, textvariable=step_vars["document"], width=26, font=NORMAL_FONT, relief=SOLID, bd=1).pack(side=LEFT, padx=px(8), ipady=2)
    teal_button(box, "Submit for approval", submit_booking_discount).pack(side=LEFT)


# A discount Radiobutton was clicked: remember it and redraw the step
def on_discount_choice():
    booking["PromoTypeID"] = step_vars["choice"].get()
    helpers.go_to("booking")


# Send the ID number from step 3
def submit_booking_discount():
    if submit_discount(booking["PromoTypeID"], step_vars["document"].get()):
        helpers.go_to("booking")


# Save a discount request (used in booking step 3 and the profile page)
def submit_discount(promo_type_id, document_number):
    document_number = document_number.strip()
    if len(document_number) < 4:
        messagebox.showwarning("Discount", "Please enter your ID number (at least 4 characters).")
        return False
    try:
        database.submit_promo_request(helpers.current_user["UserID"], promo_type_id, document_number)
    except ValueError as problem:
        messagebox.showwarning("Discount", str(problem))
        return False
    except Exception as error:
        show_error("Could not send your request.", error)
        return False
    messagebox.showinfo("Discount", "Your request was sent. The discount will apply once an admin approves it.")
    return True


# Save step 3: the discount only counts if it is approved
def save_step_3():
    booking["PromoID"] = None
    booking["PromoName"] = ""
    booking["DiscountPercent"] = 0
    if booking["PromoTypeID"] == 0:
        return True
    request = database.get_user_promo(helpers.current_user["UserID"], booking["PromoTypeID"])
    if request is not None and request["Status"] == "Approved":
        booking["PromoID"] = request["PromoID"]
        booking["PromoName"] = promo_name(request["PromoTypeName"])
        booking["DiscountPercent"] = request["DiscountPercentage"]
        return True
    return messagebox.askyesno("Step 3", "This discount is not approved yet, so it will NOT be applied.\n"
                                         "Continue without the discount?")


# ----- Step 4: summary, payment and confirm -----
def build_step_4(body):
    build_summary_box(body)
    box = make_box(body, "Payment method")
    box.pack(fill=X, pady=px(6))
    step_vars["method"] = StringVar(value=booking["PaymentMethod"])
    for method in PAYMENT_METHODS:
        Radiobutton(box, text=method, value=method, variable=step_vars["method"], bg=WHITE, fg=DARK_TEAL,
                    activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT, padx=(0, px(14)))
    Label(body, text="GCash, Maya, Card and Bank Transfer are only simulated in this app. No real money is "
                     "charged and card numbers are never asked or saved.",
          font=SMALL_FONT, fg=GRAY, bg=WHITE, wraplength=px(900), justify=LEFT).pack(anchor="w")
    step_vars["terms"] = IntVar(value=0)
    Checkbutton(body, text="I agree to the LakbayPH terms and the cancellation policy.", variable=step_vars["terms"],
                bg=WHITE, fg=DARK_TEAL, activebackground=WHITE, font=NORMAL_FONT).pack(anchor="w", pady=px(8))
    teal_button(body, "CONFIRM BOOKING", confirm_booking).pack(anchor="e")


# The add-ons the user picked (quantity more than 0)
def chosen_addons():
    chosen = []
    for addon in booking["AddOns"]:
        if addon["Quantity"] > 0:
            chosen.append(addon)
    return chosen


# The price summary of the booking right now
def current_totals():
    return compute_total(booking["Package"]["Price"], booking["People"], chosen_addons(), booking["DiscountPercent"])


# The summary: base price x people + add-ons - discount = total
def build_summary_box(body):
    package = booking["Package"]
    totals = current_totals()
    box = make_box(body, "Booking summary")
    box.pack(fill=X, pady=px(6))
    lines = [("Package", package["Title"]),
             ("Travel dates", booking["TravelDate"].strftime("%b %d, %Y") + "  to  " + booking["EndDate"].strftime("%b %d, %Y")),
             ("People", str(booking["People"])),
             ("Base price", peso(package["Price"]) + " x " + str(booking["People"]) + " = " + peso(totals["Base"]))]
    for addon in chosen_addons():
        lines.append(("  + " + addon["AddOnName"], peso(addon["Price"]) + " x " + str(addon["Quantity"]) +
                      " = " + peso(addon["Price"] * addon["Quantity"])))
    lines.append(("Subtotal", peso(totals["Subtotal"])))
    if totals["Discount"] > 0:
        lines.append(("Discount (" + booking["PromoName"] + " 20%)", "- " + peso(totals["Discount"])))
    row_number = 0
    for line in lines:
        Label(box, text=line[0], font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).grid(row=row_number, column=0, sticky="w", pady=1)
        Label(box, text=line[1], font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE).grid(row=row_number, column=1, sticky="w", padx=px(30))
        row_number = row_number + 1
    Label(box, text="TOTAL", font=BIG_PRICE_FONT, fg=DARK_TEAL, bg=WHITE).grid(row=row_number, column=0, sticky="w", pady=(px(8), 0))
    Label(box, text=peso(totals["Total"]), font=BIG_PRICE_FONT, fg=TEAL, bg=WHITE).grid(row=row_number, column=1, sticky="w", padx=px(30), pady=(px(8), 0))


# Make the payment info. Non-cash payments are simulated with a fake reference.
def make_payment(method):
    if method == "Pay on Trip":
        return {"PaymentMethod": method, "PaymentStatus": "Pending", "TransactionReference": None}
    codes = {"GCash": "GC", "Maya": "MY", "Card": "CD", "Bank Transfer": "BT"}
    reference = codes[method] + "-" + helpers.today().strftime("%Y%m%d") + "-" + str(random.randint(100000, 999999))
    return {"PaymentMethod": method, "PaymentStatus": "Paid", "TransactionReference": reference}


# The row that will be saved in the bookings table
def make_booking_record(totals):
    return {"UserID": helpers.current_user["UserID"], "PackageID": booking["Package"]["PackageID"],
            "NumberOfPeople": booking["People"], "PromoID": booking["PromoID"],
            "TravelDate": date_to_text(booking["TravelDate"]), "EndDate": date_to_text(booking["EndDate"]),
            "Notes": booking["Notes"], "UnitPrice": booking["Package"]["Price"],
            "DiscountAmount": totals["Discount"], "TotalAmount": totals["Total"]}


# Save everything and show the confirmation page
def confirm_booking():
    if step_vars["terms"].get() != 1:
        messagebox.showwarning("Confirm Booking", "Please agree to the terms first.")
        return
    method = step_vars["method"].get()
    booking["PaymentMethod"] = method
    totals = current_totals()
    if method != "Pay on Trip":
        question = ("This is a SIMULATED " + method + " payment of " + peso(totals["Total"]) +
                    ".\nNo real money will be charged. Continue?")
        if not messagebox.askokcancel("Simulated Payment", question):
            return
    try:
        booking_id = database.save_booking(make_booking_record(totals), chosen_addons(), make_payment(method))
    except ValueError as problem:
        messagebox.showwarning("Confirm Booking", str(problem))
        return
    except Exception as error:
        show_error("Your booking could not be saved. Nothing was charged or saved.", error)
        return
    booking.clear()
    helpers.go_to("confirmation", booking_id)


# ======================= Confirmation and receipt =======================

# The page after a booking is saved: reference number and receipt
def show_confirmation_page(parent, booking_id):
    record = database.get_booking(booking_id)
    if record is None or helpers.current_user is None or record["UserID"] != helpers.current_user["UserID"]:
        helpers.go_to("home")
        return
    page = make_scroll_area(parent)
    box = Frame(page, bg=WHITE)
    box.pack(pady=px(20))
    check = Canvas(box, width=px(70), height=px(70), bg=WHITE, highlightthickness=0)
    check.pack()
    check.create_oval(px(4), px(4), px(66), px(66), fill=TEAL, outline="")
    check.create_line(px(20), px(36), px(32), px(48), px(52), px(24), fill=WHITE, width=px(6))
    Label(box, text="Thank you! Your booking was received.", font=TITLE_FONT, fg=DARK_TEAL, bg=WHITE).pack(pady=px(6))
    Label(box, text="Booking reference", font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack()
    Label(box, text=record["BookingReference"], font=(FONT, 22, "bold"), fg=TEAL, bg=WHITE).pack()
    Label(box, text="Status: Pending. Our team will confirm your booking soon.", font=NORMAL_FONT,
          fg=DARK_TEAL, bg=WHITE).pack(pady=(0, px(10)))
    show_receipt_box(box, booking_id)
    buttons = Frame(box, bg=WHITE)
    buttons.pack(pady=px(12))
    teal_button(buttons, "Save receipt (.txt)", lambda: save_receipt(booking_id)).pack(side=LEFT, padx=px(4))
    light_button(buttons, "My Bookings", go_to_my_bookings).pack(side=LEFT, padx=px(4))
    light_button(buttons, "Back to Home", on_home_button).pack(side=LEFT, padx=px(4))


# Go to the home page (for buttons)
def on_home_button():
    helpers.go_to("home")


# A read-only Text box with the receipt
def show_receipt_box(parent, booking_id):
    receipt = Text(parent, width=58, height=26, font=MONO_FONT, relief=SOLID, bd=1, bg=LIGHT_GRAY, padx=10, pady=8)
    receipt.insert("1.0", build_receipt_text(booking_id))
    receipt.config(state=DISABLED)
    receipt.pack()


# One receipt line: name on the left, amount on the right
def add_receipt_line(lines, left, right):
    lines.append(left[:32].ljust(33) + str(right).rjust(23))


# Make the receipt text of a booking
def build_receipt_text(booking_id):
    record = database.get_booking(booking_id)
    lines = ["=" * 56, "LakbayPH - Travel Services".center(56), "BOOKING RECEIPT".center(56), "=" * 56]
    add_receipt_line(lines, "Reference", record["BookingReference"])
    add_receipt_line(lines, "Booked on", str(record["BookingDate"])[:16])
    add_receipt_line(lines, "Customer", record["FirstName"] + " " + record["LastName"])
    add_receipt_line(lines, "Contact", str(record["Email"] or record["Phone"]))
    lines.append("-" * 56)
    lines.append(record["Title"])
    lines.append(str(record["Location"]))
    add_receipt_line(lines, "Travel date", nice_date(record["TravelDate"]))
    add_receipt_line(lines, "End date", nice_date(record["EndDate"]))
    add_receipt_line(lines, "People", record["NumberOfPeople"])
    add_receipt_line(lines, "Status", record["Status"])
    lines.append("-" * 56)
    add_receipt_amounts(lines, record)
    lines.append("-" * 56)
    add_receipt_line(lines, "Payment method", record["PaymentMethod"])
    add_receipt_line(lines, "Payment status", record["PaymentStatus"])
    if record["TransactionReference"]:
        add_receipt_line(lines, "Transaction ref (simulated)", record["TransactionReference"])
    lines.append("=" * 56)
    lines.append("Thank you for booking with LakbayPH!".center(56))
    return "\n".join(lines)


# The money part of the receipt
def add_receipt_amounts(lines, record):
    base = record["UnitPrice"] * record["NumberOfPeople"]
    add_receipt_line(lines, "Base " + peso(record["UnitPrice"]) + " x " + str(record["NumberOfPeople"]), peso(base))
    addon_total = 0
    for addon in database.get_booking_addons(record["BookingID"]):
        amount = addon["UnitPrice"] * addon["Quantity"]
        add_receipt_line(lines, "+ " + addon["AddOnName"] + " x" + str(addon["Quantity"]), peso(amount))
        addon_total = addon_total + amount
    add_receipt_line(lines, "Subtotal", peso(base + addon_total))
    if record["DiscountAmount"] > 0:
        add_receipt_line(lines, "Discount (" + str(record["PromoTypeName"]) + " 20%)", "- " + peso(record["DiscountAmount"]))
    add_receipt_line(lines, "TOTAL", peso(record["TotalAmount"]))


# Save the receipt as a .txt file
def save_receipt(booking_id):
    record = database.get_booking(booking_id)
    file_path = filedialog.asksaveasfilename(title="Save receipt", defaultextension=".txt",
                                             initialfile=record["BookingReference"] + ".txt",
                                             filetypes=[("Text file", "*.txt")])
    if file_path == "":
        return
    try:
        receipt_file = open(file_path, "w", encoding="utf-8")
        receipt_file.write(build_receipt_text(booking_id))
        receipt_file.close()
        messagebox.showinfo("Receipt", "The receipt was saved.")
    except OSError as error:
        show_error("Could not save the receipt.", error)


# ======================= My Bookings =======================

# The user's bookings in 3 tabs: Upcoming, Completed, Cancelled
def show_my_bookings_page(parent, data):
    global my_bookings_tab
    if helpers.current_user is None:
        helpers.go_to("login")
        return
    if data is not None:
        my_bookings_tab = data
    database.auto_complete_bookings()
    page = make_scroll_area(parent)
    add_section_title(page, "My Bookings", "Hello, " + helpers.current_user["FirstName"] + "! Here are your trips.")
    build_booking_tabs(page)
    records = bookings_for_tab(database.get_user_bookings(helpers.current_user["UserID"]))
    list_frame = Frame(page, bg=WHITE)
    list_frame.pack(fill=X, padx=px(60), pady=px(10))
    if len(records) == 0:
        Label(list_frame, text="You have no " + my_bookings_tab.lower() + " bookings.", font=NORMAL_FONT,
              fg=GRAY, bg=WHITE).pack(pady=px(20))
        teal_button(list_frame, "Find a trip", go_to_destinations).pack()
    for record in records:
        build_booking_row(list_frame, record)
    build_footer(page)


# The 3 tab buttons (the open tab is teal)
def build_booking_tabs(page):
    tabs = Frame(page, bg=WHITE)
    tabs.pack()
    for tab in ["Upcoming", "Completed", "Cancelled"]:
        make_tab_button(tabs, tab).pack(side=LEFT, padx=px(4))


# One tab button (made in its own function so each button keeps its own tab name)
def make_tab_button(parent, tab):
    if tab == my_bookings_tab:
        return teal_button(parent, tab, lambda: helpers.go_to("my_bookings", tab), width=12)
    return light_button(parent, tab, lambda: helpers.go_to("my_bookings", tab), width=12)


# Keep only the bookings of the open tab
def bookings_for_tab(records):
    results = []
    for record in records:
        if my_bookings_tab == "Upcoming" and record["Status"] in ("Pending", "Confirmed"):
            results.append(record)
        elif my_bookings_tab == record["Status"]:
            results.append(record)
    return results


# One booking in the list with its buttons
def build_booking_row(parent, record):
    row = Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1, padx=px(12), pady=px(10))
    row.pack(fill=X, pady=px(6))
    Label(row, image=load_image(record["ImageFileName"], px(150), px(95)), bg=WHITE).pack(side=LEFT)
    info = Frame(row, bg=WHITE, padx=px(14))
    info.pack(side=LEFT, fill=BOTH, expand=True)
    Label(info, text=record["Title"], font=(FONT, 12, "bold"), fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    Label(info, text=record["BookingReference"] + "   •   " + nice_date(record["TravelDate"]) + " to " +
          nice_date(record["EndDate"]) + "   •   " + str(record["NumberOfPeople"]) + " people",
          font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w")
    Label(info, text="Total: " + peso(record["TotalAmount"]) + "   •   " + str(record["PaymentMethod"]) +
          " (" + str(record["PaymentStatus"]) + ")", font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    Label(info, text=record["Status"], font=BOLD_FONT, fg=WHITE, bg=STATUS_COLORS[record["Status"]],
          padx=px(8)).pack(anchor="w", pady=(px(4), 0))
    build_booking_row_buttons(row, record)


# View / Cancel / Review buttons of one booking
def build_booking_row_buttons(row, record):
    buttons = Frame(row, bg=WHITE)
    buttons.pack(side=RIGHT)
    booking_id = record["BookingID"]
    light_button(buttons, "View Details", lambda: view_booking_details(booking_id), width=14).pack(pady=2)
    if can_cancel(record):
        Button(buttons, text="Cancel Booking", command=lambda: cancel_my_booking(record), bg=RED, fg=WHITE,
               relief=FLAT, font=BOLD_FONT, width=14, cursor="hand2").pack(pady=2)
    if record["Status"] == "Completed" and record["ReviewID"] is None:
        teal_button(buttons, "Write a Review", lambda: open_review_window(record), width=14).pack(pady=2)
    elif record["ReviewID"] is not None:
        Label(buttons, text="You rated " + stars_text(record["Rating"]), font=NORMAL_FONT, fg=GOLD, bg=WHITE).pack(pady=2)


# A booking can be cancelled if it is pending/confirmed and the trip has not started
def can_cancel(record):
    if record["Status"] not in ("Pending", "Confirmed"):
        return False
    return text_to_date(record["TravelDate"]) > helpers.today()


# A small window with the booking receipt
def view_booking_details(booking_id):
    window = Toplevel()
    window.title("Booking Details")
    window.configure(bg=WHITE)
    center_window(window, px(560), px(600))
    show_receipt_box(window, booking_id)
    buttons = Frame(window, bg=WHITE)
    buttons.pack(pady=px(10))
    teal_button(buttons, "Save receipt (.txt)", lambda: save_receipt(booking_id)).pack(side=LEFT, padx=px(4))
    light_button(buttons, "Close", window.destroy).pack(side=LEFT, padx=px(4))
    window.grab_set()


# Cancel a booking (this frees the slots on that date)
def cancel_my_booking(record):
    question = "Cancel booking " + record["BookingReference"] + "?\nThe slots will be given back."
    if not messagebox.askyesno("Cancel Booking", question):
        return
    try:
        database.cancel_booking_for_user(record["BookingID"], helpers.current_user["UserID"])
    except ValueError as problem:
        messagebox.showwarning("Cancel Booking", str(problem))
        return
    except Exception as error:
        show_error("Could not cancel the booking.", error)
        return
    messagebox.showinfo("Cancel Booking", "Your booking was cancelled.")
    helpers.go_to("my_bookings", "Cancelled")


# A window to rate a completed trip (1 to 5 stars) and write a comment
def open_review_window(record):
    window = Toplevel()
    window.title("Write a Review")
    window.configure(bg=WHITE, padx=px(20), pady=px(16))
    center_window(window, px(480), px(420))
    review_form["window"] = window
    review_form["booking_id"] = record["BookingID"]
    review_form["rating"] = IntVar(value=5)
    Label(window, text="How was " + record["Title"] + "?", font=HEADING_FONT, fg=DARK_TEAL, bg=WHITE,
          wraplength=px(420)).pack()
    review_form["stars"] = Label(window, text=stars_text(5), font=(FONT, 24), fg=GOLD, bg=WHITE)
    review_form["stars"].pack()
    Scale(window, from_=1, to=5, orient=HORIZONTAL, variable=review_form["rating"], command=on_rating_change,
          length=px(240), bg=WHITE, highlightthickness=0, label="Rating (1 to 5)").pack(pady=px(4))
    Label(window, text="Comment (optional)", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    review_form["comment"] = Text(window, height=5, width=46, font=NORMAL_FONT, relief=SOLID, bd=1, wrap=WORD)
    review_form["comment"].pack(fill=X)
    teal_button(window, "Submit Review", submit_review).pack(fill=X, pady=(px(10), 0))
    window.grab_set()


# Moving the Scale updates the stars
def on_rating_change(value):
    review_form["stars"].config(text=stars_text(int(float(value))))


# Save the review
def submit_review():
    comment = review_form["comment"].get("1.0", END).strip()[:1000]
    try:
        database.add_review(helpers.current_user["UserID"], review_form["booking_id"],
                            review_form["rating"].get(), comment)
    except ValueError as problem:
        messagebox.showwarning("Review", str(problem))
        return
    except Exception as error:
        show_error("Could not save your review.", error)
        return
    review_form["window"].destroy()
    messagebox.showinfo("Review", "Thank you for your review!")
    helpers.go_to("my_bookings", "Completed")


# ======================= Profile =======================

# Edit details, change password and see discount requests
def show_profile_page(parent, data):
    if helpers.current_user is None:
        helpers.go_to("login")
        return
    user = database.get_user(helpers.current_user["UserID"])
    page = make_scroll_area(parent)
    add_section_title(page, "My Profile", "Username: " + user["Username"])
    columns = Frame(page, bg=WHITE)
    columns.pack(pady=px(6))
    left = Frame(columns, bg=WHITE)
    left.grid(row=0, column=0, sticky="n", padx=px(12))
    right = Frame(columns, bg=WHITE)
    right.grid(row=0, column=1, sticky="n", padx=px(12))
    build_profile_details(left, user)
    build_password_box(right)
    build_profile_discount_box(right)
    build_footer(page)


# The form with the user's details
def build_profile_details(parent, user):
    box = make_box(parent, "My Details")
    box.pack(fill=X)
    fields = [("first", "First name", "FirstName"), ("last", "Last name", "LastName"),
              ("email", "Email", "Email"), ("phone", "Phone (09XXXXXXXXX)", "Phone"), ("address", "Address", "Address")]
    for field in fields:
        profile_form[field[0]] = StringVar(value=user[field[2]] or "")
        form_entry(box, field[1], profile_form[field[0]])
    profile_form["gender"] = StringVar(value=user["Gender"] or "Prefer not to say")
    Label(box, text="Gender", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w", pady=(8, 2))
    make_choice_menu(box, profile_form["gender"], ["Prefer not to say", "Male", "Female", "Other"]).pack(anchor="w")
    teal_button(box, "Save Changes", save_profile).pack(fill=X, pady=(px(12), 0))


# Check and save the profile
def save_profile():
    user_id = helpers.current_user["UserID"]
    first = profile_form["first"].get().strip()
    last = profile_form["last"].get().strip()
    email = profile_form["email"].get().strip()
    phone = profile_form["phone"].get().strip()
    if first == "" or last == "":
        messagebox.showwarning("Profile", "Please enter your first and last name.")
        return
    try:
        problem = check_contact(email, phone, user_id)
        if problem != "":
            messagebox.showwarning("Profile", problem)
            return
        phone_value = None
        if phone != "":
            phone_value = normalize_phone(phone)
        user = {"FirstName": first, "LastName": last, "Email": none_if_empty(email.lower()), "Phone": phone_value,
                "Address": none_if_empty(profile_form["address"].get()), "Gender": profile_form["gender"].get()}
        database.update_profile(user_id, user)
        helpers.log_in_user(database.get_user(user_id))
    except Exception as error:
        show_error("Could not save your profile.", error)
        return
    messagebox.showinfo("Profile", "Your profile was saved.")
    helpers.go_to("profile")


# The change password form
def build_password_box(parent):
    box = make_box(parent, "Change Password")
    box.pack(fill=X)
    profile_form["current"] = StringVar()
    profile_form["new"] = StringVar()
    profile_form["confirm"] = StringVar()
    form_entry(box, "Current password", profile_form["current"], secret=True)
    form_entry(box, "New password (8+ characters, letter and number)", profile_form["new"], secret=True)
    form_entry(box, "Confirm new password", profile_form["confirm"], secret=True)
    teal_button(box, "Change Password", change_password).pack(fill=X, pady=(px(12), 0))


# Check the old password, then save the new one
def change_password():
    user = database.get_user(helpers.current_user["UserID"])
    if not helpers.check_password(profile_form["current"].get(), user["Password"]):
        messagebox.showwarning("Change Password", "Your current password is wrong.")
        return
    new_password = profile_form["new"].get()
    if not is_valid_password(new_password):
        messagebox.showwarning("Change Password", "The new password needs at least 8 characters with a letter and a number.")
        return
    if new_password != profile_form["confirm"].get():
        messagebox.showwarning("Change Password", "The new passwords do not match.")
        return
    try:
        database.update_password(user["UserID"], new_password)
    except Exception as error:
        show_error("Could not change your password.", error)
        return
    messagebox.showinfo("Change Password", "Your password was changed.")
    helpers.go_to("profile")


# Discount request status and a form to send an ID number
def build_profile_discount_box(parent):
    box = make_box(parent, "PWD / Senior Citizen Discount")
    box.pack(fill=X, pady=(px(12), 0))
    promo_types = database.get_promo_types()
    for promo_type in promo_types:
        request = database.get_user_promo(helpers.current_user["UserID"], promo_type["PromoTypeID"])
        Label(box, text=promo_name(promo_type["PromoTypeName"]) + ":  " + describe_promo_status(request),
              font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    Label(box, text="Send an ID number for approval:", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w", pady=(px(8), 0))
    profile_form["promo_type"] = IntVar(value=promo_types[0]["PromoTypeID"])
    for promo_type in promo_types:
        Radiobutton(box, text=promo_name(promo_type["PromoTypeName"]), value=promo_type["PromoTypeID"],
                    variable=profile_form["promo_type"], bg=WHITE, fg=DARK_TEAL, activebackground=WHITE,
                    font=NORMAL_FONT).pack(anchor="w")
    profile_form["document"] = StringVar()
    form_entry(box, "ID number", profile_form["document"])
    teal_button(box, "Submit for approval", submit_profile_discount).pack(fill=X, pady=(px(10), 0))


# Send the discount request from the profile page
def submit_profile_discount():
    if submit_discount(profile_form["promo_type"].get(), profile_form["document"].get()):
        helpers.go_to("profile")
