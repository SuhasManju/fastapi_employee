from fastapi import APIRouter,HTTPException,Depends
from .schema import PresentDefaultIn,PresentDefaultUpdate,PresentDefaultDelete
from model import Present_Default,Employee
from users.user import autheniticate_user
from database import session
from datetime import datetime
import json
from typing import List

present_def=APIRouter(tags=['Present Default'])

@present_def.post("/presentdefault")
def add_present_default(pre_def:PresentDefaultIn,user=Depends(autheniticate_user)):
    db=session()
    result=db.query(Present_Default).filter(Present_Default.name==pre_def.name,Present_Default.o_id==user['o_id']).first()
    if result:
        raise HTTPException(status_code=400,detail="Present Default Already exits")
    emp_ids=[]
    for i in pre_def.user:
        emp_result=db.query(Employee).filter(Employee.email==i,Employee.o_id==user['o_id']).first()
        if not emp_result:
            raise HTTPException(status_code=404,detail="Employee not found")
        emp_ids.append(emp_result.id)
    present_obj=Present_Default(
        name=pre_def.name,
        effective_from=datetime.strptime(pre_def.effective_from,"%Y-%m-%d"),
        effective_to=datetime.strptime(pre_def.effective_to,"%Y-%m-%d"),
        reason=pre_def.reason,
        o_id=user['o_id'],
        users=json.dumps(emp_ids)
    )
    db.add(present_obj)
    db.commit()
    return {'message':'successfully added'}

@present_def.get("/presentdefault",response_model=List[PresentDefaultIn])
def get_present_deafult(user=Depends(autheniticate_user)):
    db=session()
    result=db.query(Present_Default).filter(Present_Default.o_id==user['o_id']).all()
    result1=[]
    if not result:
        raise HTTPException(status_code=404,detail="No present default found")
    for def_one in result:
        emp_email=[]
        for i in json.loads(def_one.users):
            emp=db.query(Employee).filter(Employee.id==i,Employee.o_id==user['o_id']).first()
            emp_email.append(emp.email)
        result1.append(PresentDefaultIn(name=def_one.name,
                                        user=emp_email,
                                        effective_from=str(def_one.effective_from),
                                        effective_to=str(def_one.effective_to),
                                        reason=def_one.reason))
    return result1

@present_def.put("/presentdefault")
def update_present_default(pre_def:PresentDefaultUpdate,user=Depends(autheniticate_user)):
    db=session()
    old_result=db.query(Present_Default).filter(Present_Default.name==pre_def.old_name,Present_Default.o_id==user['o_id']).first()
    if not old_result: 
        raise HTTPException(status_code=404,detail="No detail found for old Present Default")
    if pre_def.old_name!=pre_def.name:
        new_result=db.query(Present_Default).filter(Present_Default.name==pre_def.name,Present_Default.o_id==user['o_id']).first()
        if new_result:
            raise HTTPException(status_code=404,detail="Present Default already present")
    emp_ids=[]
    for i in pre_def.user:
        emp_result=db.query(Employee).filter(Employee.email==i,Employee.o_id==user['o_id']).first()
        if not emp_result:
            raise HTTPException(status_code=404,detail="Employee not found")
        emp_ids.append(emp_result.id)
    old_result.name=pre_def.name
    old_result.reason=pre_def.reason
    old_result.effective_from=datetime.strptime(pre_def.effective_from,"%Y-%m-%d")
    old_result.effective_to=datetime.strptime(pre_def.effective_to,"%Y-%m-%d")
    old_result.users=json.dumps(emp_ids)
    db.commit()
    return {"message":"Successfullyy updated"}

@present_def.delete("/presentdefault")
def delete_present_default(pre_def:PresentDefaultDelete,user=Depends(autheniticate_user)):
    db=session()
    result=db.query(Present_Default).filter(Present_Default.name==pre_def.name,Present_Default.o_id==user['o_id']).first()
    if not result:
        raise HTTPException(status_code=404,detail="Present Default not found")
    db.delete(result)
    db.commit()
    return {"message":"Successfully deleted"}





    

