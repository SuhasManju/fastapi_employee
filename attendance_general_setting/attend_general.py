from fastapi.routing import APIRouter
from fastapi import BackgroundTasks
from fastapi import status,HTTPException,Depends,Request
from database import *
from model import *
from .schema import *
from users.user import autheniticate_user
from fastapi.responses import JSONResponse
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.state import InstanceState
from itertools import zip_longest
import json 
from sqlalchemy.orm import Session
from datetime import datetime


genral_attendance = APIRouter(tags=['general_attendance_settings'])



# def calculate_new_maximum_balance(leave_type: Mg_LeaveTypeIn):
#     current_date = datetime.now()
#     initial_month = leave_type.entitlement.effictive_from  # Assuming 'effictive_from' represents the initial month
    
#     if current_date.month >= initial_month:
#         # Use the maximum_balance if it's set, otherwise use a default value
#         new_maximum_balance = leave_type.entitlement.maximum_balance or "12"  # Replace "default_value" with your desired default
#     else:
#         new_maximum_balance = "12"  
    
#     return new_maximum_balance

# def update_maximum_balance(db: Session, leave_type: Mg_LeaveTypeIn):
#     current_date = datetime.now()
#     initial_month = leave_type.entitlement.effictive_from
    
#     if current_date.month >= initial_month:
#         new_maximum_balance = calculate_new_maximum_balance(leave_type)
#         leave_type.entitlement.maximum_balance = new_maximum_balance
#         db.commit()




@genral_attendance.post("/general_attendance_settings")
def create_general_attendance_settings(
    general_attendance_settings: Attendance_General_SettingIn,
    current_user: User = Depends(autheniticate_user)
):
    db=session()

    existing_general_attendance_settings = db.query(Attendance_General_settings).filter(
        Attendance_General_settings.effictive_from == general_attendance_settings.effictive_from,
        Mg_LeaveType.o_id == current_user.get('o_id')
    ).first()
    if existing_general_attendance_settings:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" data already exists")

    duplicate_leave_type = db.query(Attendance_General_settings).filter(
        Attendance_General_settings.effictive_from == general_attendance_settings.effictive_from,
        Attendance_General_settings.o_id != current_user.get('o_id')
    ).first()
    if duplicate_leave_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" data already exists")


    effictive_from = datetime.strptime(general_attendance_settings.effictive_from, "%Y-%m-%d")

   
    for i in general_attendance_settings.late_night_work.location:
        location_ids=[]
        location = db.query(WorkLocation).filter(WorkLocation.location_name == i,WorkLocation.is_deleted==False,WorkLocation.o_id==current_user.get('o_id')).first()
        if location:
                location_ids.append(location.id)

     
    leave_type_obj = Attendance_General_settings(
        effictive_from=effictive_from,
        default_shift_time=general_attendance_settings.default_shift_time,
        scale_view=general_attendance_settings.scale_view,

        total_hour_calculation=general_attendance_settings.working_hours.total_hour_calculation,
        minimum_hours_required=general_attendance_settings.working_hours.minimum_hours_required ,
        strict_mode_manual=general_attendance_settings.working_hours.strict_mode_manual,
        strict_mode_full_day=general_attendance_settings.working_hours.strict_mode_full_day,
        strict_mode_half_day=general_attendance_settings.working_hours.strict_mode_half_day,
        strict_shift_hours_full_day=general_attendance_settings.working_hours.strict_shift_hours_full_day,
        strict_shift_hour_half_day=general_attendance_settings.working_hours.strict_shift_hour_half_day,
        lenient_mode_manual=general_attendance_settings.working_hours.lenient_mode_manual,
        lenient_mode_per_day=general_attendance_settings.working_hours.lenient_mode_per_day,
        lenient_mode_shift=general_attendance_settings.working_hours.lenient_mode_shift,
        show_overtime_deveation=general_attendance_settings.working_hours.show_overtime_deveation,
        maximum_hours_required=general_attendance_settings.working_hours.maximum_hours_required,
        round_off=general_attendance_settings.working_hours.round_off,
        first_check_in=general_attendance_settings.working_hours.first_check_in,
        last_check_out=general_attendance_settings.working_hours.last_check_out,
        worked_hours=general_attendance_settings.working_hours.worked_hours,

        enable_tracking=general_attendance_settings.late_night_work.enable_tracking,
        location=json.dumps(location_ids),
        start_time=general_attendance_settings.late_night_work.start_time,
        end_time=general_attendance_settings.late_night_work.end_time,
        shift_margin_enable=general_attendance_settings.late_night_work.shift_margin_enable,

        web_check_in_out= general_attendance_settings.permissions.web_check_in_out,
        mobile_check_in_out=general_attendance_settings.permissions.mobile_check_in_out,
        show_all_check_in_out=general_attendance_settings.permissions.show_all_check_in_out,
        view_report_entries=general_attendance_settings.permissions.view_report_entries,
        edit_report_entries=general_attendance_settings.permissions.edit_report_entries,
        edit_own_entries=general_attendance_settings.permissions.edit_own_entries,
        show_attendance_report=json.dumps(general_attendance_settings.permissions.show_attendance_report),
        show_balance_over_time=json.dumps(general_attendance_settings.permissions.show_balance_over_time),
        edit_balance_over_time=json.dumps(general_attendance_settings.permissions.edit_balance_over_time),
        track_in_out_location=general_attendance_settings.permissions.track_in_out_location,
        restrict_in_out_entries=general_attendance_settings.permissions.restrict_in_out_entries,

        view_emp_shift_map= json.dumps(general_attendance_settings.shift_settings.view_emp_shift_map),
        edit_emp_shift_map = json.dumps(general_attendance_settings.shift_settings.edit_emp_shift_map),
        allow_changing_shifts = general_attendance_settings.shift_settings.allow_changing_shifts,
        email_notification_modify =general_attendance_settings.shift_settings.email_notification_modify,
        feeds_notification_modify=general_attendance_settings.shift_settings.feeds_notification_modify,
        eligibility_shift_allowence=general_attendance_settings.shift_settings.eligibility_shift_allowence,
        make_reason_mandatory=general_attendance_settings.shift_settings.make_reason_mandatory,

        o_id=current_user.get('o_id'),
        created_by=current_user.get('id'),
        updated_by=current_user.get('id')
    )
    db.add(leave_type_obj)
    db.commit()
    db.refresh(leave_type_obj)
    db.commit()
    response_data = {"message": "Created Successfully"}
    return JSONResponse(jsonable_encoder(response_data))







