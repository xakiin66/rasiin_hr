# Copyright (c) 2023, Rasiin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeSchedulling(Document):
	def before_insert(self):
		# frappe.msgprint(frappe.utils.getdate(self.from_date))
		self.from_date = frappe.utils.getdate(self.from_date)
