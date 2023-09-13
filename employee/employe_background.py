from fastapi import BackgroundTasks
from database import session
from model import Employee,Mg_LeaveType,CurrentLeave
import json

def addcurrentleave(backgroundtasks:BackgroundTasks,e_id:int,o_id:int):
    db=session()
    e=db.query(Employee).filter(Employee.id==e_id).first()
    result=db.query(Mg_LeaveType).filter(Mg_LeaveType.o_id==o_id).all()
    for l in result:
        if l.employee:
            currentleave=CurrentLeave(emp_id=e.id,leave_type=l.id,num_of_leaves=(int(l.maximum_balance)-(int(l.opening_balance))),booked=0,o_id=o_id)
            db.add(currentleave)
                
        else:
            gender_result=e.gender in json.loads(l.gender)
            martial_result=e.marital_status in json.loads(l.martial_status)
            dep_result=e.department in json.loads(l.department)
            des_result=e.designation in json.loads(l.designation)
            loc_result=e.location in json.loads(l.location)
            role_result=e.role in json.loads(l.role)
            emptype_result=e.employee_type in json.loads(l.employee_type)
            hiresource_result=e.source_of_hire in json.loads(l.source_of_hire)

            if gender_result and martial_result and dep_result and des_result and loc_result and role_result and emptype_result and hiresource_result:
                currentleave=CurrentLeave(emp_id=e.id,leave_type=l.id,num_of_leaves=(int(l.maximum_balance)-(int(l.opening_balance))),booked=0,o_id=o_id)
                db.add(currentleave)
        db.commit()