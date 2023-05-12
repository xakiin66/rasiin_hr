# Copyright (c) 2023, Rasiin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeavesAssigment(Document):
    pass
	# def on_submit(self):
	# 	att = frappe.get_doc({
	# 		"doctype" : "Attendance",
	# 		"employee" : self.employee,
	# 		"attendance_date" : self.from_date,
	# 		"status" : "On Leave",
	# 		"remark" : self.reason
	# 	})
	# 	att.insert(ignore_permissions = 1)
	# 	att.submit()
