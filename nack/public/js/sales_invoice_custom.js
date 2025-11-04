// frappe.ui.form.on('Sales Invoice', {
//     before_save(frm) {
//         // Only show dialog for new invoices (optional: remove this check if you want every save)
//         if (frm.is_new() && !frm.doc.is_custom_order_checked) {
//             return new Promise((resolve, reject) => {
//                 frappe.confirm(
//                     'Is this a custom order? (Click "Yes" to apply a 30% price increase)',
//                     () => {
//                         // ✅ User clicked Yes — apply 30% increase
//                         frm.doc.items.forEach(item => {
//                             const new_rate = flt(item.rate) * 1.3;
//                             item.rate = new_rate;
//                             item.amount = new_rate * flt(item.qty);
//                         });

//                         frm.doc.is_custom_order_checked = 1;

//                         // Recalculate totals before saving
//                         frm.trigger("calculate_taxes_and_totals");

//                         frappe.msgprint(__('Applied 30% price increase for custom order.'));
//                         resolve();
//                     },
//                     () => {
//                         // User clicked No — continue without changes
//                         frm.doc.is_custom_order_checked = 1;
//                         resolve();
//                     }
//                 );
//             });
//         }
//     }
// });



frappe.ui.form.on('Sales Invoice', {
    refresh(frm) {
        // Show the button only when the document is saved (not new or cancelled)
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            frm.add_custom_button('Apply 30% Custom Order Increase', () => {
                frappe.confirm(
                    'Is this a custom order? (Click "Yes" to apply a 30% price increase)',
                    () => {
                        // ✅ User clicked Yes — apply 30% increase
                        frm.doc.items.forEach(item => {
                            const new_rate = flt(item.rate) * 1.3;
                            item.rate = new_rate;
                            item.amount = new_rate * flt(item.qty);
                        });

                        // Mark the flag so it doesn’t get re-applied
                        frm.doc.is_custom_order_checked = 1;

                        // Recalculate totals before saving
                        frm.trigger("calculate_taxes_and_totals");

                        frm.refresh_field("items");
                        frm.refresh_fields(["total", "grand_total", "rounded_total"]);

                        frappe.msgprint(__('Applied 30% price increase for custom order.'));

                        // Save changes automatically (optional)
                        frm.save();
                    },
                    () => {
                        frappe.msgprint(__('No price increase applied.'));
                    }
                );
            });
        }
    }
});
