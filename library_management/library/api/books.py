import frappe

@frappe.whitelist()
def get_books():

    return frappe.get_all(
        "Library Book",
        fields=[
            "name",
            "title",
            "author",
            "status"
        ]
    )