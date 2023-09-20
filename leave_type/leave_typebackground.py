from fastapi import BackgroundTasks,HTTPException,status
from model import Mg_LeaveType,Employee,CurrentLeave
from database import session
import json

def addcurrentleave(backgroundtasks:BackgroundTasks,leave_id:int,o_id:int):
    db=session()
    result=db.query(Mg_LeaveType).filter(Mg_LeaveType.id==leave_id).first()
    emp_result=db.query(Employee).filter(Employee.o_id==o_id).all()
    if not emp_result:
        raise HTTPException(status_code=404,detail="No employee found")

    for e in emp_result:
        if result.employee==True:
            
            currentleave=CurrentLeave(emp_id=e.id,leave_type=result.id,num_of_leaves=(int(result.maximum_balance)-(int(result.opening_balance))),booked=0,o_id=o_id)
            db.add(currentleave)
        else:
            gender_result=e.gender in json.loads(result.gender)
            martial_result=e.marital_status in json.loads(result.martial_status)
            dep_result=e.department in json.loads(result.department)
            des_result=e.designation in json.loads(result.designation)
            loc_result=e.location in json.loads(result.location)
            role_result=e.role in json.loads(result.role)
            emptype_result=e.employee_type in json.loads(result.employee_type)
            hiresource_result=e.source_of_hire in json.loads(result.source_of_hire)

            if gender_result and martial_result and dep_result and des_result and loc_result and role_result and emptype_result and hiresource_result:
                currentleave=CurrentLeave(emp_id=e.id,leave_type=result.id,num_of_leaves=(int(result.maximum_balance)-(int(result.opening_balance))),booked=0,o_id=o_id)
                db.add(currentleave)

    db.commit()
    db.close()