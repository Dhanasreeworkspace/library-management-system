import frappe
from frappe.utils import today, date_diff

def execute(filters=None):

    columns = [
        {
            "label": "Member",
            "fieldname": "member",
            "fieldtype": "Link",
            "options": "Library Member",
            "width": 200
        },
        {
            "label": "Book",
            "fieldname": "book",
            "fieldtype": "Link",
            "options": "Library Book",
            "width": 200
        },
        {
            "label": "Days Overdue",
            "fieldname": "days_overdue",
            "fieldtype": "Int",
            "width": 150
        },
        {
            "label": "Fine",
            "fieldname": "fine",
            "fieldtype": "Currency",
            "width": 150
        }
    ]

    data = []

    records = frappe.get_all(
        "Book Issue",
        filters={"status": "Issued"},
        fields=["member", "book", "due_date"]
    )

    for row in records:

        overdue_days = date_diff(
            today(),
            row.due_date
        )

        if overdue_days > 0:
            data.append({
                "member": row.member,
                "book": row.book,
                "days_overdue": overdue_days,
                "fine": overdue_days * 10
            })

    return columns, data