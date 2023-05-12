import frappe 
from frappe.utils import getdate

from datetime import timedelta, date
@frappe.whitelist()
def submit_attendance():
    today = frappe.utils.getdate()
    att_list = frappe.db.get_list('Attendance',
    filters={
        'docstatus': 0,
        "attendance_date" : ['<', today]
    },
    fields=['name','employee', "in_time" , "out_time" , "shift"],
   

        page_length=1000,
    
    )
    for attendacne in att_list:
        att = frappe.get_doc("Attendance" ,attendacne.name )
        if attendacne.out_time and attendacne.in_time:
            # check_time_date = str(att.in_time)
            # em_chec_ti = check_time_date.split(" ")[1]
            
            # shift_end = frappe.db.get_value("Shift Type" , att.shift , "end_time")
            # last_time_in = frappe.utils.time_diff_in_hours(em_chec_ti, str(shift_end))
			
            # if attendacne.in_time:
            #     if abs(last_time_in > 3):
            #         continue

            
            att.submit()
        else:
            if att.in_time :
                em_time_chec = str(att.in_time)
                em_time_chec_ti = em_time_chec.split(" ")[1]
                exact_time = frappe.utils.to_timedelta(em_time_chec_ti)
                shift_end = frappe.db.get_value("Shift Type" , att.shift , "end_time")
			
                last_time = frappe.utils.time_diff_in_hours(em_time_chec_ti, str(shift_end))
                # return str({"mes":last_time})
                if abs(last_time) < 3:
                    # return str({"mes":last_time})
                    att.in_time = ""
                    att.out_time = att.in_time
                    att.remark = "No Check in"
                    att.out_time_string = em_time_chec_ti
                    att.in_time_string = ""
                    att.early_in = ""
                    att.late_in = ""
                    att.late_out = ""
                    att.early_out = ""                 
					
                else:
                    att.in_time_string = em_time_chec_ti
                    att.remark = "No Check Out"

                   
            att.status = "Half Day"
            # att.leave_type = "Leave Without Pay"
            
            att.save()
            att.submit()
    frappe.db.commit()      
    return att_list


@frappe.whitelist()
def mark_attendance_leaves():
    leaves = frappe.db.get_list('Leaves Assigment',
    filters={
        'docstatus': 1,
        "to_date" : ["<=", getdate()]
    },
    fields=['employee' , 'from_date' , 'to_date' , "reason"],
   
    page_length=1000,
   
    )
    for leave in leaves:
          for date in daterange(leave.from_date , leave.to_date):
                try:
                    attend = frappe.get_doc(
                                    {
                                        "doctype" : "Attendance",
                                        "employee" :leave.employee,
                                        "status" : "On Leave",
                                    
                                        "attendance_date" : date,
                                        "remark" : leave.reason
                                    
                                        # "company" : emp_d.company
                                        
                                    
                                    })
                                # if not no_atte_in_sp_holiday:
                                
                    attend.insert()
                    attend.submit()
                    frappe.db.commit()
                except Exception as e:frappe.errprint(e) 

def daterange(start_date, end_date):
		for n in range(int ((end_date - start_date).days)+1):
			yield start_date + timedelta(n)