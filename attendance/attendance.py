from attendance.schema import *
from fastapi import APIRouter,Depends,HTTPException,Request
from users.user import autheniticate_user
from model import Employee,Attendance,Shifts,Attendance_General_settings
from database import session
from datetime import datetime
import redis


attend=APIRouter(tags=['Attendance'])

@attend.post('/attendance')
def post_attendance(att:AttendanceIn,request:Request,user=Depends(autheniticate_user)):
    db=session()
    redis_con=redis.Redis(host="localhost",port=6379)
    emp_result=db.query(Employee).filter(Employee.email==att.email,Employee.o_id==user['o_id']).first()
    if not emp_result:
        raise HTTPException(status_code=404,detail="No employee not found")
    attend_result=db.query(Attendance).filter(Attendance.emp_id==emp_result.id,Attendance.check_out==None,Attendance.date==datetime.today().date()).first()
    if att.checkin and attend_result:
        raise HTTPException(status_code=400,detail="Attendance not yet completed")
    settings_result=db.query(Attendance_General_settings).filter(Attendance_General_settings.o_id==user['o_id']).all()
    shift_result=db.query(Shifts).filter(Shifts.o_id==user['o_id']).first()
    
    if att.checkin:
        if att.checkin.time()<shift_result.start_from:
            raise HTTPException(status_code=404,detail="employee still out of shift time")
        
        
        
        emp_attend=Attendance(emp_id=emp_result.id,
                          check_in=att.checkin.time(),
                          date=att.checkin.date())
        db.add(emp_attend)
    else:
        attend_result.check_out=att.checkout.time()
    db.commit()
    return {"mesage":"done"}