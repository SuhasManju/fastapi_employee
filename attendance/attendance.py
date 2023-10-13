from attendance.schema import *
from fastapi import APIRouter,Depends,HTTPException,Request
from users.user import autheniticate_user
from model import Employee,Attendance,Shifts,Attendance_General_settings
from database import session
from datetime import datetime
import json
# import redis


attend=APIRouter(tags=['Attendance'])

@attend.post('/attendance')
def post_attendance(att:AttendanceIn,request:Request,user=Depends(autheniticate_user)):
    db=session()
    if att.checkin:
        checkinTime=datetime.strptime(att.checkin, "%Y-%m-%dT%H:%M:%S.%fZ")
    if att.checkout:
        checkoutTime=datetime.strptime(att.checkout, "%Y-%m-%dT%H:%M:%S.%fZ")
    # redis_con=redis.Redis(host="localhost",port=6379)
    emp_result=db.query(Employee).filter(Employee.email==att.email,Employee.o_id==user['o_id']).first()
    if not emp_result:
        raise HTTPException(status_code=404,detail="No employee not found")
    attend_result=db.query(Attendance).filter(Attendance.emp_id==emp_result.id,Attendance.check_out==None).first()
    if att.checkin and attend_result:
        raise HTTPException(status_code=400,detail="Attendance not yet completed")
    # settings_result=db.query(Attendance_General_settings).filter(Attendance_General_settings.o_id==user['o_id']).all()
    shift_result=db.query(Shifts).filter(Shifts.o_id==user['o_id']).first()
    
    if att.checkin:
        if checkinTime.time()<shift_result.start_from:
            raise HTTPException(status_code=404,detail="employee still out of shift time")
        
        
        
        emp_attend=Attendance(emp_id=emp_result.id,
                          check_in=checkinTime.time(),
                          date=checkinTime.date(),
                          check_in_location_coord=json.dumps(att.location))
        db.add(emp_attend)
    else:
        attend_result.check_out=checkoutTime.time()
        attend_result.check_out_location_coord=json.dumps(att.location)
    db.commit()
    return {"mesage":"done"}

@attend.get("/attendance",response_model=List[AttendanceOut])
def get_attendance(email:str,user=Depends(autheniticate_user)):
    db=session()
    emp_result=db.query(Employee).filter(Employee.email==email,Employee.o_id==user['o_id']).first()
    if not emp_result:
        raise HTTPException(status_code=404,detail="No Employee found")
    result=db.query(Attendance).filter(Attendance.emp_id==emp_result.id).all()
    if not result:
        raise HTTPException(status_code=404,detail="No attendance found")
    x=[]
    for i in result:
        if i.check_in<i.check_out:
            checkin=datetime(year=2023,month=10,day=13,hour=i.check_in.hour,minute=i.check_in.minute,second=i.check_in.second)
            checkout=datetime(year=2023,month=10,day=13,hour=i.check_out.hour,minute=i.check_out.minute,second=i.check_out.second)
        else:
            checkin=datetime(year=2023,month=10,day=13,hour=i.check_in.hour,minute=i.check_in.minute,second=i.check_in.second)
            checkout=datetime(year=2023,month=10,day=14,hour=i.check_out.hour,minute=i.check_out.minute,second=i.check_out.second)
        j=AttendanceOut(email=email,date=str(i.date),checkin=str(i.check_in),checkout=str(i.check_out),total_hours=str(checkout-checkin))
        x.append(j)
    return x
        
    
