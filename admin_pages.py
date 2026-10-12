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

ADMIN_MENU = [("Dashboard", "admin_dashboard"), ("Packages", "admin_packages"),
              ("Bookings", "admin_bookings"), ("Discount Requests", "admin_discounts")]
IMAGE_TYPES = (".png", ".jpg", ".jpeg")


# ======================= Layout and role check =======================

# Stop if the logged in user is not an admin (checked in the database)
def require_admin():
    user = helpers.current_user
    if user is not None and database.user_is_admin(user["UserID"]):
        return True
    messagebox.showerror("LakbayPH", "Only admins can do this.")
    return False


# The left menu of the admin panel. Returns the frame for the page content.
def build_admin_layout(parent, active_page):
    menu = Frame(parent, bg=DEEP_TEAL, width=px(210))
    menu.pack(side=LEFT, fill=Y)
    menu.pack_propagate(False)
    top = Frame(menu, bg=DEEP_TEAL)
    top.pack(fill=X, pady=px(18))
    Label(top, image=load_logo(px(44)), bg=DEEP_TEAL).pack()
    Label(top, text="LakbayPH", font=(FONT, 15, "bold"), fg=TEAL, bg=DEEP_TEAL).pack()
    Label(top, text="Admin Panel", font=SMALL_FONT, fg=WHITE, bg=DEEP_TEAL).pack()
    for item in ADMIN_MENU:
        make_menu_button(menu, item[0], item[1], active_page).pack(fill=X, padx=px(10), pady=2)
    make_menu_button(menu, "Log Out", "logout", active_page).pack(side=BOTTOM, fill=X, padx=px(10), pady=(2, px(16)))
    make_menu_button(menu, "View Website", "home", active_page).pack(side=BOTTOM, fill=X, padx=px(10), pady=2)
    content = Frame(parent, bg=WHITE)
    content.pack(side=LEFT, fill=BOTH, expand=True)
    return content


# One button of the left menu (teal when it is the open page)
def make_menu_button(parent, text, page_name, active_page):
    color = DEEP_TEAL
    if page_name == active_page:
        color = TEAL
    if page_name == "logout":
        command = user_pages.log_out
    else:
        command = lambda: helpers.go_to(page_name)
    return Button(parent, text="   " + text, command=command, bg=color, fg=WHITE, relief=FLAT, anchor="w",
                  font=(FONT, 11, "bold"), activebackground=TEAL, activeforeground=WHITE, cursor="hand2", pady=px(6))


# The title at the top of an admin page
def add_admin_title(parent, title, subtitle):
    box = Frame(parent, bg=WHITE)
    box.pack(fill=X, padx=px(20), pady=(px(16), px(8)))
    Label(box, text=title, font=TITLE_FONT, fg=DARK_TEAL, bg=WHITE).pack(anchor="w")
    Label(box, text=subtitle, font=NORMAL_FONT, fg=GRAY, bg=WHITE).pack(anchor="w")


# A Listbox with a Scrollbar inside a frame
def make_listbox(parent, height):
    box = Frame(parent, bg=WHITE)
    scrollbar = Scrollbar(box, orient=VERTICAL)
    listbox = Listbox(box, height=height, font=MONO_FONT, yscrollcommand=scrollbar.set, activestyle="none",
                      selectbackground=TEAL, selectforeground=WHITE, relief=SOLID, bd=1, exportselection=False)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)
    return box, listbox


# Put text in a fixed-width column (for the Listbox rows)
def column(text, width, right=False):
    text = str(text)
    if len(text) > width:
        text = text[:width - 1] + "~"
    if right:
        return text.rjust(width) + " "
    return text.ljust(width) + " "


# ======================= Dashboard =======================

# Numbers and a bar chart
def show_dashboard_page(parent, data):
    content = build_admin_layout(parent, "admin_dashboard")
    database.auto_complete_bookings()
    stats = database.get_dashboard_stats()
    add_admin_title(content, "Dashboard", "Welcome back, " + helpers.current_user["FirstName"] + "!")
    row = Frame(content, bg=WHITE)
    row.pack(fill=X, padx=px(20))
    make_stat_box(row, "Total Bookings", str(stats["TotalBookings"]), TEAL)
    make_stat_box(row, "Revenue (paid)", peso(stats["Revenue"]), GREEN)
    make_stat_box(row, "Active Packages", str(stats["ActivePackages"]), DARK_TEAL)
    make_stat_box(row, "Pending Bookings", str(stats["PendingBookings"]), GOLD)
    make_stat_box(row, "Pending Discounts", str(stats["PendingDiscounts"]), RED)
    chart_box = make_box(content, "Bookings per package type (not cancelled)")
    chart_box.pack(fill=X, padx=px(20), pady=px(16))
    draw_bar_chart(chart_box, database.get_bookings_per_type())


