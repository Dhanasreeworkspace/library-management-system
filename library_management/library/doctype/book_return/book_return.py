import frappe
from frappe.model.document import Document
from frappe.utils import date_diff

class BookReturn(Document):

    def validate(self):

        issue = frappe.get_doc(
            "Book Issue",
            self.book_issue
        )

        overdue_days = date_diff(
            self.return_date,
            issue.due_date
        )

        if overdue_days > 0:
            self.fine_amount = overdue_days * 10
        else:
            self.fine_amount = 0

    def on_submit(self):

        issue = frappe.get_doc(
            "Book Issue",
            self.book_issue
        )

        issue.status = "Returned"
        issue.save()

        frappe.db.set_value(
            "Library Book",
            issue.book,
            "status",
            "Available"
        )