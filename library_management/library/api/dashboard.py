import frappe
from frappe.utils import getdate

@frappe.whitelist(allow_guest=True)
def get_dashboard():

    today = getdate()

    members = frappe.db.count("Library Member")
    books = frappe.db.count("Library Book")

    issued = frappe.db.count(
        "Book Issue",
        {"status": "Issued"}
    )

    overdue = frappe.db.count(
        "Book Issue",
        {
            "status": "Issued",
            "due_date": ["<", today]
        }
    )

    return {
        "members": members,
        "books": books,
        "issued": issued,
        "overdue": overdue
    }