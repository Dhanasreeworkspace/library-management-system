import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today
from frappe import _


class BookIssue(Document):

    def validate(self):
        self.validate_member()
        self.validate_max_books()
        self.validate_overdue_books()
        self.validate_book()
        self.calculate_due_date()

    def on_submit(self):
        self.update_book_status()

    def on_cancel(self):
        self.restore_book_status()

    def validate_member(self):

        member = frappe.get_doc("Library Member", self.member)

        if not member.active:
            frappe.throw(_("Inactive members cannot borrow books."))

    def validate_max_books(self):

        count = frappe.db.count(
            "Book Issue",
            {
                "member": self.member,
                "status": "Issued"
            }
        )

        if count >= 3:
            frappe.throw(_("Maximum 3 books allowed."))

    def validate_overdue_books(self):

        overdue = frappe.db.exists(
            "Book Issue",
            {
                "member": self.member,
                "status": "Issued",
                "due_date": ["<", today()]
            }
        )

        if overdue:
            frappe.throw(_("Member has overdue books."))

    def validate_book(self):

        book = frappe.get_doc("Library Book", self.book)

        if book.status != "Available":
            frappe.throw(_("Book is already issued."))

    def calculate_due_date(self):

        loan_period = frappe.db.get_value(
            "Library Book",
            self.book,
            "loan_period"
        )

        self.due_date = add_days(
            self.issue_date,
            loan_period
        )

    def update_book_status(self):

        frappe.db.set_value(
            "Library Book",
            self.book,
            "status",
            "Issued"
        )

    def restore_book_status(self):

        frappe.db.set_value(
            "Library Book",
            self.book,
            "status",
            "Available"
        )