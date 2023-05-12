// Copyright (c) 2023, Rasiin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Percentage', {
	// refresh: function(frm) {

	// }
	get_employee_list:function(frm){
		let amount = frm.doc.amount
		if(frm.doc.amount_type == "Percentage"){
			amount = frm.doc.percentage
		}
		if(!frm.doc.percentage && !frm.doc.amount){
			frappe.throw(__('Please Select Amount'))
		}
		let filters = {
			status: 'Active',
			volunteer: ["!=", 1]
		}
		let applied_for = frm.doc.applied_for
		if (applied_for == "Department"){
			if(!frm.doc.department){
				frappe.throw(__('Please Select Department'))
			}
			filters['department'] = frm.doc.department
		}
		if (applied_for == "Designation"){
			if(!frm.doc.designation){
				frappe.throw(__('Please Select Designation'))
			}
			filters['designation'] = frm.doc.designation
		}
		if (applied_for == "Person"){
			if(!frm.doc.employee){
				frappe.throw(__('Please Select Empoyee'))
			}
			filters['name'] = frm.doc.employee
		}
		
		frappe.db.get_list('Employee', {
			fields: ['name', 'employee_name'],
			filters: filters,
			limit : 500
		}).then(records => {
			let emp_list = []
			records.forEach(r => {
				emp_list.push({
					employee : r.name,
					employee_name : r.employee_name,
					percentage : amount

				})
				
			});
			setTimeout(() => {
				frm.set_value("applied_employee" , [])
				frm.set_value("applied_employee" , emp_list)
			}, 100);
			
			// console.log(records);
		})
	},
	applied_for:function(frm){
		frm.set_value("applied_employee" , [])
	},
	amount_type : function(frm){
		frm.set_value("percentage" , '')
		frm.set_value("amount" , '')
		frm.set_value("applied_employee" , [])

	}
});
