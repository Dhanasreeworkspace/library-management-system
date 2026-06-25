import frappe

@frappe.whitelist()
def get_members():

    return frappe.get_all(
        "Library Member",
        fields=[
            "name",
            "member_name",
            "active"
        ]
    )