# One colored box with a number
def make_stat_box(parent, title, value, color):
    box = Frame(parent, bg=color, padx=px(14), pady=px(12))
    box.pack(side=LEFT, fill=X, expand=True, padx=px(5))
    Label(box, text=value, font=(FONT, 18, "bold"), fg=WHITE, bg=color).pack(anchor="w")
    Label(box, text=title, font=NORMAL_FONT, fg=WHITE, bg=color).pack(anchor="w")


# A simple bar chart drawn on a Canvas
def draw_bar_chart(parent, rows):
    canvas = Canvas(parent, width=px(640), height=px(270), bg=WHITE, highlightthickness=0)
    canvas.pack()
    biggest = 1
    for row in rows:
        biggest = max(biggest, row["Total"])
    base_y = px(230)
    canvas.create_line(px(50), px(20), px(50), base_y, fill=GRAY)
    canvas.create_line(px(50), base_y, px(620), base_y, fill=GRAY)
    colors = [TEAL, DARK_TEAL, GOLD]
    x = px(110)
    number = 0
    for row in rows:
        height = int(row["Total"] / biggest * px(180))
        canvas.create_rectangle(x, base_y - height, x + px(110), base_y, fill=colors[number % 3], outline="")
        canvas.create_text(x + px(55), base_y - height - px(12), text=str(row["Total"]), font=BOLD_FONT, fill=DARK_TEAL)
        canvas.create_text(x + px(55), base_y + px(16), text=row["PackageType"], font=NORMAL_FONT, fill=DARK_TEAL)
        x = x + px(170)
        number = number + 1


# ======================= Packages: list (Read) =======================

# The packages page: list on the left, form on the right
def show_packages_page(parent, data):
    content = build_admin_layout(parent, "admin_packages")
    add_admin_title(content, "Packages", "Create, edit, delete and add pictures to tour packages")
    body = Frame(content, bg=WHITE)
    body.pack(fill=BOTH, expand=True, padx=px(16), pady=(0, px(12)))
    left = Frame(body, bg=WHITE)
    left.pack(side=LEFT, fill=Y)
    right = Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    right.pack(side=LEFT, fill=BOTH, expand=True, padx=(px(12), 0))
    build_package_list(left)
    build_package_form(make_scroll_area(right))
    refresh_package_list()
    clear_form()
    if data is not None:
        select_package(data)