@genral_attendance.get("/general_attendance_settings", response_model=List[Attendance_General_settingsOut])
def get_all_general_attendance_settings(current_user: User = Depends(autheniticate_user)):
    db = session()

    db_general_attendance_settings = db.query(Attendance_General_settings).filter(
        Attendance_General_settings.is_deleted == False,
        Attendance_General_settings.o_id == current_user.get('o_id')
    ).all()

    if not db_general_attendance_settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No general attendance settings Data found")

    result = []
    for datas in db_general_attendance_settings:
        # Extract department IDs from the list representation
        location_ids = extract_ids(datas.location)
        
       

        # Fetch department names based on department IDs
        location = [fetch_location_name(db, location_id, datas.o_id) for location_id in location_ids]
        
       

        result.append(
            Attendance_General_settingsOut(
            effictive_from= datas.effictive_from,
            default_shift_time= datas.default_shift_time,
            scale_view= datas.scale_view,
            total_hour_calculation= datas.total_hour_calculation,
            minimum_hours_required= datas.minimum_hours_required ,
            strict_mode_manual= datas.strict_mode_manual,
            strict_mode_full_day= datas.strict_mode_full_day,
            strict_mode_half_day= datas.strict_mode_half_day,
            strict_shift_hours_full_day= datas.strict_shift_hours_full_day,
            strict_shift_hour_half_day= datas.strict_shift_hour_half_day,
            lenient_mode_manual= datas.lenient_mode_manual,
            lenient_mode_per_day= datas.lenient_mode_per_day,
            lenient_mode_shift= datas.lenient_mode_shift,
            show_overtime_deveation= datas.show_overtime_deveation,
            maximum_hours_required= datas.maximum_hours_required,
            round_off= datas.round_off,
            first_check_in= datas.first_check_in,
            last_check_out= datas.last_check_out,
            worked_hours= datas.worked_hours 
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

def fetch_location_name(db, location_id, o_id):
    locaion_name = db.query(WorkLocation.location_name).filter(
        WorkLocation.id == location_id,
        WorkLocation.o_id == o_id
    ).scalar()
    return locaion_name

