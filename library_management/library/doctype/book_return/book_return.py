import frappe
from frappe.model.document import Document
from frappe.utils import date_diff
from frappe import _

FINE_PER_DAY = 10


class BookReturn(Document):

    def validate(self):
        self.fetch_issue_details()
        self.calculate_fine()

    def on_submit(self):
        self.update_status()

    def fetch_issue_details(self):

        issue = frappe.get_doc(
            "Book Issue",
            self.book_issue
        )

        self.member = issue.member
        self.book = issue.book

    def calculate_fine(self):

        issue = frappe.get_doc(
            "Book Issue",
            self.book_issue
        )

        late_days = date_diff(
            self.return_date,
            issue.due_date
        )

        if late_days > 0:
            self.fine_amount = late_days * FINE_PER_DAY
        else:
            self.fine_amount = 0

    def update_status(self):

        issue = frappe.get_doc(
            "Book Issue",
            self.book_issue
        )

        issue.status = "Returned"
        issue.save(ignore_permissions=True)

        frappe.db.set_value(
            "Library Book",
            issue.book,
            "status",
            "Available"
        )


# ===================================================
# THIS FUNCTION MUST BE OUTSIDE THE CLASS
# ===================================================

@frappe.whitelist()
def get_fine_amount(book_issue, return_date):

    if not book_issue or not return_date:
        return 0

    issue = frappe.get_doc("Book Issue", book_issue)

    late_days = date_diff(return_date, issue.due_date)

    if late_days > 0:
        return late_days * FINE_PER_DAY

    return 0