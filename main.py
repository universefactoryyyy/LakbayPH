# main.py - starts LakbayPH: makes the window and switches between pages
from tkinter import *
from tkinter import messagebox
import helpers
import database
import user_pages
import admin_pages

# Make the text sharp on Windows screens that use scaling (125%, 150%...)
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# The main window (made in start_app)
root = None

# Page name -> the function that builds the page
PAGES = {
    "home": user_pages.show_home_page,
    "destinations": user_pages.show_destinations_page,
    "details": user_pages.show_details_page,
    "login": user_pages.show_login_page,
    "signup": user_pages.show_signup_page,
    "booking": user_pages.show_booking_page,
    "confirmation": user_pages.show_confirmation_page,
    "my_bookings": user_pages.show_my_bookings_page,
    "profile": user_pages.show_profile_page,
    "contact": user_pages.show_contact_page,
    "blog": user_pages.show_blog_page,
    "admin_dashboard": admin_pages.show_dashboard_page,
    "admin_packages": admin_pages.show_packages_page,
    "admin_bookings": admin_pages.show_bookings_page,
    "admin_discounts": admin_pages.show_discounts_page,
}


# Clear the window and show another page
def show_page(page_name, data=None):
    # Remove everything from the old page
    for widget in root.winfo_children():
        widget.destroy()
    helpers.scroll_canvas = None

    # Admin pages: check the role in the database, not just the buttons
    if page_name.startswith("admin"):
        if helpers.current_user is None or not database.user_is_admin(helpers.current_user["UserID"]):
            messagebox.showwarning("LakbayPH", "Only admins can open the admin panel.")
            page_name = "home"
            data = None

    # User pages have the top bar; admin pages have their own left menu
    if not page_name.startswith("admin"):
        user_pages.build_top_bar(root, page_name)
    page_frame = Frame(root, bg=helpers.WHITE)
    page_frame.pack(fill=BOTH, expand=True)
    try:
        PAGES[page_name](page_frame, data)
    except Exception as error:
        helpers.show_error("Sorry, something went wrong while opening this page.", error)


# Make the window, set up the database and show the home page
def start_app():
    global root
    root = Tk()
    root.title("LakbayPH - Travel Services")
    root.configure(bg=helpers.WHITE)
    helpers.SCALE = root.winfo_fpixels("1i") / 96
    set_window_size()
    set_window_icon()

    # Create the database on the first run
    try:
        database.setup_database()
        database.auto_complete_bookings()
    except Exception as error:
        helpers.show_error("The database could not be opened.", error)
        root.destroy()
        return

    helpers.show_page_function = show_page
    show_page("home")
    root.mainloop()


# About 1100 x 700 (bigger on scaled screens), centered on the screen
def set_window_size():
    width = min(helpers.px(1100), int(root.winfo_screenwidth() * 0.95))
    height = min(helpers.px(700), int(root.winfo_screenheight() * 0.88))
    helpers.center_window(root, width, height)
    root.minsize(helpers.px(900), helpers.px(560))


# Show the logo in the title bar
def set_window_icon():
    try:
        root.iconbitmap(helpers.resource_path("assets/logo.ico"))
    except Exception:
        pass


if __name__ == "__main__":
    start_app()
