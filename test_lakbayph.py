# test_lakbayph.py - simple tests for the price computation and the validation.
# Run it with:  python test_lakbayph.py

import sys
import helpers

passed = 0
failed = 0


# Compare what we got with what we expected and print PASS or FAIL
def check(name, result, expected):
    global passed, failed
    if result == expected:
        passed = passed + 1
        print("PASS  " + name)
    else:
        failed = failed + 1
        print("FAIL  " + name + "   got: " + str(result) + "   expected: " + str(expected))


# Price: base price x people + add-ons - discount = total
def test_compute_total():
    totals = helpers.compute_total(28000, 3, [], 0)
    check("3 people, no add-ons", totals["Total"], 84000)
    addons = [{"Price": 5000, "Quantity": 2}, {"Price": 1500, "Quantity": 1}]
    totals = helpers.compute_total(28000, 3, addons, 0)
    check("add-ons total", totals["AddOns"], 11500)
    check("subtotal with add-ons", totals["Subtotal"], 95500)
    check("total with add-ons", totals["Total"], 95500)
    totals = helpers.compute_total(2500, 2, [], 20)
    check("20% discount amount", totals["Discount"], 1000)
    check("total after 20% discount", totals["Total"], 4000)
    totals = helpers.compute_total(2800, 1, [{"Price": 1200, "Quantity": 1}], 20)
    check("discount is on base + add-ons", totals["Discount"], 800)
    check("total 4000 - 800", totals["Total"], 3200)
    totals = helpers.compute_total(2500, 1, [{"Price": 800, "Quantity": 0}], 0)
    check("quantity 0 adds nothing", totals["Total"], 2500)


# Email format
def test_email():
    check("good email", helpers.is_valid_email("juan@email.com"), True)
    check("good email with dots", helpers.is_valid_email("juan.dela.cruz@school.edu.ph"), True)
    check("no @", helpers.is_valid_email("juanemail.com"), False)
    check("two @", helpers.is_valid_email("juan@@email.com"), False)
    check("no domain dot", helpers.is_valid_email("juan@email"), False)
    check("nothing before @", helpers.is_valid_email("@email.com"), False)
    check("space inside", helpers.is_valid_email("juan dc@email.com"), False)
    check("ends with dot", helpers.is_valid_email("juan@email.com."), False)


# PH mobile numbers: 09XXXXXXXXX or +639XXXXXXXXX
def test_phone():
    check("09 format", helpers.is_valid_phone("09171234567"), True)
    check("+639 format", helpers.is_valid_phone("+639171234567"), True)
    check("with spaces and dashes", helpers.is_valid_phone("0917-123 4567"), True)
    check("too short", helpers.is_valid_phone("0917123456"), False)
    check("too long", helpers.is_valid_phone("091712345678"), False)
    check("letters", helpers.is_valid_phone("0917ABC4567"), False)
    check("landline", helpers.is_valid_phone("0281234567"), False)
    check("+63 without 9", helpers.is_valid_phone("+632812345678"), False)
    check("normalize +639 to 09", helpers.normalize_phone("+639171234567"), "09171234567")
    check("normalize removes spaces", helpers.normalize_phone("0917 123 4567"), "09171234567")


# Password rules and hashing
def test_password():
    check("good password", helpers.is_valid_password("travel123"), True)
    check("too short", helpers.is_valid_password("abc123"), False)
    check("no number", helpers.is_valid_password("travelling"), False)
    check("no letter", helpers.is_valid_password("12345678"), False)
    saved = helpers.hash_password("lphttken")
    check("hash is not plain text", "lphttken" in saved, False)
    check("right password matches", helpers.check_password("lphttken", saved), True)
    check("wrong password fails", helpers.check_password("wrong", saved), False)
    check("same password, different salt", helpers.hash_password("abc") == helpers.hash_password("abc"), False)


# Small text helpers
def test_text_helpers():
    check("peso whole number", helpers.peso(28000), "₱28,000")
    check("peso with cents", helpers.peso(99.5), "₱99.50")
    check("duration 3D/2N", helpers.duration_text(3, 2), "3D/2N")
    items = helpers.split_list_text("Flights, 5 nights (2 in Cebu, 3 in Bohol), Breakfast")
    check("split keeps commas inside ( )", items, ["Flights", "5 nights (2 in Cebu, 3 in Bohol)", "Breakfast"])
    check("split by lines", helpers.split_list_text("Lunch\nGuide, with comma"), ["Lunch", "Guide, with comma"])


test_compute_total()
test_email()
test_phone()
test_password()
test_text_helpers()
print("")
print(str(passed) + " passed, " + str(failed) + " failed")

# Tell build.bat that something failed
if failed > 0:
    sys.exit(1)
