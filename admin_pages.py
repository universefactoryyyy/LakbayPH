# admin_pages.py - the admin panel: dashboard, packages (create, read,
# update, delete + pictures), bookings and discount requests.
# Every admin action checks the role in the database first (require_admin).

import os
import shutil
from tkinter import *
from tkinter import messagebox, filedialog
import helpers
import database
import user_pages
from helpers import *

# Widgets and data of the packages form
form = {}
form_addons = []
package_rows = []
editing_id = None

# Bookings and discount pages
booking_rows = []
promo_rows = []
lists = {}

ADMIN_MENU = [("▦", "Dashboard", "admin_dashboard"), ("✈", "Packages", "admin_packages"),
              ("☰", "Bookings", "admin_bookings"), ("✓", "Discount Requests", "admin_discounts")]
IMAGE_TYPES = (".png", ".jpg", ".jpeg")
BOOKING_STATUSES = ["All", "Pending", "Confirmed", "Completed", "Cancelled"]
PROMO_STATUSES = ["All", "Pending", "Approved", "Rejected"]

# Admin colors
PAGE_BG = LIGHT_GRAY
MENU_HOVER = "#0D4752"
MENU_LINE = "#164B55"
STRIPE = "#F7FAFB"
DARK_GOLD = "#A87A00"
PILL_COLORS = {"Pending": GOLD, "Confirmed": GREEN, "Completed": DARK_TEAL, "Cancelled": RED,
               "Approved": GREEN, "Rejected": RED}
ROW_COLORS = {"Pending": DARK_GOLD, "Confirmed": GREEN, "Completed": DARK_TEAL, "Cancelled": GRAY,
              "Approved": GREEN, "Rejected": GRAY}


# ======================= Layout and role check =======================

# Stop if the logged in user is not an admin (checked in the database)
def require_admin():
    user = helpers.current_user
    if user is not None and database.user_is_admin(user["UserID"]):
        return True
    messagebox.showerror("LakbayPH", "Only admins can do this.")
    return False


# The admin page: left menu, white title bar, and a gray area for the content.
# Returns the frame for the page content.
def build_admin_layout(parent, active_page, title, subtitle):
    build_side_menu(parent, active_page)
    main = Frame(parent, bg=PAGE_BG)
    main.pack(side=LEFT, fill=BOTH, expand=True)
    build_admin_header(main, title, subtitle)
    content = Frame(main, bg=PAGE_BG)
    content.pack(fill=BOTH, expand=True, padx=px(20), pady=px(16))
    return content


# The dark menu on the left (with the number of things waiting for the admin)
def build_side_menu(parent, active_page):
    menu = Frame(parent, bg=DEEP_TEAL, width=px(205))
    menu.pack(side=LEFT, fill=Y)
    menu.pack_propagate(False)
    top = Frame(menu, bg=DEEP_TEAL)
    top.pack(fill=X, pady=(px(20), px(14)))
    Label(top, image=load_logo(px(48)), bg=DEEP_TEAL).pack()
    Label(top, text="LakbayPH", font=(FONT, 15, "bold"), fg=TEAL, bg=DEEP_TEAL).pack()
    Label(top, text="ADMIN PANEL", font=(FONT, 8, "bold"), fg="#8FB5BC", bg=DEEP_TEAL).pack()
    Frame(menu, bg=MENU_LINE, height=1).pack(fill=X, padx=px(16), pady=(0, px(12)))
    Label(menu, text="MENU", font=(FONT, 8, "bold"), fg="#8FB5BC", bg=DEEP_TEAL).pack(anchor="w", padx=px(22), pady=(0, px(4)))
    badges = {"admin_bookings": database.get_booking_counts().get("Pending", 0),
              "admin_discounts": database.get_promo_counts().get("Pending", 0)}
    for item in ADMIN_MENU:
        make_menu_button(menu, item, active_page, badges.get(item[2], 0)).pack(fill=X, padx=px(10), pady=2)
    build_menu_bottom(menu)


# The bottom of the menu: who is logged in, View Website and Log Out
def build_menu_bottom(menu):
    make_menu_button(menu, ("⏏", "Log Out", "logout"), "", 0).pack(side=BOTTOM, fill=X, padx=px(10), pady=(2, px(16)))
    make_menu_button(menu, ("⌂", "View Website", "home"), "", 0).pack(side=BOTTOM, fill=X, padx=px(10), pady=2)
    user = helpers.current_user
    card = Frame(menu, bg=MENU_HOVER, padx=px(10), pady=px(10))
    card.pack(side=BOTTOM, fill=X, padx=px(10), pady=px(10))
    initials = (user["FirstName"][:1] + user["LastName"][:1]).upper()
    Label(card, text=initials, font=(FONT, 11, "bold"), fg=WHITE, bg=TEAL, width=3, pady=px(4)).pack(side=LEFT)
    names = Frame(card, bg=MENU_HOVER)
    names.pack(side=LEFT, padx=px(8))
    Label(names, text=user["FirstName"] + " " + user["LastName"], font=BOLD_FONT, fg=WHITE, bg=MENU_HOVER).pack(anchor="w")
    Label(names, text="@" + user["Username"] + "  •  Admin", font=SMALL_FONT, fg="#8FB5BC", bg=MENU_HOVER).pack(anchor="w")


# One button of the left menu (teal when it is the open page)
def make_menu_button(parent, item, active_page, badge):
    page_name = item[2]
    color = DEEP_TEAL
    if page_name == active_page:
        color = TEAL
    if page_name == "logout":
        command = user_pages.log_out
    else:
        command = lambda: helpers.go_to(page_name)
    button = Button(parent, text="  " + item[0] + "    " + item[1], command=command, bg=color, fg=WHITE,
                    relief=FLAT, bd=0, anchor="w", font=(FONT, 11, "bold"), activebackground=TEAL,
                    activeforeground=WHITE, cursor="hand2", pady=px(7))
    button.bind("<Enter>", on_menu_enter)
    button.bind("<Leave>", on_menu_leave)
    if badge > 0:
        Label(button, text=" " + str(badge) + " ", font=(FONT, 8, "bold"), fg=DEEP_TEAL,
              bg=GOLD).place(relx=1.0, x=-px(10), rely=0.5, anchor="e")
    return button


# The mouse is over a menu button: make it a bit lighter
def on_menu_enter(event):
    if event.widget["bg"] == DEEP_TEAL:
        event.widget.config(bg=MENU_HOVER)


# The mouse left a menu button: back to the normal color
def on_menu_leave(event):
    if event.widget["bg"] == MENU_HOVER:
        event.widget.config(bg=DEEP_TEAL)


