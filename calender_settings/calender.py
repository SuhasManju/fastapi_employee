from fastapi import APIRouter,Depends,HTTPException
from users.user import autheniticate_user
import numpy as np
from calender_settings.calender_schema import *
from database import session
from model import WorkLocation,CalenderSettings
import json

calender=APIRouter(tags=['Calender Settings'])

def convertoArray(arr:List[List[int]]):
        a=np.zeros((7,5),dtype='int8')
        rows=0
        for i in arr:
            for j in i:
                a[rows,j-1]=1
            rows+=1
        return a.tolist()

@calender.post("/calendersettings")
def add_calendersettings(cal:CalenderSettingResponse,user=Depends(autheniticate_user)):


    def addToDataBase(db,cal,location,user):
        location_result=db.query(WorkLocation).filter(WorkLocation.location_name==location,WorkLocation.o_id==user['o_id']).first()
        if not location_result:
            raise HTTPException(status_code=404,detail="Work Location not found")
        calender_result=db.query(CalenderSettings).filter(CalenderSettings.location==location_result.w_id,CalenderSettings.o_id==user['o_id']).first()
        if calender_result:
            raise HTTPException(status_code=400,detail="Calender result already exists")
        weekenddef=[cal.weekend_definition.Monday,
                    cal.weekend_definition.Tuesday,
                    cal.weekend_definition.Wednesday,
                    cal.weekend_definition.Thursday,
                    cal.weekend_definition.Friday,
                    cal.weekend_definition.Saturday,
                    cal.weekend_definition.Sunday,]

        cal_obj=CalenderSettings(
            location=location_result.w_id,
            week_starts_on=cal.week_start_on,
            work_week_start_on=cal.work_week_start_on,
            work_week_end_on=cal.work_week_end_on,
            half_full_day=cal.half_full_day,
            calender_starts=cal.calender_starts,
            calender_ends=cal.calender_ends,
            weekend_definition=json.dumps(convertoArray(weekenddef)),
            statutory_weekend=cal.statutory_weekend,
            o_id=user['o_id'])
        db.add(cal_obj)

    db=session()
    if cal.location=='All Location':
        loc_result=db.query(WorkLocation).filter(WorkLocation.o_id==user['o_id']).all()
        for i in loc_result:
            addToDataBase(db,cal,i.location_name,user)
        db.commit()
    else:
        addToDataBase(db,cal,cal.location,user)
        db.commit()
    return {"message":"Successfully inserted"}


@calender.get("/calendersettings",response_model=List[CalenderSettingResponse])
def get_calendersettings(user=Depends(autheniticate_user)):
    def arrayToWeekend(a:list[list[int]])->WeekendDefinition:
        
        def returnList(x:list[int])->list[int]:
            r=[]
            for i in range(len(x)):
                if x[i]==1:
                    r.append(i+1)
            return r
        week=WeekendDefinition(
        Sunday=returnList(a[6]),
        Monday=returnList(a[0]),
        Tuesday=returnList(a[1]),
        Wednesday=returnList(a[2]),
        Thursday=returnList(a[3]),
        Friday=returnList(a[4]),
        Saturday=returnList(a[5]))
        return week
    db=session()
    cal_all=db.query(CalenderSettings).filter(CalenderSettings.o_id==user['o_id']).all()
    if not cal_all:
        raise HTTPException(status_code=404,detail="No calender settings found")
    result=[]
    for cal_one in cal_all:
        loc_one=db.query(WorkLocation).filter(WorkLocation.w_id==cal_one.location).one()
        if not loc_one:
            continue
        weekend=arrayToWeekend(json.loads(cal_one.weekend_definition))
        cal=CalenderSettingResponse(location=loc_one.location_name,
                         week_start_on=cal_one.week_starts_on,
                         work_week_end_on=cal_one.work_week_end_on,
                         work_week_start_on=cal_one.work_week_start_on,
                         half_full_day=cal_one.half_full_day,
                         weekend_definition=weekend,
                         statutory_weekend=cal_one.statutory_weekend,
                         calender_starts=cal_one.calender_starts,
                         calender_ends=cal_one.calender_ends
                         )
        result.append(cal)
    return result


@calender.put("/calendersettings")
def update_calender(cal:CalenderSettingResponse,user=Depends(autheniticate_user)):
    db=session()
    loc_result=db.query(WorkLocation).filter(WorkLocation.location_name==cal.location,WorkLocation.o_id==user['o_id']).first()
    if not loc_result:
        raise HTTPException(status_code=404,detail="No location found")
    cal_result=db.query(CalenderSettings).filter(CalenderSettings.location==loc_result.w_id,CalenderSettings.o_id==user['o_id']).first()
    if not cal_result:
        raise HTTPException(status_code=404,detail="calender settings not found")
    
    weekenddef=[
                    cal.weekend_definition.Monday,
                    cal.weekend_definition.Tuesday,
                    cal.weekend_definition.Wednesday,
                    cal.weekend_definition.Thursday,
                    cal.weekend_definition.Friday,
                    cal.weekend_definition.Saturday,
                    cal.weekend_definition.Sunday,]
    cal_result.week_starts_on=cal.week_start_on
    cal_result.work_week_start_on=cal.work_week_start_on
    cal_result.work_week_end_on=cal.work_week_end_on
    cal_result.half_full_day=cal.half_full_day
    cal_result.calender_starts=cal.calender_starts
    cal_result.calender_ends=cal.calender_ends
    cal_result.statutory_weekend=cal.statutory_weekend
    cal_result.weekend_definition=json.dumps(convertoArray(weekenddef))
    db.commit()
    return {"message":"successfully updated"}

        
        


