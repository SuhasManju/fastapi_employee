from fastapi import APIRouter,HTTPException,Query
from .schema import *
from typing import List
from database import session
shifts=APIRouter(tags=['shifts'])
from model import *
from itertools import zip_longest
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime
from users.user import *


@shifts.post('/shifts')
def post_shifts(shift:ShiftsIn, current_user: User = Depends(autheniticate_user)):
    db = session()
    result = db.query(Shifts).filter(
        Shifts.o_id == current_user.get('o_id'),
        Shifts.shift_name == shift.shift_name,
        Shifts.is_deleted == False
    ).all()

    if result:
        raise HTTPException(status_code=409, detail="Shift already exists")

    
    division_list=[]
    for applicable in shift.applicable_for:
        department_ids = [] 
        location_ids = []

    if applicable.division:
        division_list.extend(applicable.division)  
        
    for department_name in applicable.department:
            department = db.query(Department).filter(Department.dept_name == department_name,Department.is_deleted==False,Department.o_id==current_user.get('o_id')).first()
            if department:
                department_ids.append(department.d_id)
        
   
        
    for location_name in applicable.location:
            location = db.query(WorkLocation).filter(WorkLocation.location_name == location_name,WorkLocation.is_deleted==False,WorkLocation.o_id==current_user.get('o_id')).first()
            if location:
                location_ids.append(location.w_id)
        
       
    data_obj=Shifts(
        shift_name=shift.shift_name,
        start_from = time(
            shift.start_from.hour,
            shift.start_from.minute,
            shift.start_from.second,
            shift.start_from.microsecond
        ),
        to_time=time(
            shift.to_time.hour,
            shift.to_time.minute,
            shift.to_time.second,
            shift.to_time.microsecond
        ),
        shift_margin = shift.shift_margin,
        hours_befor_shift=shift.hours_befor_shift,
        hours_after_shift=shift.hours_after_shift,
        department=json.dumps(department_ids),
        location=json.dumps(location_ids),
        division =json.dumps(division_list),
        weekend=shift.weekend,
        half_working_and_half_weekend=shift.half_working_and_half_weekend,
        weekend_defination= shift.weekend_defination,
        o_id=current_user.get('o_id'),
        created_by=current_user.get('id'),
        updated_by = current_user.get('id'))
    db.add(data_obj)
    db.commit()
    return {'message':"successfuly created"}



@shifts.get("/shifts", response_model=List[ShiftsOut])
def get_all_shifts(current_user: User = Depends(autheniticate_user)):
    db = session()

    db_shifts = db.query(Shifts).filter(
        Shifts.is_deleted == False,
        Shifts.o_id == current_user.get('o_id')
    ).all()

    if not db_shifts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No  Data found")

    result = []
    for datas in db_shifts:
        # Extract department IDs from the list representation
        department_ids = extract_ids(datas.department)

        # Extract location IDs from the list representation
        location_ids = extract_ids(datas.location)

        # Fetch department names based on department IDs
        departments = [fetch_department_name(db, dept_id, datas.o_id) for dept_id in department_ids]
        

        # Fetch location names based on location IDs
        locations = [fetch_location_name(db, location_id, datas.o_id) for location_id in location_ids]

        result.append(
            ShiftsOut(
                shift_name=datas.shift_name,
                start_from=datas.start_from,
                to_time=datas.to_time, 
                shift_margin =datas.shift_margin,
                hours_befor_shift =datas.hours_befor_shift,
                hours_after_shift= datas.hours_after_shift,
                weekend=datas.weekend,
                half_working_and_half_weekend=datas.half_working_and_half_weekend,
                weekend_defination=datas.weekend_defination,
                division=json.loads(datas.division) if datas.division is not None else None,
                department=departments,  
                location=locations  
            )
        )

    return JSONResponse(jsonable_encoder(result))

def extract_ids(id_str):
    try:
        return json.loads(id_str)
    except (ValueError, TypeError):
        return []

def extract_id(id_str):
    try:
        return int(id_str.strip("[]"))
    except ValueError:
        return None

def fetch_department_name(db, department_id, o_id):
    department_name = db.query(Department.dept_name).filter(
        Department.id == department_id,
        Department.o_id == o_id
    ).scalar()
    return department_name

def fetch_location_name(db, location_id, o_id):
    location_name = db.query(WorkLocation.location_name).filter(
        WorkLocation.id == location_id,
        WorkLocation.o_id == o_id
    ).scalar()
    return location_name



@shifts.put('/shifts/')
def update_shift( shift_update: Shiftsupdate, current_user: User = Depends(autheniticate_user)):
    db = session()

    # Check if the shift with the given shift_id exists
    existing_shift = db.query(Shifts).filter(
        Shifts.shift_name == shift_update.old_shift_name,
        Shifts.o_id == current_user.get('o_id'),
        Shifts.is_deleted == False
    ).first()

    if not existing_shift:
        raise HTTPException(status_code=404, detail="Shift not found")

    if shift_update.shift_name != existing_shift.shift_name:
        shift_with_same_name = db.query(Shifts).filter(
            Shifts.shift_name == shift_update.shift_name,
            Shifts.o_id == current_user.get('o_id'),
            Shifts.is_deleted == False
        ).first()
        if shift_with_same_name:
            raise HTTPException(status_code=409, detail="Shift name already exists")

    division_list = []
    for applicable in shift_update.applicable_for:
        department_ids = []
        location_ids = []

        if applicable.division:
            division_list.extend(applicable.division)

        for department_name in applicable.department:
            department = db.query(Department).filter(
                Department.dept_name == department_name,
                Department.is_deleted == False,
                Department.o_id == current_user.get('o_id')
            ).first()
            if department:
                department_ids.append(department.id)

        for location_name in applicable.location:
            location = db.query(WorkLocation).filter(
                WorkLocation.location_name == location_name,
                WorkLocation.is_deleted == False,
                WorkLocation.o_id == current_user.get('o_id')
            ).first()
            if location:
                location_ids.append(location.id)

    # Update the existing shift with new values
    existing_shift.shift_name = shift_update.shift_name
    existing_shift.start_from = time(
        shift_update.start_from.hour,
        shift_update.start_from.minute,
        shift_update.start_from.second,
        shift_update.start_from.microsecond
    )
    existing_shift.to_time = time(
        shift_update.to_time.hour,
        shift_update.to_time.minute,
        shift_update.to_time.second,
        shift_update.to_time.microsecond
    )
    existing_shift.shift_margin = shift_update.shift_margin
    existing_shift.hours_befor_shift = shift_update.hours_befor_shift
    existing_shift.hours_after_shift = shift_update.hours_after_shift
    existing_shift.department = json.dumps(department_ids)
    existing_shift.location = json.dumps(location_ids)
    existing_shift.division = json.dumps(division_list)
    existing_shift.weekend = shift_update.weekend
    existing_shift.half_working_and_half_weekend = shift_update.half_working_and_half_weekend
    existing_shift.weekend_defination = shift_update.weekend_defination
    existing_shift.updated_by = current_user.get('id')

    db.commit()
    return {'message': "Shift updated successfully"}


@shifts.delete("/shifts",)
def delete_shifts(s: Shift_Delete,current_user: User = Depends(autheniticate_user)):
    db=session()
    result=db.query(Shifts).filter(Shifts.shift_name==s.shift_name).all()
    if not result:
        raise HTTPException(status_code=404,detail="Shift not found")
    for r in result:
        r.is_deleted=True
    db.commit()
    return {"message":"Successfully deleted"}