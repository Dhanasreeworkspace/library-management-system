import frappe
from frappe.utils import date_diff, getdate

FINE_PER_DAY = 10


def execute(filters=None):

    columns = [
        {
            "label": "Member",
            "fieldname": "member",
            "fieldtype": "Link",
            "options": "Library Member",
            "width": 180,
        },
        {
            "label": "Book",
            "fieldname": "book",
            "fieldtype": "Link",
            "options": "Library Book",
            "width": 180,
        },
        {
            "label": "Due Date",
            "fieldname": "due_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Days Overdue",
            "fieldname": "days_overdue",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Fine",
            "fieldname": "fine",
            "fieldtype": "Currency",
            "width": 120,
        },
    ]

    data = []

    today_date = getdate()

    issues = frappe.get_all(
        "Book Issue",
        filters={"status": "Issued"},
        fields=["member", "book", "due_date"],
    )

    for issue in issues:

        if issue.due_date and getdate(issue.due_date) < today_date:

            days = date_diff(today_date, issue.due_date)

            fine = days * FINE_PER_DAY

            data.append(
                {
                    "member": issue.member,
                    "book": issue.book,
                    "due_date": issue.due_date,
                    "days_overdue": days,
                    "fine": fine,
                }
            )

    return columns, data