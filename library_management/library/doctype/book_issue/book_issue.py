import frappe
from frappe.model.document import Document
from frappe.utils import add_days,today

class BookIssue(Document):

    def validate(self):
        self.validate_member()
        self.validate_book()
        self.calculate_due_date()

    def validate_member(self):

        member = frappe.get_doc(
            "Library Member",
            self.member
        )

        if not member.active:
            frappe.throw(
                "Inactive members cannot borrow books"
            )

        issued_books = frappe.db.count(
            "Book Issue",
            {
                "member": self.member,
                "status": "Issued"
            }
        )

        if issued_books >= 3:
            frappe.throw(
                "Maximum 3 books allowed"
            )

        overdue = frappe.db.exists(
            "Book Issue",
            {
                "member": self.member,
                "status": "Issued",
                "due_date": ["<", today()]
            }
        )

        if overdue:
            frappe.throw(
                "Member has overdue books"
            )

    def validate_book(self):

        book = frappe.get_doc(
            "Library Book",
            self.book
        )

        if book.status == "Issued":
            frappe.throw(
                "Book already issued"
            )

    def calculate_due_date(self):

        book = frappe.get_doc(
            "Library Book",
            self.book
        )

        self.due_date = add_days(
            self.issue_date,
            book.loan_period
        )

    def on_submit(self):

        frappe.db.set_value(
            "Library Book",
            self.book,
            "status",
            "Issued"
        )