# The search box, the Listbox and the New / Delete buttons
def build_package_list(parent):
    row = Frame(parent, bg=WHITE)
    row.pack(fill=X)
    Label(row, text="Search:", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    form["search"] = StringVar()
    search_entry = Entry(row, textvariable=form["search"], font=NORMAL_FONT, relief=SOLID, bd=1)
    search_entry.pack(side=LEFT, fill=X, expand=True, padx=px(6), ipady=2)
    search_entry.bind("<KeyRelease>", on_search_typed)
    header = column("ID", 3, True) + column("Title", 19) + column("Type", 5) + column("Price", 8, True) + column("Slot", 4, True) + "On"
    Label(parent, text=header, font=MONO_FONT, fg=GRAY, bg=WHITE, anchor="w").pack(fill=X, pady=(px(8), 0))
    box, form["package_list"] = make_listbox(parent, 22)
    box.pack(fill=Y, expand=True)
    form["package_list"].config(width=48)
    form["package_list"].bind("<<ListboxSelect>>", on_package_select)
    buttons = Frame(parent, bg=WHITE)
    buttons.pack(fill=X, pady=(px(8), 0))
    teal_button(buttons, "+ New Package", clear_form).pack(side=LEFT)
    Button(buttons, text="Delete", command=delete_package, bg=RED, fg=WHITE, relief=FLAT,
           font=BOLD_FONT, padx=px(14), pady=px(5), cursor="hand2").pack(side=RIGHT)


# Typing in the search box filters the list
def on_search_typed(event):
    refresh_package_list()


# Fill the Listbox with the packages that match the search
def refresh_package_list():
    global package_rows
    keyword = form["search"].get().strip().lower()
    package_rows = []
    form["package_list"].delete(0, END)
    for package in database.get_all_packages():
        words = (str(package["PackageID"]) + " " + package["Title"] + " " + package["PackageType"] + " " +
                 str(package["Location"])).lower()
        if keyword != "" and keyword not in words:
            continue
        active = "Yes"
        if package["IsActive"] != 1:
            active = "No"
        text = (column(package["PackageID"], 3, True) + column(package["Title"], 19) + column(package["PackageType"][:5], 5) +
                column(format(package["Price"], ",.0f"), 8, True) + column(package["MaxSlots"], 4, True) + active)
        form["package_list"].insert(END, text)
        package_rows.append(package)


# A package was clicked in the list: show it in the form
def on_package_select(event):
    selection = form["package_list"].curselection()
    if len(selection) == 0:
        return
    load_package_into_form(package_rows[selection[0]])


# Select a package in the list by its ID (after saving)
def select_package(package_id):
    number = 0
    for package in package_rows:
        if package["PackageID"] == package_id:
            form["package_list"].selection_set(number)
            form["package_list"].see(number)
            load_package_into_form(package)
        number = number + 1


# ======================= Packages: form (Create / Update) =======================

# A label in the first column of the form
def form_label(parent, text, row):
    Label(parent, text=text, font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE, anchor="nw").grid(row=row, column=0, sticky="nw", pady=px(4), padx=(0, px(10)))


# A one-line Entry in the second column of the form
def form_text_entry(parent, key, row, width=40):
    form[key] = StringVar()
    Entry(parent, textvariable=form[key], width=width, font=NORMAL_FONT, relief=SOLID, bd=1).grid(row=row, column=1, sticky="w", pady=px(4), ipady=2)


# The whole package form
def build_package_form(parent):
    grid = Frame(parent, bg=WHITE, padx=px(16), pady=px(12))
    grid.pack(fill=BOTH, expand=True)
    form["form_title"] = Label(grid, text="New Package", font=HEADING_FONT, fg=TEAL, bg=WHITE)
    form["form_title"].grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, px(6)))
    build_form_basics(grid)
    build_form_numbers(grid)
    build_form_dates(grid)
    build_form_texts(grid)
    build_form_image(grid)
    build_form_addons(grid)
    buttons = Frame(grid, bg=WHITE)
    buttons.grid(row=40, column=0, columnspan=2, sticky="ew", pady=px(14))
    teal_button(buttons, "Save Package", save_package_form).pack(side=LEFT)
    light_button(buttons, "Clear Form", clear_form).pack(side=LEFT, padx=px(8))


# Title, type, category, price and description
def build_form_basics(grid):
    form_label(grid, "Title *", 1)
    form_text_entry(grid, "title", 1)
    form_label(grid, "Type *", 2)
    form["type"] = StringVar(value="Domestic")
    types = Frame(grid, bg=WHITE)
    types.grid(row=2, column=1, sticky="w")
    for name in PACKAGE_TYPES:
        Radiobutton(types, text=name, value=name, variable=form["type"], bg=WHITE, fg=DARK_TEAL,
                    activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT)
    form_label(grid, "Category *", 3)
    form["category"] = StringVar()
    form["category_names"] = []
    for category in database.get_categories():
        form["category_names"].append(str(category["CategoryID"]) + " - " + category["CategoryName"] + " (" + category["CategoryType"] + ")")
    make_choice_menu(grid, form["category"], form["category_names"], None, 40).grid(row=3, column=1, sticky="w", pady=px(4))
    form_label(grid, "Price (₱) *", 4)
    form_text_entry(grid, "price", 4, 16)
    form_label(grid, "Description *", 5)
    form_text_entry(grid, "description", 5)


# A Spinbox in the second column of the form
def form_spinbox(parent, key, low, high):
    form[key] = StringVar()
    spinbox = Spinbox(parent, from_=low, to=high, textvariable=form[key], width=6, font=NORMAL_FONT)
    return spinbox


