from database import session
from users.user import autheniticate_user
from model import EmployeeCalender,Employee
from fastapi import APIRouter,Depends,HTTPException
from datetime import datetime
import json
import numpy as np

empcal=APIRouter(tags=['employee calender'])

@empcal.post("/employeecalender")
def add_employeecalender(user=Depends(autheniticate_user)):
    db=session()
    emp_all=db.query(Employee).filter(Employee.o_id==user['o_id']).all()
    today=datetime.today()
    if not emp_all:
        raise HTTPException(status_code=404,detail="Employee not found")
    for emp_one in emp_all:
        cal_result=db.query(EmployeeCalender).filter(EmployeeCalender.emp_id==emp_one.id,EmployeeCalender.month==today.month).all()
        if cal_result:
            pass
        emp_cal=EmployeeCalender(emp_id=emp_one.id,
                                 month=today.month,
                                 calender=json.dumps(np.zeros((7,5),dtype="int8").tolist()),
                                 o_id=user['o_id']
                                 )
        db.add(emp_cal)
    db.commit()
    return {"message":"successfully created"}
    