# The white bar at the top with the page title and today's date
def build_admin_header(parent, title, subtitle):
    bar = Frame(parent, bg=WHITE, padx=px(24), pady=px(14))
    bar.pack(fill=X)
    Frame(parent, bg=BORDER, height=1).pack(fill=X)
    right = Frame(bar, bg=WHITE)
    right.pack(side=RIGHT)
    Label(right, text=helpers.today().strftime("%A"), font=SMALL_FONT, fg=GRAY, bg=WHITE).pack(anchor="e")
    Label(right, text=helpers.today().strftime("%B %d, %Y"), font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="e")
    Label(bar, text=title, font=TITLE_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    Label(bar, text=subtitle, font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w")


# A white card with a title. Returns (card, header, body); the header has room
# on the right for buttons, and the widgets go in the body.
def make_card(parent, title, note=""):
    card = Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    header = Frame(card, bg=WHITE)
    header.pack(fill=X, padx=px(16), pady=(px(12), px(8)))
    Label(header, text=title, font=(FONT, 12, "bold"), fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    if note != "":
        Label(header, text=note, font=SMALL_FONT, fg=GRAY, bg=WHITE).pack(side=LEFT, padx=px(8), pady=(px(3), 0))
    body = Frame(card, bg=WHITE)
    body.pack(fill=BOTH, expand=True, padx=px(16), pady=(0, px(14)))
    return card, header, body


# A Listbox with a Scrollbar inside a frame
def make_listbox(parent, height):
    box = Frame(parent, bg=WHITE)
    scrollbar = Scrollbar(box, orient=VERTICAL)
    listbox = Listbox(box, height=height, font=MONO_FONT, yscrollcommand=scrollbar.set, activestyle="none",
                      selectbackground=TEAL, selectforeground=WHITE, relief=FLAT, bd=0, highlightthickness=1,
                      highlightbackground=BORDER, highlightcolor=BORDER, exportselection=False)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    return box, listbox


# The gray header line above a Listbox (the column names)
def make_list_header(parent, text):
    Label(parent, text=text, font=("Consolas", 10, "bold"), fg=GRAY, bg=PAGE_BG, anchor="w",
          padx=3, pady=px(4)).pack(fill=X)


# Give a Listbox row its text color, and every second row a light background
def color_list_row(listbox, index, color):
    background = WHITE
    if index % 2 == 1:
        background = STRIPE
    listbox.itemconfig(index, bg=background, fg=color)


# Put text in a fixed-width column (for the Listbox rows)
def column(text, width, right=False):
    text = str(text)
    if len(text) > width:
        text = text[:width - 1] + "~"
    if right:
        return text.rjust(width) + " "
    return text.ljust(width) + " "


# A small colored label with a status, like "Pending"
def status_pill(parent, status):
    return Label(parent, text=" " + status + " ", font=(FONT, 8, "bold"), fg=WHITE,
                 bg=PILL_COLORS.get(status, GRAY), padx=px(4), pady=1)


# A colored button that is grayed out when the action is not allowed
def action_button(parent, text, command, enabled, color=TEAL):
    button = Button(parent, text=text, command=command, bg=color, fg=WHITE, relief=FLAT, bd=0,
                    font=BOLD_FONT, cursor="hand2", pady=px(5), activebackground=DARK_TEAL,
                    activeforeground=WHITE, disabledforeground=WHITE)
    if not enabled:
        button.config(state=DISABLED, bg="#C3D2D5", cursor="arrow")
    return button


# One "title: value" line in a details panel
def panel_line(parent, title, value):
    row = Frame(parent, bg=WHITE)
    row.pack(fill=X, pady=px(2))
    Label(row, text=title, font=BOLD_FONT, fg=GRAY, bg=WHITE, width=10, anchor="nw").pack(side=LEFT, anchor="n")
    Label(row, text=value, font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE, wraplength=px(200),
          justify=LEFT, anchor="w").pack(side=LEFT, fill=X)


# The page options for the bookings / discounts pages
# (status filter, search words and the row to select)
def page_options(data, default_status):
    options = {"status": default_status, "keyword": "", "select": None}
    if data is not None:
        options.update(data)
    return options


# Buttons like "Pending 3" to filter a list by status
def build_status_chips(parent, statuses, counts, active, page_name):
    row = Frame(parent, bg=PAGE_BG)
    row.pack(fill=X, pady=(0, px(12)))
    for status in statuses:
        make_chip(row, status, counts, active, page_name).pack(side=LEFT, padx=(0, px(8)))


# One filter button (teal when it is the chosen status)
def make_chip(parent, status, counts, active, page_name):
    if status == "All":
        count = sum(counts.values())
    else:
        count = counts.get(status, 0)
    background = WHITE
    color = DARK_TEAL
    if status == active:
        background = TEAL
        color = WHITE
    return Button(parent, text=status + "   " + str(count), bg=background, fg=color, relief=SOLID, bd=1,
                  font=BOLD_FONT, padx=px(14), pady=px(4), cursor="hand2", activebackground=LIGHT_TEAL,
                  command=lambda: helpers.go_to(page_name, {"status": status}))


# Select the row whose key has this value, and show it with show_function
def select_list_row(listbox, rows, key, value, show_function):
    number = 0
    for row in rows:
        if row[key] == value:
            listbox.selection_set(number)
            listbox.see(number)
            show_function(row)
        number = number + 1


# ======================= Dashboard =======================

# Numbers, quick buttons, a bar chart and the newest bookings
def show_dashboard_page(parent, data):
    database.auto_complete_bookings()
    name = helpers.current_user["FirstName"]
    content = build_admin_layout(parent, "admin_dashboard", "Dashboard",
                                 "Welcome back, " + name + "! Here is how LakbayPH is doing today.")
    stats = database.get_dashboard_stats()
    row = Frame(content, bg=PAGE_BG)
    row.pack(fill=X)
    make_stat_card(row, "Total Bookings", str(stats["TotalBookings"]), "all time", TEAL)
    make_stat_card(row, "Revenue", peso(stats["Revenue"]), "paid bookings", GREEN)
    make_stat_card(row, "Active Packages", str(stats["ActivePackages"]), "shown to customers", DARK_TEAL)
    make_stat_card(row, "Pending Bookings", str(stats["PendingBookings"]), "need confirming", GOLD)
    make_stat_card(row, "Discount Requests", str(stats["PendingDiscounts"]), "waiting for review", RED)
    build_quick_actions(content)
    lower = Frame(content, bg=PAGE_BG)
    lower.pack(fill=BOTH, expand=True, pady=(px(16), 0))
    lower.columnconfigure(0, weight=3)
    lower.columnconfigure(1, weight=2)
    lower.rowconfigure(0, weight=1)
    build_chart_card(lower)
    build_recent_card(lower)


# One white box with a colored strip, a big number and a title
def make_stat_card(parent, title, value, note, color):
    card = Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    card.pack(side=LEFT, fill=X, expand=True, padx=(0, px(12)))
    Frame(card, bg=color, width=px(5)).pack(side=LEFT, fill=Y)
    body = Frame(card, bg=WHITE, padx=px(14), pady=px(12))
    body.pack(side=LEFT, fill=BOTH, expand=True)
    Label(body, text=title.upper(), font=(FONT, 8, "bold"), fg=GRAY, bg=WHITE).pack(anchor="w")
    Label(body, text=value, font=(FONT, 18, "bold"), fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    Label(body, text=note, font=SMALL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w")


# Buttons for the things the admin does most
def build_quick_actions(parent):
    row = Frame(parent, bg=PAGE_BG)
    row.pack(fill=X, pady=(px(16), 0))
    Label(row, text="Quick actions:", font=BOLD_FONT, fg=DARK_TEAL, bg=PAGE_BG).pack(side=LEFT, padx=(0, px(10)))
    teal_button(row, "+ New Package", go_to_packages).pack(side=LEFT)
    light_button(row, "Pending Bookings", go_to_pending_bookings).pack(side=LEFT, padx=px(8))
    light_button(row, "Discount Requests", go_to_pending_discounts).pack(side=LEFT)
    light_button(row, "View Website", go_to_website).pack(side=LEFT, padx=px(8))


# Open the packages page
def go_to_packages():
    helpers.go_to("admin_packages")


# Open the bookings page with only the pending bookings
def go_to_pending_bookings():
    helpers.go_to("admin_bookings", {"status": "Pending"})


# Open the discount requests that are still pending
def go_to_pending_discounts():
    helpers.go_to("admin_discounts", {"status": "Pending"})


# Open the bookings page with all bookings
def go_to_all_bookings():
    helpers.go_to("admin_bookings")


# Open the customer website
def go_to_website():
    helpers.go_to("home")


# The card with the bar chart (it is drawn again when the window changes size)
def build_chart_card(parent):
    card, header, body = make_card(parent, "Bookings per package type", "cancelled bookings not counted")
    card.grid(row=0, column=0, sticky="nsew")
    lists["chart_rows"] = database.get_bookings_per_type()
    canvas = Canvas(body, height=px(260), bg=WHITE, highlightthickness=0)
    canvas.pack(fill=BOTH, expand=True)
    canvas.bind("<Configure>", on_chart_resize)


# The chart canvas changed size: draw it again
def on_chart_resize(event):
    draw_bar_chart(event.widget, lists["chart_rows"], event.width, event.height)


# A simple bar chart drawn on a Canvas
def draw_bar_chart(canvas, rows, width, height):
    canvas.delete("all")
    biggest = 1
    for row in rows:
        biggest = max(biggest, row["Total"])
    top = px(26)
    base_y = height - px(34)
    for step in range(4):
        y = base_y - (base_y - top) * step // 3
        canvas.create_line(px(10), y, width - px(10), y, fill=BORDER)
    slot = (width - px(20)) // max(1, len(rows))
    bar_width = min(px(110), slot * 55 // 100)
    colors = [TEAL, DARK_TEAL, GOLD]
    x = px(10) + slot // 2
    number = 0
    for row in rows:
        bar_height = row["Total"] * (base_y - top) // biggest
        canvas.create_rectangle(x - bar_width // 2, base_y - bar_height, x + bar_width // 2, base_y,
                                fill=colors[number % 3], outline="")
        canvas.create_text(x, base_y - bar_height - px(12), text=str(row["Total"]), font=BOLD_FONT, fill=DARK_TEAL)
        canvas.create_text(x, base_y + px(16), text=row["PackageType"], font=NORMAL_FONT, fill=DARK_TEAL)
        x = x + slot
        number = number + 1


# The card with the 6 newest bookings
def build_recent_card(parent):
    card, header, body = make_card(parent, "Recent bookings")
    card.grid(row=0, column=1, sticky="nsew", padx=(px(16), 0))
    Button(header, text="View all  ›", command=go_to_all_bookings, font=BOLD_FONT, fg=TEAL, bg=WHITE,
           relief=FLAT, bd=0, activebackground=WHITE, activeforeground=DARK_TEAL, cursor="hand2").pack(side=RIGHT)
    records = database.get_recent_bookings(6)
    if len(records) == 0:
        Label(body, text="No bookings yet.", font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(pady=px(30))
    for record in records:
        make_recent_row(body, record)


# One booking in the Recent bookings card
def make_recent_row(parent, record):
    row = Frame(parent, bg=WHITE)
    row.pack(fill=X, pady=px(5))
    right = Frame(row, bg=WHITE)
    right.pack(side=RIGHT)
    status_pill(right, record["Status"]).pack(anchor="e")
    Label(right, text=peso(record["TotalAmount"]), font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="e")
    Label(row, text=record["BookingReference"], font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    Label(row, text=record["FirstName"] + " " + record["LastName"] + "  •  " + record["Title"], font=SMALL_FONT,
          fg=GRAY, bg=WHITE, wraplength=px(260), justify=LEFT).pack(anchor="w")
    Frame(parent, bg=BORDER, height=1).pack(fill=X)


# ======================= Packages: list (Read) =======================

# The packages page: list on the left, form on the right
def show_packages_page(parent, data):
    content = build_admin_layout(parent, "admin_packages", "Packages",
                                 "Create, edit and delete tour packages, their pictures and add-ons")
    content.columnconfigure(1, weight=1)
    content.rowconfigure(0, weight=1)
    list_card, list_header, list_body = make_card(content, "All Packages")
    list_card.grid(row=0, column=0, sticky="ns")
    form_card = Frame(content, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    form_card.grid(row=0, column=1, sticky="nsew", padx=(px(16), 0))
    build_package_list(list_header, list_body)
    build_form_top_bar(form_card)
    build_package_form(make_scroll_area(form_card))
    refresh_package_list()
    clear_form()
    if data is not None:
        select_package(data)


# The search box, the Listbox and the New / Delete buttons
def build_package_list(header, parent):
    form["list_count"] = Label(header, text="", font=SMALL_FONT, fg=GRAY, bg=WHITE)
    form["list_count"].pack(side=RIGHT, pady=(px(3), 0))
    row = Frame(parent, bg=WHITE)
    row.pack(fill=X, pady=(0, px(8)))
    Label(row, text="Search", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    form["search"] = StringVar()
    search_entry = Entry(row, textvariable=form["search"], font=NORMAL_FONT, relief=SOLID, bd=1)
    search_entry.pack(side=LEFT, fill=X, expand=True, padx=(px(8), 0), ipady=3)
    search_entry.bind("<KeyRelease>", on_search_typed)
    make_list_header(parent, column("ID", 3, True) + column("Title", 21) + column("Price", 7, True) +
                     column("Pics", 4, True) + "On")
    box, form["package_list"] = make_listbox(parent, 20)
    box.pack(fill=BOTH, expand=True)
    form["package_list"].config(width=43)
    form["package_list"].bind("<<ListboxSelect>>", on_package_select)
    buttons = Frame(parent, bg=WHITE)
    buttons.pack(fill=X, pady=(px(10), 0))
    teal_button(buttons, "+ New Package", clear_form).pack(side=LEFT)
    action_button(buttons, "Delete", delete_package, True, RED).pack(side=RIGHT, ipadx=px(10))


# Typing in the search box filters the list
def on_search_typed(event):
    refresh_package_list()
    keep_list_selection()


# The text of one package in the list
def package_line(package):
    shown = "Yes"
    if package["IsActive"] != 1 or package["Status"] != "active":
        shown = "No"
    return (column(package["PackageID"], 3, True) + column(package["Title"], 21) +
            column(format(package["Price"], ",.0f"), 7, True) + column(package["ImageCount"], 4, True) + shown)


# Fill the Listbox with the packages that match the search
def refresh_package_list():
    global package_rows
    keyword = form["search"].get().strip().lower()
    package_rows = []
    listbox = form["package_list"]
    listbox.delete(0, END)
    for package in database.get_all_packages():
        words = (str(package["PackageID"]) + " " + package["Title"] + " " + package["PackageType"] + " " +
                 str(package["Location"])).lower()
        if keyword != "" and keyword not in words:
            continue
        listbox.insert(END, package_line(package))
        color = DARK_TEAL
        if package["IsActive"] != 1 or package["Status"] != "active":
            color = GRAY
        color_list_row(listbox, len(package_rows), color)
        package_rows.append(package)
    form["list_count"].config(text=str(len(package_rows)) + " shown")


# Select the package that is in the form again (without loading it again)
def keep_list_selection():
    number = 0
    for package in package_rows:
        if package["PackageID"] == editing_id:
            form["package_list"].selection_set(number)
            form["package_list"].see(number)
        number = number + 1


# A package was clicked in the list: show it in the form
def on_package_select(event):
    selection = form["package_list"].curselection()
    if len(selection) == 0:
        return
    load_package_into_form(package_rows[selection[0]])


# Select a package in the list by its ID (after saving)
def select_package(package_id):
    select_list_row(form["package_list"], package_rows, "PackageID", package_id, load_package_into_form)


# ======================= Packages: form (Create / Update) =======================

# The bar above the form: title, and the Save / Clear / View buttons
def build_form_top_bar(card):
    bar = Frame(card, bg=WHITE, padx=px(18), pady=px(12))
    bar.pack(fill=X)
    Frame(card, bg=BORDER, height=1).pack(fill=X)
    form["form_title"] = Label(bar, text="New Package", font=HEADING_FONT, fg=DARK_TEAL, bg=WHITE, anchor="w")
    form["form_title"].pack(fill=X)
    form["form_note"] = Label(bar, text="", font=SMALL_FONT, fg=GRAY, bg=WHITE, anchor="w")
    form["form_note"].pack(fill=X)
    buttons = Frame(bar, bg=WHITE)
    buttons.pack(fill=X, pady=(px(8), 0))
    teal_button(buttons, "Save Package", save_package_form).pack(side=LEFT)
    light_button(buttons, "Clear Form", clear_form).pack(side=LEFT, padx=px(8))
    form["view_button"] = light_button(buttons, "View on Website", view_on_website)
    form["view_button"].pack(side=LEFT)


# A section of the form: a title, a line, and a grid for the fields
def form_section(parent, title, note=""):
    Label(parent, text=title, font=(FONT, 12, "bold"), fg=TEAL, bg=WHITE).pack(anchor="w", pady=(px(16), 0))
    if note != "":
        Label(parent, text=note, font=SMALL_FONT, fg=GRAY, bg=WHITE, wraplength=px(380),
              justify=LEFT).pack(anchor="w")
    Frame(parent, bg=BORDER, height=1).pack(fill=X, pady=(px(4), px(8)))
    grid = Frame(parent, bg=WHITE)
    grid.pack(fill=X)
    grid.columnconfigure(1, weight=1)
    return grid


# A label in the first column of the form
def form_label(parent, text, row):
    Label(parent, text=text, font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE, anchor="nw", width=11).grid(
        row=row, column=0, sticky="nw", pady=px(5), padx=(0, px(10)))


# A one-line Entry in the second column of the form (stretches with the window)
def form_text_entry(parent, key, row, stretch=True):
    form[key] = StringVar()
    entry = Entry(parent, textvariable=form[key], width=16, font=NORMAL_FONT, relief=SOLID, bd=1)
    sticky = "w"
    if stretch:
        sticky = "ew"
    entry.grid(row=row, column=1, sticky=sticky, pady=px(5), ipady=3)


# The whole package form
def build_package_form(parent):
    page = Frame(parent, bg=WHITE, padx=px(22), pady=px(2))
    page.pack(fill=BOTH, expand=True)
    build_form_basics(form_section(page, "Basic information"))
    build_form_numbers(form_section(page, "Schedule and slots"))
    build_form_texts(form_section(page, "Trip details", "Inclusions and highlights: write one per line"))
    build_form_pictures(form_section(page, "Pictures", "The main picture is shown on the cards; all pictures are shown on the package page"))
    build_form_addons(form_section(page, "Add-ons", "Extra things customers can add (saved when you click Save Package)"))
    Frame(page, bg=WHITE, height=px(20)).pack()


# Title, type, category, price and description
def build_form_basics(grid):
    form_label(grid, "Title *", 0)
    form_text_entry(grid, "title", 0)
    form_label(grid, "Type *", 1)
    form["type"] = StringVar(value="Domestic")
    types = Frame(grid, bg=WHITE)
    types.grid(row=1, column=1, sticky="w")
    for name in PACKAGE_TYPES:
        Radiobutton(types, text=name, value=name, variable=form["type"], bg=WHITE, fg=DARK_TEAL,
                    activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT, padx=(0, px(10)))
    form_label(grid, "Category *", 2)
    form["category"] = StringVar()
    form["category_names"] = []
    for category in database.get_categories():
        form["category_names"].append(str(category["CategoryID"]) + " - " + category["CategoryName"] + " (" + category["CategoryType"] + ")")
    make_choice_menu(grid, form["category"], form["category_names"], None, 20).grid(row=2, column=1, sticky="ew", pady=px(5))
    form_label(grid, "Price (₱) *", 3)
    form_text_entry(grid, "price", 3, False)
    form_label(grid, "Description *", 4)
    form_text_entry(grid, "description", 4)


# A Spinbox for a number
def form_spinbox(parent, key, low, high):
    form[key] = StringVar()
    spinbox = Spinbox(parent, from_=low, to=high, textvariable=form[key], width=6, font=NORMAL_FONT)
    return spinbox


# A small gray label between the fields of one row
def small_field_label(parent, text):
    Label(parent, text=text, font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(side=LEFT, padx=(px(6), px(4)))


# Duration, nights, slots, group package, status, active and the dates
def build_form_numbers(grid):
    form_label(grid, "Duration", 0)
    row = Frame(grid, bg=WHITE)
    row.grid(row=0, column=1, sticky="w", pady=px(5))
    form_spinbox(row, "duration", 1, 60).pack(side=LEFT)
    small_field_label(row, "days")
    form_spinbox(row, "nights", 0, 60).pack(side=LEFT, padx=(px(10), 0))
    small_field_label(row, "nights")
    form_label(grid, "Slots", 1)
    row2 = Frame(grid, bg=WHITE)
    row2.grid(row=1, column=1, sticky="w", pady=px(5))
    form_spinbox(row2, "max_slots", 1, 500).pack(side=LEFT)
    small_field_label(row2, "people per travel date")
    form_label(grid, "Group", 2)
    row3 = Frame(grid, bg=WHITE)
    row3.grid(row=2, column=1, sticky="w", pady=px(5))
    form["is_group"] = IntVar()
    Checkbutton(row3, text="Group package, size:", variable=form["is_group"], bg=WHITE, fg=DARK_TEAL,
                activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT)
    form_spinbox(row3, "group_size", 1, 500).pack(side=LEFT)
    build_form_status(grid)
    build_form_dates(grid)


# Status (active / inactive) and "Is active (not deleted)"
def build_form_status(grid):
    form_label(grid, "Status", 3)
    row = Frame(grid, bg=WHITE)
    row.grid(row=3, column=1, sticky="w", pady=px(5))
    form["status"] = StringVar(value="active")
    for status in ["active", "inactive"]:
        Radiobutton(row, text=status, value=status, variable=form["status"], bg=WHITE, fg=DARK_TEAL,
                    activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT, padx=(0, px(8)))
    form_label(grid, "Visible", 4)
    form["is_active"] = IntVar(value=1)
    Checkbutton(grid, text="Is active (not deleted)", variable=form["is_active"], bg=WHITE, fg=DARK_TEAL,
                activebackground=WHITE, font=NORMAL_FONT).grid(row=4, column=1, sticky="w", pady=px(5))


# Start and end dates (3 Spinboxes each)
def build_form_dates(grid):
    form_label(grid, "Start date", 5)
    start_row = Frame(grid, bg=WHITE)
    start_row.grid(row=5, column=1, sticky="w", pady=px(5))
    form["start"] = make_date_spinboxes(start_row, helpers.today())
    form_label(grid, "End date", 6)
    end_row = Frame(grid, bg=WHITE)
    end_row.grid(row=6, column=1, sticky="w", pady=px(5))
    form["end"] = make_date_spinboxes(end_row, helpers.one_year_from(helpers.today()))


# Location, ideal for, inclusions and highlights
def build_form_texts(grid):
    form_label(grid, "Location *", 0)
    form_text_entry(grid, "location", 0)
    form_label(grid, "Ideal for", 1)
    form_text_entry(grid, "ideal_for", 1)
    form_label(grid, "Inclusions", 2)
    form["inclusions"] = Text(grid, width=30, height=6, font=NORMAL_FONT, relief=SOLID, bd=1, wrap=WORD)
    form["inclusions"].grid(row=2, column=1, sticky="ew", pady=px(5))
    form_label(grid, "Highlights", 3)
    form["highlights"] = Text(grid, width=30, height=4, font=NORMAL_FONT, relief=SOLID, bd=1, wrap=WORD)
    form["highlights"].grid(row=3, column=1, sticky="ew", pady=px(5))


# The pictures: a big preview, the buttons, and all pictures of the package
def build_form_pictures(grid):
    top = Frame(grid, bg=WHITE)
    top.grid(row=0, column=0, columnspan=2, sticky="ew")
    form["image_preview"] = Label(top, bg=LIGHT_GRAY)
    form["image_preview"].pack(side=LEFT, anchor="n")
    side = Frame(top, bg=WHITE, padx=px(16))
    side.pack(side=LEFT, fill=BOTH, expand=True)
    form["image_label"] = Label(side, text="", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE, justify=LEFT,
                                anchor="w", wraplength=px(150))
    form["image_label"].pack(fill=X)
    form["image_count"] = Label(side, text="", font=SMALL_FONT, fg=GRAY, bg=WHITE, anchor="w",
                                wraplength=px(150), justify=LEFT)
    form["image_count"].pack(fill=X)
    form["thumbs"] = Frame(grid, bg=WHITE)
    form["thumbs"].grid(row=1, column=0, columnspan=2, sticky="w", pady=(px(12), 0))
    build_picture_buttons(grid)
    form["images"] = []
    form["cover"] = None
    form["selected_image"] = None


# Upload / Set as Main / Remove / Import Folder (under the small pictures)
def build_picture_buttons(grid):
    buttons = Frame(grid, bg=WHITE)
    buttons.grid(row=2, column=0, columnspan=2, sticky="w", pady=(px(4), px(6)))
    teal_button(buttons, "+ Upload Pictures", upload_images).pack(side=LEFT)
    light_button(buttons, "★ Set as Main", set_main_picture).pack(side=LEFT, padx=px(6))
    light_button(buttons, "Remove", remove_picture).pack(side=LEFT)
    light_button(grid, "Import Folder", import_image_folder).grid(row=3, column=0, columnspan=2, sticky="w")
    Label(grid, text="Tip: hold Ctrl or Shift to choose many pictures at once. Import Folder copies the pictures "
          "whose names match a package: fdbasic.jpg is the main picture and fdbasic_2.jpg, fdbasic_3.jpg ... "
          "are more pictures.", font=SMALL_FONT, fg=GRAY, bg=WHITE, justify=LEFT,
          wraplength=px(380)).grid(row=4, column=0, columnspan=2, sticky="w", pady=(px(6), 0))


# The add-ons list with Add / Update / Remove
def build_form_addons(grid):
    box = Frame(grid, bg=WHITE)
    box.grid(row=0, column=0, columnspan=2, sticky="ew")
    make_list_header(box, column("Name", 30) + column("Price", 10, True) + "Unit")
    list_box, form["addon_list"] = make_listbox(box, 5)
    list_box.pack(fill=X)
    form["addon_list"].bind("<<ListboxSelect>>", on_addon_select)
    entries = Frame(box, bg=WHITE)
    entries.pack(fill=X, pady=px(8))
    form["addon_name"] = StringVar()
    form["addon_price"] = StringVar()
    form["addon_unit"] = StringVar()
    for item in [("Name", "addon_name", 20), ("Price", "addon_price", 8), ("Unit", "addon_unit", 10)]:
        Label(entries, text=item[0], font=SMALL_FONT, fg=GRAY, bg=WHITE).pack(side=LEFT)
        Entry(entries, textvariable=form[item[1]], width=item[2], font=NORMAL_FONT, relief=SOLID, bd=1).pack(side=LEFT, padx=(px(4), px(10)), ipady=2)
    buttons = Frame(box, bg=WHITE)
    buttons.pack(fill=X)
    light_button(buttons, "Add", add_addon).pack(side=LEFT)
    light_button(buttons, "Update", update_addon).pack(side=LEFT, padx=px(6))
    light_button(buttons, "Remove", remove_addon).pack(side=LEFT)


# Empty the form for a new package
def clear_form():
    global editing_id
    editing_id = None
    form["form_title"].config(text="New Package")
    form["form_note"].config(text="Fill in the form and click Save Package. You can add pictures after saving.")
    form["view_button"].config(state=DISABLED)
    for key in ["title", "price", "description", "location", "ideal_for"]:
        form[key].set("")
    form["type"].set("Domestic")
    form["category"].set(form["category_names"][0])
    form["duration"].set("3")
    form["nights"].set("2")
    form["max_slots"].set("20")
    form["group_size"].set("1")
    form["is_group"].set(0)
    form["status"].set("active")
    form["is_active"].set(1)
    set_date_spinboxes(form["start"], helpers.today())
    set_date_spinboxes(form["end"], helpers.one_year_from(helpers.today()))
    form["inclusions"].delete("1.0", END)
    form["highlights"].delete("1.0", END)
    form["package_list"].selection_clear(0, END)
    load_addons_into_form([])
    form["selected_image"] = None
    refresh_gallery()


# Show a package in the form so it can be edited
def load_package_into_form(package):
    global editing_id
    editing_id = package["PackageID"]
    form["form_title"].config(text="Editing package #" + str(editing_id) + "  -  " + package["Title"])
    form["form_note"].config(text="Last changed " + str(package["UpdatedAt"])[:16] + ". Click Save Package to keep your changes.")
    form["view_button"].config(state=NORMAL)
    form["title"].set(package["Title"])
    form["type"].set(package["PackageType"])
    for name in form["category_names"]:
        if name.startswith(str(package["CategoryID"]) + " - "):
            form["category"].set(name)
    form["price"].set(format(package["Price"], ".2f"))
    form["description"].set(package["Description"])
    form["duration"].set(str(package["Duration"]))
    form["nights"].set(str(package["DurationNights"]))
    form["max_slots"].set(str(package["MaxSlots"]))
    form["group_size"].set(str(package["GroupSize"] or 1))
    form["is_group"].set(package["IsGroupPackage"])
    form["status"].set(package["Status"] or "active")
    form["is_active"].set(package["IsActive"])
    set_date_spinboxes(form["start"], text_to_date(package["StartDate"]))
    set_date_spinboxes(form["end"], text_to_date(package["EndDate"]))
    form["location"].set(package["Location"] or "")
    form["ideal_for"].set(package["IdealFor"] or "")
    set_text_box(form["inclusions"], split_list_text(package["Inclusions"]))
    set_text_box(form["highlights"], split_list_text(package["Highlights"]))
    form["selected_image"] = None
    refresh_gallery()
    load_addons_into_form(database.get_addons(editing_id))


# Put a list of lines into a Text box
def set_text_box(text_box, lines):
    text_box.delete("1.0", END)
    text_box.insert("1.0", "\n".join(lines))


# Read the lines of a Text box (empty lines are skipped), joined with new lines
def read_text_box(text_box):
    lines = []
    for line in text_box.get("1.0", END).split("\n"):
        if line.strip() != "":
            lines.append(line.strip())
    return "\n".join(lines)


# Read and check the number fields. Returns (numbers, "") or (None, problem).
def read_form_numbers():
    price = read_float(form["price"].get())
    duration = read_int(form["duration"].get())
    nights = read_int(form["nights"].get())
    max_slots = read_int(form["max_slots"].get())
    group_size = read_int(form["group_size"].get())
    if price is None or price <= 0:
        return None, "The price must be a number more than 0."
    if duration is None or duration < 1:
        return None, "The duration must be at least 1 day."
    if nights is None or nights < 0 or nights > duration:
        return None, "Nights must be from 0 up to the number of days."
    if max_slots is None or max_slots < 1:
        return None, "Max slots must be at least 1."
    if group_size is None or group_size < 1:
        return None, "Group size must be at least 1."
    return {"Price": price, "Duration": duration, "DurationNights": nights,
            "MaxSlots": max_slots, "GroupSize": group_size}, ""


# Read and check the whole form. Returns (package, "") or (None, problem).
def read_package_form():
    title = form["title"].get().strip()
    description = form["description"].get().strip()
    location = form["location"].get().strip()
    if title == "" or description == "" or location == "":
        return None, "Please fill in the title, description and location."
    if len(description) > 200:
        return None, "The description can only have 200 characters (it has " + str(len(description)) + ")."
    package, problem = read_form_numbers()
    if problem != "":
        return None, problem
    start = read_date_spinboxes(form["start"])
    end = read_date_spinboxes(form["end"])
    if start is None or end is None or end < start:
        return None, "Please choose real start and end dates (the end cannot be before the start)."
    package["Title"] = title
    package["Description"] = description
    package["Location"] = location
    package["PackageType"] = form["type"].get()
    package["CategoryID"] = int(form["category"].get().split(" - ")[0])
    package["StartDate"] = date_to_text(start)
    package["EndDate"] = date_to_text(end)
    package["Status"] = form["status"].get()
    package["IsGroupPackage"] = form["is_group"].get()
    package["IsActive"] = form["is_active"].get()
    package["IdealFor"] = none_if_empty(form["ideal_for"].get())
    package["Inclusions"] = read_text_box(form["inclusions"])
    package["Highlights"] = read_text_box(form["highlights"])
    return package, ""


# Save the form (new package or changes to the selected one)
def save_package_form():
    if not require_admin():
        return
    package, problem = read_package_form()
    if problem != "":
        messagebox.showwarning("Save Package", problem)
        return
    try:
        package_id = database.save_package(package, form_addons, editing_id)
    except Exception as error:
        show_error("Could not save the package. Nothing was changed.", error)
        return
    message = "Package #" + str(package_id) + " was saved."
    if editing_id is None:
        message = message + "\n\nYou can now upload its pictures."
    messagebox.showinfo("Save Package", message)
    helpers.go_to("admin_packages", package_id)


# Open the package page on the customer website
def view_on_website():
    if editing_id is not None:
        helpers.go_to("details", editing_id)


# ======================= Packages: Delete =======================

# Soft delete: the package is hidden (IsActive = 0), bookings are kept
def delete_package():
    if not require_admin():
        return
    if editing_id is None:
        messagebox.showwarning("Delete Package", "Please choose a package in the list first.")
        return
    question = ("Delete package #" + str(editing_id) + " - " + form["title"].get() + "?\n\n"
                "It will be hidden from customers. Old bookings are kept.")
    if not messagebox.askyesno("Delete Package", question):
        return
    try:
        database.soft_delete_package(editing_id)
    except Exception as error:
        show_error("Could not delete the package.", error)
        return
    messagebox.showinfo("Delete Package", "The package was deleted (hidden).")
    helpers.go_to("admin_packages", editing_id)


# ======================= Packages: add-ons =======================

# Copy the add-ons of a package into the form list
def load_addons_into_form(addons):
    form_addons.clear()
    for addon in addons:
        form_addons.append({"AddOnID": addon["AddOnID"], "AddOnName": addon["AddOnName"],
                            "Price": addon["Price"], "Unit": addon["Unit"], "Removed": False})
    refresh_addon_list()


# Show the add-ons that are not removed
def refresh_addon_list():
    form["addon_list"].delete(0, END)
    form["addon_rows"] = []
    number = 0
    for addon in form_addons:
        if not addon["Removed"]:
            text = column(addon["AddOnName"], 30) + column(format(addon["Price"], ",.2f"), 10, True) + str(addon["Unit"] or "")
            form["addon_list"].insert(END, text)
            color_list_row(form["addon_list"], len(form["addon_rows"]), DARK_TEAL)
            form["addon_rows"].append(number)
        number = number + 1


# The add-on that is selected in the list (or None)
def selected_addon():
    selection = form["addon_list"].curselection()
    if len(selection) == 0:
        messagebox.showwarning("Add-ons", "Please choose an add-on in the list first.")
        return None
    return form_addons[form["addon_rows"][selection[0]]]


# An add-on was clicked: put it in the boxes
def on_addon_select(event):
    selection = form["addon_list"].curselection()
    if len(selection) == 0:
        return
    addon = form_addons[form["addon_rows"][selection[0]]]
    form["addon_name"].set(addon["AddOnName"])
    form["addon_price"].set(format(addon["Price"], ".2f"))
    form["addon_unit"].set(addon["Unit"] or "")


# Read the add-on boxes. Returns (name, price, unit) or None if wrong.
def read_addon_boxes():
    name = form["addon_name"].get().strip()
    price = read_float(form["addon_price"].get())
    if name == "" or price is None or price < 0:
        messagebox.showwarning("Add-ons", "Please enter the add-on name and a price (0 or more).")
        return None
    return (name, price, none_if_empty(form["addon_unit"].get()))


# Add a new add-on to the list
def add_addon():
    values = read_addon_boxes()
    if values is None:
        return
    form_addons.append({"AddOnID": None, "AddOnName": values[0], "Price": values[1], "Unit": values[2], "Removed": False})
    for key in ["addon_name", "addon_price", "addon_unit"]:
        form[key].set("")
    refresh_addon_list()


# Change the selected add-on
def update_addon():
    addon = selected_addon()
    values = read_addon_boxes()
    if addon is None or values is None:
        return
    addon["AddOnName"] = values[0]
    addon["Price"] = values[1]
    addon["Unit"] = values[2]
    refresh_addon_list()


# Remove the selected add-on (hidden in the database when saved)
def remove_addon():
    addon = selected_addon()
    if addon is None:
        return
    if addon["AddOnID"] is None:
        form_addons.remove(addon)
    else:
        addon["Removed"] = True
    refresh_addon_list()


# ======================= Packages: pictures =======================

# Load the pictures of the package from the database and show them
def refresh_gallery():
    for widget in form["thumbs"].winfo_children():
        widget.destroy()
    # An empty frame keeps its old size in Tk, so make it small again
    form["thumbs"].config(width=1, height=1)
    form["images"] = []
    form["cover"] = None
    if editing_id is not None:
        for row in database.get_package_images(editing_id):
            form["images"].append(row["ImageFileName"])
        form["cover"] = database.get_package(editing_id)["ImageFileName"]
    if form["selected_image"] not in form["images"]:
        form["selected_image"] = form["cover"]
    number = 0
    for file_name in form["images"]:
        make_form_thumb(form["thumbs"], file_name).grid(row=number // 6, column=number % 6,
                                                        padx=(0, px(10)), pady=(0, px(8)))
        number = number + 1
    show_image_preview()


# One small picture (teal border = chosen, "Main picture" under the main one)
def make_form_thumb(parent, file_name):
    box = Frame(parent, bg=WHITE)
    color = BORDER
    if file_name == form["selected_image"]:
        color = TEAL
    Button(box, image=load_image(file_name, px(104), px(66)), command=lambda: select_form_image(file_name),
           bg=color, relief=FLAT, bd=0, padx=3, pady=3, activebackground=TEAL, cursor="hand2").pack()
    caption = ""
    if file_name == form["cover"]:
        caption = "★ Main picture"
    Label(box, text=caption, font=(FONT, 8, "bold"), fg=DARK_GOLD, bg=WHITE).pack()
    return box


# A small picture was clicked: show it big
def select_form_image(file_name):
    form["selected_image"] = file_name
    refresh_gallery()


# Show the chosen picture big, with its file name
def show_image_preview():
    file_name = form["selected_image"]
    form["image_preview"].config(image=load_image(file_name, px(240), px(150)))
    count = str(len(form["images"])) + " picture(s)"
    if editing_id is None:
        text = "Save the package first, then upload its pictures."
        count = ""
    elif file_name is None:
        text = "No pictures yet. Click Upload Pictures to add some."
    else:
        text = file_name
        if file_name == form["cover"]:
            text = text + "  (main picture)"
        if find_image_path(file_name).endswith("placeholder.jpg"):
            text = text + "\nThe file is missing, so a placeholder is shown."
    form["image_label"].config(text=text)
    form["image_count"].config(text=count)


# Copy a picture into the app's images folder. Returns the file name used.
def copy_image_file(file_path):
    folder = get_images_folder()   # makes the folder with os.mkdir if it is missing
    file_name = os.path.basename(file_path)
    target = os.path.join(folder, file_name)
    if os.path.abspath(file_path).lower() == os.path.abspath(target).lower():
        return file_name
    # Do not overwrite another picture with the same name
    base, extension = os.path.splitext(file_name)
    number = 2
    while os.path.exists(target):
        file_name = base + "_" + str(number) + extension
        target = os.path.join(folder, file_name)
        number = number + 1
    shutil.copy(file_path, target)
    return file_name


# Stop with a message if no package is open in the form
def package_is_open(title):
    if editing_id is None:
        messagebox.showwarning(title, "Please save the package first (or choose one in the list).")
        return False
    return True


# Upload Pictures: choose one or more png/jpg/jpeg files and add them to this package
def upload_images():
    if not require_admin() or not package_is_open("Upload Pictures"):
        return
    file_paths = filedialog.askopenfilenames(title="Choose one or more pictures",
                                             filetypes=[("Pictures", "*.png *.jpg *.jpeg")])
    if not file_paths:
        return
    file_names = []
    try:
        for file_path in file_paths:
            if file_path.lower().endswith(IMAGE_TYPES):
                file_names.append(copy_image_file(file_path))
        database.add_package_images(editing_id, file_names)
    except Exception as error:
        show_error("Could not add the pictures.", error)
        return
    if len(file_names) == 0:
        messagebox.showwarning("Upload Pictures", "Please choose .png, .jpg or .jpeg files.")
        return
    form["selected_image"] = file_names[0]
    after_picture_change()
    messagebox.showinfo("Upload Pictures", str(len(file_names)) + " picture(s) were added to package #" + str(editing_id) + ".")


# Show the new pictures in the form and the new picture count in the list
def after_picture_change():
    refresh_gallery()
    refresh_package_list()
    keep_list_selection()


# Make the chosen picture the main picture (shown on the cards)
def set_main_picture():
    if not require_admin() or not package_is_open("Set as Main"):
        return
    if form["selected_image"] is None:
        messagebox.showwarning("Set as Main", "Please click a picture first.")
        return
    try:
        database.set_package_image(editing_id, form["selected_image"])
    except Exception as error:
        show_error("Could not change the main picture.", error)
        return
    after_picture_change()


# Remove the chosen picture from the package (the file itself is kept)
def remove_picture():
    if not require_admin() or not package_is_open("Remove Picture"):
        return
    file_name = form["selected_image"]
    if file_name is None:
        messagebox.showwarning("Remove Picture", "Please click a picture first.")
        return
    if not messagebox.askyesno("Remove Picture", "Remove " + file_name + " from this package?"):
        return
    try:
        database.remove_package_image(editing_id, file_name)
    except Exception as error:
        show_error("Could not remove the picture.", error)
        return
    form["selected_image"] = None
    after_picture_change()


# Import Folder: copy every picture whose name matches a package picture
def import_image_folder():
    if not require_admin():
        return
    folder = filedialog.askdirectory(title="Choose the folder with the package pictures")
    if folder == "":
        return
    try:
        result = copy_matching_images(folder)
    except Exception as error:
        show_error("Could not import the pictures.", error)
        return
    clear_image_cache()
    message = str(result[0]) + " picture(s) were imported."
    if len(result[1]) > 0:
        message = message + "\n\nNo picture found for: " + ", ".join(result[1][:12])
        if len(result[1]) > 12:
            message = message + " and " + str(len(result[1]) - 12) + " more"
    messagebox.showinfo("Import Folder", message)
    helpers.go_to("admin_packages", editing_id)


# Copy the matching pictures (main + more pictures of each package).
# Returns (number copied, list of names not found).
def copy_matching_images(folder):
    files_in_folder = {}
    for name in os.listdir(folder):
        if name.lower().endswith(IMAGE_TYPES):
            files_in_folder[name.lower()] = name
    copied = 0
    not_found = []
    for row in database.get_image_file_names():
        wanted = row["ImageFileName"]
        if not wanted:
            continue
        found = find_matching_file(files_in_folder, wanted)
        file_names = find_extra_files(files_in_folder, wanted)
        if found is None and len(file_names) == 0:
            not_found.append(wanted)
            continue
        if found is not None:
            file_names.insert(0, found)
        for name in file_names:
            shutil.copy(os.path.join(folder, name), os.path.join(get_images_folder(), name))
        if found is not None and found != wanted:
            database.rename_package_image(row["PackageID"], wanted, found)
        database.add_package_images(row["PackageID"], file_names)
        copied = copied + len(file_names)
    return (copied, not_found)


# Find "fdbasic.jpg" in the folder (same name, or same name with another picture type)
def find_matching_file(files_in_folder, wanted):
    if wanted.lower() in files_in_folder:
        return files_in_folder[wanted.lower()]
    wanted_base = os.path.splitext(wanted.lower())[0]
    for extension in IMAGE_TYPES:
        if wanted_base + extension in files_in_folder:
            return files_in_folder[wanted_base + extension]
    return None


# Find the extra pictures of "fdbasic.jpg": fdbasic_2.jpg, fdbasic_beach.png, ...
def find_extra_files(files_in_folder, wanted):
    start = os.path.splitext(wanted.lower())[0] + "_"
    extras = []
    for lower_name in sorted(files_in_folder.keys()):
        if lower_name.startswith(start):
            extras.append(files_in_folder[lower_name])
    return extras


# ======================= Bookings =======================

# All bookings with status buttons, a search box and a details panel
def show_bookings_page(parent, data):
    database.auto_complete_bookings()
    options = page_options(data, "All")
    content = build_admin_layout(parent, "admin_bookings", "Bookings",
                                 "Confirm, complete, cancel and mark bookings as paid")
    lists["booking_status"] = options["status"]
    build_status_chips(content, BOOKING_STATUSES, database.get_booking_counts(), options["status"], "admin_bookings")
    body = Frame(content, bg=PAGE_BG)
    body.pack(fill=BOTH, expand=True)
    list_card, header, list_body = make_card(body, "Booking list", "double-click to see the receipt")
    list_card.pack(side=LEFT, fill=BOTH, expand=True)
    panel_card, panel_header, lists["panel"] = make_card(body, "Booking details")
    panel_card.config(width=px(370))
    panel_card.pack_propagate(False)
    panel_card.pack(side=LEFT, fill=Y, padx=(px(16), 0))
    build_bookings_list(header, list_body, options["keyword"])
    lists["all_bookings"] = database.get_all_bookings(options["status"])
    fill_bookings_list()
    select_list_row(lists["bookings"], booking_rows, "BookingID", options["select"], show_booking_panel)


# The search box and the Listbox of bookings
def build_bookings_list(header, parent, keyword):
    lists["booking_search"] = StringVar(value=keyword)
    entry = Entry(header, textvariable=lists["booking_search"], width=20, font=NORMAL_FONT, relief=SOLID, bd=1)
    entry.pack(side=RIGHT, ipady=2)
    entry.bind("<KeyRelease>", on_booking_search)
    Label(header, text="Search", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=RIGHT, padx=(0, px(6)))
    make_list_header(parent, column("Reference", 17) + column("Customer", 15) + column("Travel", 10) +
                     column("Total", 9, True) + column("Status", 9) + "Package")
    box, lists["bookings"] = make_listbox(parent, 16)
    box.pack(fill=BOTH, expand=True)
    lists["bookings"].bind("<<ListboxSelect>>", on_booking_select)
    lists["bookings"].bind("<Double-Button-1>", on_booking_double_click)


# Typing in the search box filters the list
def on_booking_search(event):
    fill_bookings_list()


# Fill the bookings Listbox (only the ones that match the search words)
def fill_bookings_list():
    global booking_rows
    keyword = lists["booking_search"].get().strip().lower()
    booking_rows = []
    listbox = lists["bookings"]
    listbox.delete(0, END)
    for record in lists["all_bookings"]:
        words = (record["BookingReference"] + " " + record["FirstName"] + " " + record["LastName"] + " " + record["Title"]).lower()
        if keyword != "" and keyword not in words:
            continue
        text = (column(record["BookingReference"], 17) + column(record["FirstName"] + " " + record["LastName"], 15) +
                column(record["TravelDate"], 10) + column(format(record["TotalAmount"], ",.0f"), 9, True) +
                column(record["Status"], 9) + record["Title"])
        listbox.insert(END, text)
        color_list_row(listbox, len(booking_rows), ROW_COLORS.get(record["Status"], DARK_TEAL))
        booking_rows.append(record)
    if len(booking_rows) == 0:
        listbox.insert(END, "  (no bookings)")
    show_booking_panel(None)


# A booking was clicked: show it in the details panel
def on_booking_select(event):
    selection = lists["bookings"].curselection()
    if len(selection) == 0 or selection[0] >= len(booking_rows):
        return
    show_booking_panel(booking_rows[selection[0]])


# A booking was double-clicked: open the receipt window
def on_booking_double_click(event):
    selection = lists["bookings"].curselection()
    if len(selection) > 0 and selection[0] < len(booking_rows):
        view_selected_booking()


# The details panel on the right (empty text if no booking is chosen)
def show_booking_panel(record):
    panel = lists["panel"]
    for widget in panel.winfo_children():
        widget.destroy()
    if record is None:
        Label(panel, text="Click a booking in the list\nto see its details here.", font=NORMAL_FONT,
              fg=GRAY, bg=WHITE).pack(pady=px(40))
        return
    top = Frame(panel, bg=WHITE)
    top.pack(fill=X, pady=(0, px(8)))
    Label(top, text=record["BookingReference"], font=HEADING_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    status_pill(top, record["Status"]).pack(side=RIGHT)
    for line in booking_panel_lines(record):
        panel_line(panel, line[0], line[1])
    build_booking_actions(panel, record)


# The lines of the details panel, as (title, value)
def booking_panel_lines(record):
    discount = "None"
    if record["PromoTypeName"] is not None:
        discount = record["PromoTypeName"] + " (" + peso(record["DiscountAmount"]) + " off)"
    return [("Customer", record["FirstName"] + " " + record["LastName"]),
            ("Contact", str(record["Email"] or record["Phone"])),
            ("Package", record["Title"]),
            ("Travel", nice_date(record["TravelDate"]) + " - " + nice_date(record["EndDate"])),
            ("People", str(record["NumberOfPeople"])),
            ("Payment", str(record["PaymentMethod"]) + "  •  " + str(record["PaymentStatus"])),
            ("Discount", discount),
            ("Total", peso(record["TotalAmount"])),
            ("Booked on", str(record["BookingDate"])[:16]),
            ("Notes", str(record["Notes"] or "(none)"))]


# The action buttons under the details (gray when not allowed for this status)
def build_booking_actions(panel, record):
    status = record["Status"]
    Frame(panel, bg=BORDER, height=1).pack(fill=X, pady=px(10))
    row1 = Frame(panel, bg=WHITE)
    row1.pack(fill=X)
    action_button(row1, "Confirm", confirm_selected_booking, status == "Pending").pack(side=LEFT, fill=X, expand=True)
    action_button(row1, "Mark Completed", complete_selected_booking, status == "Confirmed",
                  DARK_TEAL).pack(side=LEFT, fill=X, expand=True, padx=(px(6), 0))
    row2 = Frame(panel, bg=WHITE)
    row2.pack(fill=X, pady=px(6))
    can_pay = status != "Cancelled" and record["PaymentStatus"] == "Pending"
    action_button(row2, "Mark as Paid", mark_selected_paid, can_pay, GREEN).pack(side=LEFT, fill=X, expand=True)
    action_button(row2, "Cancel Booking", cancel_selected_booking, status in ("Pending", "Confirmed"),
                  RED).pack(side=LEFT, fill=X, expand=True, padx=(px(6), 0))
    light_button(panel, "View Receipt and History", view_selected_booking).pack(fill=X)


# Open the bookings page again (same filter and search), with this booking selected
def reload_bookings(booking_id):
    helpers.go_to("admin_bookings", {"status": lists["booking_status"],
                                     "keyword": lists["booking_search"].get(), "select": booking_id})


# The booking that is selected in the list (or None)
def selected_booking():
    selection = lists["bookings"].curselection()
    if len(selection) == 0 or selection[0] >= len(booking_rows):
        messagebox.showwarning("Bookings", "Please choose a booking in the list first.")
        return None
    return booking_rows[selection[0]]


# Change the status of the selected booking (only from the allowed statuses)
def change_selected_booking(new_status, allowed, description):
    if not require_admin():
        return
    record = selected_booking()
    if record is None:
        return
    if record["Status"] not in allowed:
        messagebox.showwarning("Bookings", "This booking is " + record["Status"] + ". It cannot be changed to " + new_status + ".")
        return
    if not messagebox.askyesno("Bookings", "Change " + record["BookingReference"] + " to " + new_status + "?"):
        return
    try:
        database.change_booking_status(record["BookingID"], new_status, helpers.current_user["UserID"], description)
    except Exception as error:
        show_error("Could not change the booking.", error)
        return
    reload_bookings(record["BookingID"])


# Confirm button: Pending -> Confirmed
def confirm_selected_booking():
    change_selected_booking("Confirmed", ["Pending"], "Confirmed by admin")


# Mark Completed button: Confirmed -> Completed
def complete_selected_booking():
    change_selected_booking("Completed", ["Confirmed"], "Marked as completed by admin")


# Cancel button: Pending or Confirmed -> Cancelled (frees the slots)
def cancel_selected_booking():
    change_selected_booking("Cancelled", ["Pending", "Confirmed"], "Cancelled by admin")


# Mark the payment of the selected booking as paid
def mark_selected_paid():
    if not require_admin():
        return
    record = selected_booking()
    if record is None:
        return
    if record["Status"] == "Cancelled" or record["PaymentStatus"] != "Pending":
        messagebox.showwarning("Bookings", "Only pending payments of active bookings can be marked as paid.")
        return
    if not messagebox.askyesno("Bookings", "Mark the payment of " + record["BookingReference"] + " as paid?"):
        return
    try:
        database.mark_payment_paid(record["BookingID"], helpers.current_user["UserID"])
    except Exception as error:
        show_error("Could not update the payment.", error)
        return
    reload_bookings(record["BookingID"])


# A window with the receipt, notes and history of the selected booking
def view_selected_booking():
    record = selected_booking()
    if record is None:
        return
    window = Toplevel()
    window.title("Booking " + record["BookingReference"])
    window.configure(bg=WHITE, padx=px(10), pady=px(10))
    center_window(window, px(600), px(700))
    user_pages.show_receipt_box(window, record["BookingID"])
    lines = ["Notes: " + str(record["Notes"] or "(none)"), "", "History:"]
    for history in database.get_booking_history(record["BookingID"]):
        lines.append(str(history["ActionDate"])[:16] + "  " + history["ActionType"] + ": " +
                     str(history["PreviousStatus"]) + " -> " + str(history["NewStatus"]) + "  " + str(history["ActionDescription"]))
    history_box = Text(window, width=70, height=8, font=SMALL_FONT, relief=SOLID, bd=1, wrap=WORD)
    history_box.insert("1.0", "\n".join(lines))
    history_box.config(state=DISABLED)
    history_box.pack(fill=X, pady=px(8))
    light_button(window, "Close", window.destroy).pack()


# ======================= Discount requests =======================

# All PWD / Senior Citizen requests with status buttons and a details panel
def show_discounts_page(parent, data):
    options = page_options(data, "Pending")
    content = build_admin_layout(parent, "admin_discounts", "Discount Requests",
                                 "Approve or reject PWD and Senior Citizen IDs")
    lists["promo_status"] = options["status"]
    build_status_chips(content, PROMO_STATUSES, database.get_promo_counts(), options["status"], "admin_discounts")
    body = Frame(content, bg=PAGE_BG)
    body.pack(fill=BOTH, expand=True)
    list_card, header, list_body = make_card(body, "Requests")
    list_card.pack(side=LEFT, fill=BOTH, expand=True)
    panel_card, panel_header, lists["promo_panel"] = make_card(body, "Request details")
    panel_card.config(width=px(370))
    panel_card.pack_propagate(False)
    panel_card.pack(side=LEFT, fill=Y, padx=(px(16), 0))
    make_list_header(list_body, column("ID", 4, True) + column("Customer", 20) + column("Type", 15) +
                     column("Status", 9) + "ID Number")
    box, lists["promos"] = make_listbox(list_body, 16)
    box.pack(fill=BOTH, expand=True)
    lists["promos"].bind("<<ListboxSelect>>", on_promo_select)
    fill_promo_list(options["status"])
    select_list_row(lists["promos"], promo_rows, "PromoID", options["select"], show_promo_panel)


# Fill the requests Listbox
def fill_promo_list(status):
    global promo_rows
    promo_rows = database.get_promo_requests(status)
    listbox = lists["promos"]
    number = 0
    for request in promo_rows:
        text = (column(request["PromoID"], 4, True) + column(request["FirstName"] + " " + request["LastName"], 20) +
                column(request["PromoTypeName"], 15) + column(request["Status"], 9) + request["DocumentNumber"])
        listbox.insert(END, text)
        color_list_row(listbox, number, ROW_COLORS.get(request["Status"], DARK_TEAL))
        number = number + 1
    if len(promo_rows) == 0:
        listbox.insert(END, "  (no requests)")
    show_promo_panel(None)


# A request was clicked: show it in the details panel
def on_promo_select(event):
    selection = lists["promos"].curselection()
    if len(selection) == 0 or selection[0] >= len(promo_rows):
        return
    show_promo_panel(promo_rows[selection[0]])


# The details of one request with Approve and Reject
def show_promo_panel(request):
    panel = lists["promo_panel"]
    for widget in panel.winfo_children():
        widget.destroy()
    if request is None:
        Label(panel, text="Click a request in the list\nto see its details here.", font=NORMAL_FONT,
              fg=GRAY, bg=WHITE).pack(pady=px(40))
        return
    top = Frame(panel, bg=WHITE)
    top.pack(fill=X, pady=(0, px(8)))
    Label(top, text=request["PromoTypeName"], font=HEADING_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    status_pill(top, request["Status"]).pack(side=RIGHT)
    panel_line(panel, "Customer", request["FirstName"] + " " + request["LastName"])
    panel_line(panel, "Contact", str(request["Email"] or request["Phone"]))
    panel_line(panel, "ID number", request["DocumentNumber"])
    panel_line(panel, "Sent on", str(request["CreatedAt"])[:16])
    panel_line(panel, "Checked on", str(request["ValidationDate"] or "not yet")[:16])
    Frame(panel, bg=BORDER, height=1).pack(fill=X, pady=px(10))
    row = Frame(panel, bg=WHITE)
    row.pack(fill=X)
    action_button(row, "Approve", approve_request, request["Status"] != "Approved", GREEN).pack(side=LEFT, fill=X, expand=True)
    action_button(row, "Reject", reject_request, request["Status"] != "Rejected", RED).pack(side=LEFT, fill=X, expand=True, padx=(px(6), 0))
    Label(panel, text="Approved customers get the discount on their next bookings.", font=SMALL_FONT,
          fg=GRAY, bg=WHITE, wraplength=px(300), justify=LEFT).pack(anchor="w", pady=(px(8), 0))


# Approve or reject the selected request
def set_selected_request(new_status):
    if not require_admin():
        return
    selection = lists["promos"].curselection()
    if len(selection) == 0 or selection[0] >= len(promo_rows):
        messagebox.showwarning("Discount Requests", "Please choose a request in the list first.")
        return
    request = promo_rows[selection[0]]
    name = request["FirstName"] + " " + request["LastName"]
    if not messagebox.askyesno("Discount Requests", "Set the " + request["PromoTypeName"] + " request of " + name + " to " + new_status + "?"):
        return
    try:
        database.set_promo_status(request["PromoID"], new_status, helpers.current_user["UserID"])
    except Exception as error:
        show_error("Could not update the request.", error)
        return
    helpers.go_to("admin_discounts", {"status": lists["promo_status"], "select": request["PromoID"]})


# Approve button
def approve_request():
    set_selected_request("Approved")


# Reject button
def reject_request():
    set_selected_request("Rejected")
