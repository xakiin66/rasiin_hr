# Copyright (c) 2023, Rasiin and contributors
# For license information, please see license.txt

import frappe
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.setup.doctype.holiday_list.holiday_list import is_holiday
from frappe import _
from datetime import timedelta, date
from frappe.utils import getdate
def execute(filters=None):
	worked_on_holiday = filters.get('worked_on_holiday')
	holiday = {}
	if worked_on_holiday:
		
		holiday=	{
			"label": _("Holiday"),
			"fieldtype": "Data",
			"fieldname": "holiday",
			
			"width": 100,
		}

	columns, data = get_columns(), get_data(filters)
	if holiday:
		columns.insert(4 , holiday)
	return columns, data
def get_data(filters):
	from_date ,to_date , worked_on_holiday = filters.get('from_date'), filters.get('to_date') , filters.get('worked_on_holiday')
	roles = frappe.get_roles(frappe.session.user)
	# frappe.errprint(roles)
	condition = ''
	if 'Medical Director' in roles and frappe.session.user != "Administrator":
		condition = 'and department = "Medical Department - RS"'
	if "HR Manager" not in roles and 'Medical Director' not in roles:
		condition = 'and department = "No Depart - RS'
	if worked_on_holiday:
		condition += f'and worked_on_holiday = {worked_on_holiday}'
	data = frappe.db.sql(f"""
		select 
		attendance_date,
	
		employee_name ,
		status ,
		shift, 
		holiday,
		in_time_string,
		out_time_string ,
		hourse ,

		early_in,
		late_in ,
		early_out ,
		late_out
		


		from `tabAttendance`

		where attendance_date between "{from_date}" and "{to_date} " {condition}
	
	
	""" , as_dict = 1)

	special_holida_data = frappe.db.sql(f"""
		select 
		attendance_date,
	
		employee_name ,
		status ,
		shift, 
		holiday,
		in_time_string,
		out_time_string ,
		hourse ,

		early_in,
		late_in ,
		early_out ,
		late_out
		


		from `tabSpecial Holiday Worked`

		where attendance_date between "{from_date}" and "{to_date} " 
	
	
	""" , as_dict = 1)
	for d in special_holida_data:
		data.append(d)
	def daterange(start_date, end_date):
		for n in range(int ((end_date - start_date).days)+1):
			yield start_date + timedelta(n)

	start_date = getdate(from_date)
	end_date = getdate(to_date)
	
	holiday_atte_list = []
	holiday_scheduled_list = []
	emp_list = frappe.db.get_all("Employee" , 
	
	  filters={
        'status': 'Active'
    },
    fields=['name', 'employee_name','employee'],
   
    page_length=1000,
	 )
	if  not worked_on_holiday:
		for emp in emp_list:
			# frappe.errprint(d)
			holiday_list_name = get_holiday_list_for_employee(emp['name'], False)
			# for single_date in daterange(start_date, end_date):
			# 	print(single_date.strftime("%Y-%m-%d"))
			
			for single_date in daterange(start_date, end_date):
				special_holiday = frappe.db.get_value("Special Holiday" , {"from_date" : ["<=", getdate(single_date)] , "to_date" : [">=", getdate(single_date)]})
				if 	special_holiday:
					holiday_atte = {}
					sp_h = frappe.get_doc("Special Holiday"  , special_holiday)
					holiday = sp_h.holiday
					holiday_atte['employee_name'] = emp['employee_name']
					holiday_atte['status'] = f"<span class='bg-danger text-white'>{holiday}</span>"
					holiday_atte['attendance_date']  = getdate(single_date)
					
					holiday_atte_list.append(holiday_atte)
					
				elif is_holiday(holiday_list_name, single_date):
					holiday_atte = {}
					# frappe.errprint(single_date)
					# holiday_atte['employee'] = emp['name']
					holiday_atte['employee_name'] = emp['employee_name']
					holiday_atte['status'] = "<span class='bg-danger text-white'>Holiday</span>"
					holiday_atte['attendance_date']  = getdate(single_date)
					
					holiday_atte_list.append(holiday_atte)
					# frappe.errprint(holiday_atte_list)
					# data.append({'employee' : d['employee_name']   , "status" : "Holiday"})
		# # data = [{"employee" : "Home" , "name" : "full name" , "status" : 'Holiday'}]
		
			holiday_scheduled = frappe.db.get_all("Employee Schedulling" , fields = ['shift','from_date'] , filters = {"employee" :  emp['employee'] ,"shift" :"Free","from_date" : ("between", [from_date, to_date])})
			# frappe.msgprint(str(to_date))
			for hold_s in holiday_scheduled:
				holiday_sc = {}
				# frappe.errprint(single_date)
				# holiday_atte['employee'] = emp['name']
				holiday_sc['employee_name'] = emp['employee_name']
				holiday_sc['status'] = "<span class='bg-danger text-white'>Holiday</span>"
				holiday_sc['attendance_date']  = getdate(hold_s.from_date)
				holiday_sc['shift'] = frappe.db.get_value("Employee Schedulling" , {"employee" :  emp['employee'] ,"from_date" : frappe.utils.add_to_date(getdate(hold_s.from_date) , days = -1)} , "shift")
		
				
				holiday_scheduled_list.append(holiday_sc)
		for hold in holiday_atte_list:
			search_dict = {'employee_name': hold['employee_name'], 'attendance_date': hold['attendance_date']}
			found = any(all(item in d.items() for item in search_dict.items()) for d in data)
			if found:
				continue
			
			data.append(hold)
		
		for h in holiday_scheduled_list:
		
			search_dict = {'employee_name': h['employee_name'], 'attendance_date': h['attendance_date']}
			found = any(all(item in d.items() for item in search_dict.items()) for d in data)
			if found:
				continue
			data.append(h)
	data = sorted(data, key=lambda x: x['attendance_date'])

	return data 
