frappe.ui.form.on("Book Return", {

    book_issue(frm){
        calculate_fine(frm);
    },

    return_date(frm){
        calculate_fine(frm);
    }

});

function calculate_fine(frm){

    if(!frm.doc.book_issue || !frm.doc.return_date){
        return;
    }

    frappe.call({
        method:"library_management.library.doctype.book_return.book_return.get_fine_amount",

        args:{
            book_issue:frm.doc.book_issue,
            return_date:frm.doc.return_date
        },

        callback:function(r){

            frm.set_value(
                "fine_amount",
                r.message
            );

        }

    });

}