# Duration, nights, slots, group package, status and active
def build_form_numbers(grid):
    form_label(grid, "Duration", 6)
    row = Frame(grid, bg=WHITE)
    row.grid(row=6, column=1, sticky="w", pady=px(4))
    form_spinbox(row, "duration", 1, 60).pack(side=LEFT)
    Label(row, text=" days    Nights:", font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    form_spinbox(row, "nights", 0, 60).pack(side=LEFT)
    form_label(grid, "Slots / Group", 7)
    row2 = Frame(grid, bg=WHITE)
    row2.grid(row=7, column=1, sticky="w", pady=px(4))
    Label(row2, text="Max slots/date:", font=NORMAL_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    form_spinbox(row2, "max_slots", 1, 500).pack(side=LEFT, padx=(0, px(10)))
    form["is_group"] = IntVar()
    Checkbutton(row2, text="Group   Size:", variable=form["is_group"], bg=WHITE, fg=DARK_TEAL,
                activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT)
    form_spinbox(row2, "group_size", 1, 500).pack(side=LEFT)
    form_label(grid, "Status", 8)
    row3 = Frame(grid, bg=WHITE)
    row3.grid(row=8, column=1, sticky="w", pady=px(4))
    form["status"] = StringVar(value="active")
    for status in ["active", "inactive"]:
        Radiobutton(row3, text=status, value=status, variable=form["status"], bg=WHITE, fg=DARK_TEAL,
                    activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT)
    form["is_active"] = IntVar(value=1)
    Checkbutton(row3, text="Is active (not deleted)", variable=form["is_active"], bg=WHITE, fg=DARK_TEAL,
                activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT, padx=px(16))


# Start and end dates (3 Spinboxes each)
def build_form_dates(grid):
    form_label(grid, "Start date", 9)
    start_row = Frame(grid, bg=WHITE)
    start_row.grid(row=9, column=1, sticky="w", pady=px(4))
    form["start"] = make_date_spinboxes(start_row, helpers.today())
    form_label(grid, "End date", 10)
    end_row = Frame(grid, bg=WHITE)
    end_row.grid(row=10, column=1, sticky="w", pady=px(4))
    form["end"] = make_date_spinboxes(end_row, helpers.one_year_from(helpers.today()))


# Location, ideal for, inclusions and highlights
def build_form_texts(grid):
    form_label(grid, "Location *", 11)
    form_text_entry(grid, "location", 11)
    form_label(grid, "Ideal for", 12)
    form_text_entry(grid, "ideal_for", 12)
    form_label(grid, "Inclusions\n(one per line)", 13)
    form["inclusions"] = Text(grid, width=44, height=6, font=NORMAL_FONT, relief=SOLID, bd=1, wrap=WORD)
    form["inclusions"].grid(row=13, column=1, sticky="w", pady=px(4))
    form_label(grid, "Highlights\n(one per line)", 14)
    form["highlights"] = Text(grid, width=44, height=4, font=NORMAL_FONT, relief=SOLID, bd=1, wrap=WORD)
    form["highlights"].grid(row=14, column=1, sticky="w", pady=px(4))


# The picture preview with Upload Image and Import Folder
def build_form_image(grid):
    form_label(grid, "Picture", 15)
    box = Frame(grid, bg=WHITE)
    box.grid(row=15, column=1, sticky="w", pady=px(4))
    form["image_preview"] = Label(box, bg=LIGHT_GRAY)
    form["image_preview"].pack(side=LEFT)
    side = Frame(box, bg=WHITE, padx=px(10))
    side.pack(side=LEFT, fill=Y)
    form["image_label"] = Label(side, text="", font=SMALL_FONT, fg=GRAY, bg=WHITE, wraplength=px(200), justify=LEFT)
    form["image_label"].pack(anchor="w")
    teal_button(side, "Upload Image", upload_image).pack(fill=X, pady=(px(6), 2))
    light_button(side, "Import Folder", import_image_folder).pack(fill=X)
    Label(side, text="Import Folder copies all pictures whose\nfile names match the packages\n(for example fdbasic.jpg).",
          font=SMALL_FONT, fg=GRAY, bg=WHITE, justify=LEFT).pack(anchor="w", pady=(px(6), 0))
    form["image_name"] = None


# The add-ons list with Add / Update / Remove
def build_form_addons(grid):
    form_label(grid, "Add-ons", 16)
    box = Frame(grid, bg=WHITE)
    box.grid(row=16, column=1, sticky="w", pady=px(4))
    list_box, form["addon_list"] = make_listbox(box, 5)
    list_box.pack(fill=X)
    form["addon_list"].config(width=46)
    form["addon_list"].bind("<<ListboxSelect>>", on_addon_select)
    entries = Frame(box, bg=WHITE)
    entries.pack(fill=X, pady=px(4))
    form["addon_name"] = StringVar()
    form["addon_price"] = StringVar()
    form["addon_unit"] = StringVar()
    for item in [("Name", "addon_name", 22), ("Price", "addon_price", 8), ("Unit", "addon_unit", 11)]:
        Label(entries, text=item[0], font=SMALL_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
        Entry(entries, textvariable=form[item[1]], width=item[2], font=NORMAL_FONT, relief=SOLID, bd=1).pack(side=LEFT, padx=(2, px(6)))
    buttons = Frame(box, bg=WHITE)
    buttons.pack(fill=X)
    light_button(buttons, "Add", add_addon).pack(side=LEFT)
    light_button(buttons, "Update", update_addon).pack(side=LEFT, padx=px(6))
    light_button(buttons, "Remove", remove_addon).pack(side=LEFT)
    Label(buttons, text="(saved when you click Save Package)", font=SMALL_FONT, fg=GRAY, bg=WHITE).pack(side=LEFT, padx=px(8))


# Empty the form for a new package
def clear_form():
    global editing_id
    editing_id = None
    form["form_title"].config(text="New Package")
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
    form["image_name"] = None
    form["package_list"].selection_clear(0, END)
    load_addons_into_form([])
    show_image_preview()


# Show a package in the form so it can be edited
def load_package_into_form(package):
    global editing_id
    editing_id = package["PackageID"]
    form["form_title"].config(text="Editing package #" + str(editing_id))
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
    form["image_name"] = package["ImageFileName"]
    show_image_preview()
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
    package["ImageFileName"] = form["image_name"]
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
    messagebox.showinfo("Save Package", "Package #" + str(package_id) + " was saved.")
    helpers.go_to("admin_packages", package_id)


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

# Show the picture of the form (placeholder if there is none)
def show_image_preview():
    photo = load_image(form["image_name"], px(220), px(138))
    form["image_preview"].config(image=photo)
    if form["image_name"] is None:
        form["image_label"].config(text="No picture yet")
    elif find_image_path(form["image_name"]).endswith("placeholder.jpg"):
        form["image_label"].config(text="File: " + form["image_name"] + " (missing, showing placeholder)")
    else:
        form["image_label"].config(text="File: " + form["image_name"])


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


# Upload Image: choose a png/jpg/jpeg file and use it for this package
def upload_image():
    if not require_admin():
        return
    file_path = filedialog.askopenfilename(title="Choose a picture",
                                           filetypes=[("Pictures", "*.png *.jpg *.jpeg")])
    if file_path == "":
        return
    if not file_path.lower().endswith(IMAGE_TYPES):
        messagebox.showwarning("Upload Image", "Please choose a .png, .jpg or .jpeg file.")
        return
    try:
        file_name = copy_image_file(file_path)
        if editing_id is not None:
            database.set_package_image(editing_id, file_name)
    except Exception as error:
        show_error("Could not copy the picture.", error)
        return
    form["image_name"] = file_name
    clear_image_cache()
    show_image_preview()
    if editing_id is None:
        messagebox.showinfo("Upload Image", "Picture copied. Click Save Package to keep it.")
    else:
        messagebox.showinfo("Upload Image", "The picture of package #" + str(editing_id) + " was changed.")


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


# Copy the matching pictures. Returns (number copied, list of names not found).
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
        if found is None:
            not_found.append(wanted)
            continue
        shutil.copy(os.path.join(folder, found), os.path.join(get_images_folder(), found))
        if found != wanted:
            database.set_package_image(row["PackageID"], found)
        copied = copied + 1
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


# ======================= Bookings =======================

# All bookings with a status filter and action buttons
def show_bookings_page(parent, data):
    content = build_admin_layout(parent, "admin_bookings")
    database.auto_complete_bookings()
    status = "All"
    if data is not None:
        status = data
    add_admin_title(content, "Bookings", "Confirm, complete, cancel and mark bookings as paid")
    lists["booking_status"] = StringVar(value=status)
    build_status_filter(content, lists["booking_status"], ["All", "Pending", "Confirmed", "Completed", "Cancelled"],
                        reload_bookings)
    header = (column("Reference", 17) + column("Customer", 16) + column("Package", 22) + column("Travel", 10) +
              column("Ppl", 3, True) + column("Total", 10, True) + column("Status", 9) + "Payment")
    Label(content, text=header, font=MONO_FONT, fg=GRAY, bg=WHITE, anchor="w").pack(fill=X, padx=px(20))
    box, lists["bookings"] = make_listbox(content, 18)
    box.pack(fill=BOTH, expand=True, padx=px(20))
    buttons = Frame(content, bg=WHITE)
    buttons.pack(fill=X, padx=px(20), pady=px(10))
    light_button(buttons, "View Details", view_selected_booking).pack(side=LEFT)
    teal_button(buttons, "Confirm", confirm_selected_booking).pack(side=LEFT, padx=px(6))
    teal_button(buttons, "Mark Completed", complete_selected_booking).pack(side=LEFT)
    teal_button(buttons, "Mark as Paid", mark_selected_paid).pack(side=LEFT, padx=px(6))
    Button(buttons, text="Cancel Booking", command=cancel_selected_booking, bg=RED, fg=WHITE, relief=FLAT,
           font=BOLD_FONT, padx=px(14), pady=px(5), cursor="hand2").pack(side=LEFT)
    fill_bookings_list(status)


# Radiobuttons to filter a list by status
def build_status_filter(parent, variable, statuses, command):
    row = Frame(parent, bg=WHITE)
    row.pack(fill=X, padx=px(20), pady=(0, px(6)))
    Label(row, text="Show:", font=BOLD_FONT, fg=DARK_TEAL, bg=WHITE).pack(side=LEFT)
    for status in statuses:
        Radiobutton(row, text=status, value=status, variable=variable, command=command, bg=WHITE, fg=DARK_TEAL,
                    activebackground=WHITE, font=NORMAL_FONT).pack(side=LEFT)


# A filter Radiobutton was clicked
def reload_bookings():
    helpers.go_to("admin_bookings", lists["booking_status"].get())


# Fill the bookings Listbox
def fill_bookings_list(status):
    global booking_rows
    booking_rows = database.get_all_bookings(status)
    for record in booking_rows:
        text = (column(record["BookingReference"], 17) + column(record["FirstName"] + " " + record["LastName"], 16) +
                column(record["Title"], 22) + column(record["TravelDate"], 10) + column(record["NumberOfPeople"], 3, True) +
                column(format(record["TotalAmount"], ",.0f"), 10, True) + column(record["Status"], 9) + str(record["PaymentStatus"]))
        lists["bookings"].insert(END, text)
    if len(booking_rows) == 0:
        lists["bookings"].insert(END, "  (no bookings)")


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
    reload_bookings()


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
    reload_bookings()


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

# All PWD / Senior Citizen requests with Approve and Reject
def show_discounts_page(parent, data):
    global promo_rows
    content = build_admin_layout(parent, "admin_discounts")
    status = "Pending"
    if data is not None:
        status = data
    add_admin_title(content, "Discount Requests", "Approve or reject PWD and Senior Citizen IDs")
    lists["promo_status"] = StringVar(value=status)
    build_status_filter(content, lists["promo_status"], ["All", "Pending", "Approved", "Rejected"], reload_discounts)
    header = (column("ID", 4, True) + column("Customer", 20) + column("Contact", 24) + column("Type", 15) +
              column("ID Number", 18) + column("Status", 9) + "Sent")
    Label(content, text=header, font=MONO_FONT, fg=GRAY, bg=WHITE, anchor="w").pack(fill=X, padx=px(20))
    box, lists["promos"] = make_listbox(content, 18)
    box.pack(fill=BOTH, expand=True, padx=px(20))
    promo_rows = database.get_promo_requests(status)
    for request in promo_rows:
        text = (column(request["PromoID"], 4, True) + column(request["FirstName"] + " " + request["LastName"], 20) +
                column(request["Email"] or request["Phone"], 24) + column(request["PromoTypeName"], 15) +
                column(request["DocumentNumber"], 18) + column(request["Status"], 9) + str(request["CreatedAt"])[:10])
        lists["promos"].insert(END, text)
    buttons = Frame(content, bg=WHITE)
    buttons.pack(fill=X, padx=px(20), pady=px(10))
    teal_button(buttons, "Approve", approve_request).pack(side=LEFT)
    Button(buttons, text="Reject", command=reject_request, bg=RED, fg=WHITE, relief=FLAT, font=BOLD_FONT,
           padx=px(14), pady=px(5), cursor="hand2").pack(side=LEFT, padx=px(6))


# A filter Radiobutton was clicked
def reload_discounts():
    helpers.go_to("admin_discounts", lists["promo_status"].get())


# Approve or reject the selected request
def set_selected_request(new_status):
    if not require_admin():
        return
    selection = lists["promos"].curselection()
    if len(selection) == 0:
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
    reload_discounts()


# Approve button
def approve_request():
    set_selected_request("Approved")


# Reject button
def reject_request():
    set_selected_request("Rejected")