def get_columns():
	columns = [
		# employee,
		# employee_name ,
		# status ,
		# shift, 
		# in_time_string,
		# out_time_string ,
		# hourse ,

		# early_in,
		# late_in ,
		# early_out ,
		# late_out
			{
			"label": _("Date"),
			"fieldtype": "Date",
			"fieldname": "attendance_date",
			
			"width": 100,
		},
	
		{
			"label": _("Name"),
			"fieldtype": "Data",
			"fieldname": "employee_name",
			
			"width": 200,
		},
		{
			"label": _("Status"),
			"fieldtype": "Data",
			"fieldname": "status",
			
			"width": 180,
		},

			{
			"label": _("Shift"),
			"fieldtype": "Data",
			"fieldname": "shift",
			
			"width": 100,
		},
			{
			"label": _("Time In"),
			"fieldtype": "Data",
			"fieldname": "in_time_string",
			
			"width": 100,
		},
		# out_time_string ,
		# hourse ,

		# early_in,
		# late_in ,
		# early_out ,
		# late_out

		{
			"label": _("Time Out"),
			"fieldtype": "Data",
			"fieldname": "out_time_string",
			
			"width": 100,
		},

		{
			"label": _("W Hours"),
			"fieldtype": "Data",
			"fieldname": "hourse",
			
			"width": 100,
		},

		{
			"label": _("Early In"),
			"fieldtype": "Data",
			"fieldname": "early_in",
			
			"width": 100,
		},

		{
			"label": _("Late In"),
			"fieldtype": "Data",
			"fieldname": "late_in",
			
			"width": 100,
		},

		# early_out ,
		# late_out
			{
			"label": _("Early Out"),
			"fieldtype": "Data",
			"fieldname": "early_out",
			
			"width": 100,
		},

		{
			"label": _("Late Out"),
			"fieldtype": "Data",
			"fieldname": "late_out",
			
			"width": 100,
		},
	
	]
	return columns