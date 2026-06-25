import frappe
from frappe.utils import today

@frappe.whitelist()
def get_dashboard_data():

    return {
        "total_books": frappe.db.count("Library Book"),

        "available_books": frappe.db.count(
            "Library Book",
            {"status":"Available"}
        ),

        "issued_books": frappe.db.count(
            "Library Book",
            {"status":"Issued"}
        ),

        "members": frappe.db.count(
            "Library Member"
        ),

        "overdue_books": frappe.db.count(
            "Book Issue",
            {
                "status":"Issued",
                "due_date":["<", today()]
            }
        )
    }