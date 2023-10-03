from fastapi import APIRouter,status,HTTPException,Depends
from database import session
from model import CurrentLeave,Mg_LeaveType,Employee
from users.user import autheniticate_user
from .currentleave_schema import *
import json
from typing import List

currentleave_router=APIRouter(tags=["Current Leave"])

@currentleave_router.post("/currentleave")
def add_currentleaves(user=Depends(autheniticate_user)):
    db=session()
    leavetype=db.query(Mg_LeaveType).filter(Mg_LeaveType.o_id==user['o_id']).all()
    if not leavetype:
        raise HTTPException(status_code=404, detail= "Leave type not found")
    employee=db.query(Employee).filter(Employee.o_id==user['o_id']).all()
    if not employee:
        raise HTTPException(status_code=404,detail="No employees found")
    for e in employee:
        for l in leavetype:
            if l.employee:
                currentleave=CurrentLeave(emp_id=e.id,leave_type=l.id,num_of_leaves=(int(l.maximum_balance)-(int(l.opening_balance))),booked=0,o_id=user['o_id'])
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
                    currentleave=CurrentLeave(emp_id=e.id,leave_type=l.id,num_of_leaves=(int(l.maximum_balance)-(int(l.opening_balance))),booked=0,o_id=user['o_id'])
                    db.add(currentleave)
                    
                else:
                    pass
    db.commit()
    return {"message":"successfully created"}

@currentleave_router.get("/currentleave",response_model=List[CurrentLeaveOut])
def get_currentleaves(user=Depends(autheniticate_user)):
    db=session()
    currentleave=db.query(CurrentLeave).filter(CurrentLeave.o_id==user['o_id']).all()
    x=[]
    for c in currentleave:
        empresult=db.query(Employee).filter(Employee.id==c.emp_id).first().email
        leavetype=db.query(Mg_LeaveType).filter(Mg_LeaveType.id==c.leave_type).first().leave_type_name
        z=CurrentLeaveOut(
            emp_name=empresult,
            leave_type=leavetype,
            number_of_leaves=c.num_of_leaves,
            booked=c.booked
        )
        x.append(z)
    return x


@currentleave_router.post("/currentleave/customupdate")
def customUpdate(update:CurrentLeaveCustom,user=Depends(autheniticate_user)):
    db=session()
    leave_result=db.query(Mg_LeaveType).filter(Mg_LeaveType.leave_type_name==update.leave_type,Mg_LeaveType.o_id==user['o_id']).first()
    if not leave_result:
        raise HTTPException(status_code=404,detail="Leave type not found")
    emp_result=db.query(Employee).filter(Employee.email==update.emp_email,Employee.o_id==user['o_id']).first()
    if not emp_result:
        raise HTTPException(status_code=404,detail="Employee not found")
    curr_result=db.query(CurrentLeave).filter(CurrentLeave.leave_type==leave_result.id,CurrentLeave.emp_id==emp_result.id).first()
    if not curr_result:
        raise HTTPException(status_code=404,detail="CurrentLeave not found")
    
    curr_result.num_of_leaves=update.no_leaves
    db.commit()
    db.refresh(curr_result)
    return {"message":"Successfuly updated"}
    
    