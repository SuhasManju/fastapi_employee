from fastapi import APIRouter,HTTPException,Depends
from users.user import autheniticate_user
from model import Absent_Schedule,Department,WorkLocation,Designation
from .schema import AbsentScheduleIn,AbsentScheduleDelete,AbsentScheduleUpdate,AbsentScheduleOut
from typing import List
from database import session
import json
from datetime import time

absent_sce=APIRouter(tags=['Absent Schedule'])

@absent_sce.post("/absentschedule")
def add_absent_schedule(absent:AbsentScheduleIn,user=Depends(autheniticate_user)):
    db=session()
    old_result=db.query(Absent_Schedule).filter(Absent_Schedule.name==absent.name,Absent_Schedule.o_id==user['o_id'],Absent_Schedule.is_deleted==False).first()
    if old_result:
        raise HTTPException(status_code=404,detail="Absent Schedule already exists")
    loc=[]
    dep=[]
    des=[]
    for i in absent.location:
        loc_one=db.query(WorkLocation).filter(WorkLocation.location_name==i,WorkLocation.o_id==user['o_id']).first()
        if not loc_one:
            raise HTTPException(status_code=404,detail="Worklocation not found")
        loc.append(loc_one.w_id)
    for i in absent.department:
        dep_one=db.query(Department).filter(Department.dept_name==i,Department.o_id==user['o_id']).first()
        if not dep_one:
            raise HTTPException(status_code=404,detail="Department not found")
        dep.append(dep_one.d_id)
    for i in absent.designation:
        des_one=db.query(Designation).filter(Designation.des_name==i,Designation.o_id==user['o_id']).first()
        if not des_one:
            raise HTTPException(status_code=404,detail="Designation not found")
        des.append(des_one.des_id)
    abs_time=absent.schedule_run.split(":")
    abs_obj=Absent_Schedule(name=absent.name,
                            schedule_run=time(hour=abs_time[0],minute=abs_time[1]),
                            process_data=absent.process_data,
                            push_absense_to_leave_module=absent.push_absense_to_leave_module,
                            notify_through_email=absent.notify_through_email,
                            department=json.dumps(dep),
                            designation=json.dumps(des),
                            location=json.dumps(loc),
                            role=json.dumps(absent.role),
                            o_id=user['o_id']
                            )
    db.add(abs_obj)
    db.commit()
    
    return {"message":"Successfully inserted"}

@absent_sce.get("/absentschedule",response_model=List[AbsentScheduleOut])
def get_absent_schedule(user=Depends(autheniticate_user)):
    db=session()
    result=db.query(Absent_Schedule).filter(Absent_Schedule.o_id==user['o_id'],Absent_Schedule.is_deleted==False).all()
    if not result:
        raise HTTPException(status_code=404,detail="Not found")
    x=[]
    for one in result:
        dep=[]
        des=[]
        loc=[]
        for i in json.loads(one.department):
            dep_result=db.query(Department).filter(Department.d_id==i,Department.o_id==user['o_id'],Department.is_deleted==False).first()
            if not dep_result:
                continue
            dep.append(dep_result.dept_name)
        for i in json.loads(one.designation):
            des_result=db.query(Designation).filter(Designation.des_id==i,Designation.o_id==user['o_id'],Designation.is_deleted==False).first()
            if not des_result:
                continue
            des.append(des_result.des_name)
        for i in json.loads(one.location):
            loc_result=db.query(WorkLocation).filter(WorkLocation.w_id==i,WorkLocation.o_id==user['o_id'],Designation.is_deleted==False).first()
            if not loc_result:
                continue
            loc.append(loc_result.location_name)
        x.append(AbsentScheduleOut(name=one.name,
                                  schedule_run=str(one.schedule_run),
                                  process_data=one.process_data,
                                  push_absense_to_leave_module=one.push_absense_to_leave_module,
                                  notify_through_email=one.notify_through_email,
                                  department=dep,
                                  role=json.loads(one.role),
                                  designation=des,
                                  location=loc))
    return x

@absent_sce.delete("/absentschedule")
def delete_absent_schedule(abs_sce:AbsentScheduleDelete,user=Depends(autheniticate_user)):
    db=session()
    result=db.query(Absent_Schedule).filter(Absent_Schedule.name==abs_sce.name,Absent_Schedule.o_id==user['o_id'],Absent_Schedule.is_deleted==False).first()
    if not result:
        raise HTTPException(status_code=404,detail="Not Absent Schedule found")
    result.is_deleted=True
    db.commit()
    return {'message':'Successfuly deleted'}

@absent_sce.put("/absentschedule")
def update_absent_schedule(abs_sce_up:AbsentScheduleUpdate,user=Depends(autheniticate_user)):
    db=session()
    old_result=db.query(Absent_Schedule).filter(Absent_Schedule.name==abs_sce_up.old_name,Absent_Schedule.is_deleted==False,Absent_Schedule.o_id==user['o_id']).first()
    if not old_result:
        raise HTTPException(status_code=404,detail="Not Old absent schedule found")
    if abs_sce_up.old_name!=abs_sce_up.name:
        new_result=db.query(Absent_Schedule).filter(Absent_Schedule.name==abs_sce_up.name,Absent_Schedule.is_deleted==False,Absent_Schedule.o_id==user['o_id']).first()
        if new_result:
            raise HTTPException(status_code=400,detail="absent schedule already exists")
    
    loc=[]
    dep=[]
    des=[]
    for i in abs_sce_up.location:
        loc_one=db.query(WorkLocation).filter(WorkLocation.location_name==i,WorkLocation.o_id==user['o_id']).first()
        if not loc_one:
            raise HTTPException(status_code=404,detail="Worklocation not found")
        loc.append(loc_one.w_id)
    for i in abs_sce_up.department:
        dep_one=db.query(Department).filter(Department.dept_name==i,Department.o_id==user['o_id']).first()
        if not dep_one:
            raise HTTPException(status_code=404,detail="Department not found")
        dep.append(dep_one.d_id)
    for i in abs_sce_up.designation:
        des_one=db.query(Designation).filter(Designation.des_name==i,Designation.o_id==user['o_id']).first()
        if not des_one:
            raise HTTPException(status_code=404,detail="Designation not found")
        des.append(des_one.des_id)
    abs_time=abs_sce_up.schedule_run.split(":")
    old_result.name=abs_sce_up.name
    old_result.schedule_run=time(hour=int(abs_time[0]),minute=int(abs_time[1]))
    old_result.process_data=abs_sce_up.process_data
    old_result.push_absense_to_leave_module=abs_sce_up.push_absense_to_leave_module
    old_result.notify_through_email=abs_sce_up.notify_through_email
    old_result.department=json.dumps(dep)
    old_result.designation=json.dumps(des)
    old_result.location=json.dumps(loc)
    old_result.role=json.dumps(abs_sce_up.role)
    db.commit()
    return {'message':'Successfully updated'}



    