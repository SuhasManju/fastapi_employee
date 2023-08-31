from fastapi.routing import APIRouter
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

leave_type = APIRouter(tags=['leave_type'])

@leave_type.post("/mg_leave_type", tags=['leave_type'])
def create_leave_type(
    mg_leave_type: Mg_LeaveTypeIn,
    current_user: User = Depends(autheniticate_user)
):
    db = session()

    existing_leave_type = db.query(Mg_LeaveType).filter(
        Mg_LeaveType.leave_type_name == mg_leave_type.leave_type_name,
        Mg_LeaveType.o_id == current_user.get('o_id')
    ).first()
    if existing_leave_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Leave Type data already exists")

    duplicate_leave_type = db.query(Mg_LeaveType).filter(
        Mg_LeaveType.leave_type_name == mg_leave_type.leave_type_name,
        Mg_LeaveType.o_id != current_user.get('o_id')
    ).first()
    if duplicate_leave_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Leave Type data already exists")

    start_date = mg_leave_type.start_date.split('T')[0]
    end_date = mg_leave_type.end_date.split('T')[0]


   

    for gender, martial_status, department, designation, location, role, employee_type, source_of_hire,duration_allowed,allow_request_for_future_days,leave_applied_only_on,leave_cannot_taken_with in zip_longest(
        mg_leave_type.applicable.gender,
        mg_leave_type.applicable.martial_status,
        mg_leave_type.applicable.department,
        mg_leave_type.applicable.designation,
        mg_leave_type.applicable.location,
        mg_leave_type.applicable.role,
        mg_leave_type.applicable.employee_type,
        mg_leave_type.applicable.source_of_hire,
        mg_leave_type.restriction.duration_allowed,
        mg_leave_type.restriction.allow_request_for_future_days,
        mg_leave_type.restriction.leave_applied_only_on,
        mg_leave_type.restriction.leave_cannot_taken_with,
        fillvalue=None,
    ):
        leave_type_obj = Mg_LeaveType(
        leave_type_name=mg_leave_type.leave_type_name,
        leave_type_code=mg_leave_type.leave_type_code,
        leave_type=mg_leave_type.leave_type,
        unit=mg_leave_type.unit,
        balance_based_on=mg_leave_type.balance_based_on,
        description=mg_leave_type.description,
        start_date=start_date,
        end_date=end_date,
        effictive_after=mg_leave_type.entitlement.effictive_after,
        effictive_from=mg_leave_type.entitlement.effictive_from,
        accural=mg_leave_type.entitlement.accural,
        accural_by=mg_leave_type.entitlement.accural_by,
        accural_on=mg_leave_type.entitlement.accural_on,
        accural_month_on=mg_leave_type.entitlement.accural_month_on,
        accural_by_days=mg_leave_type.entitlement.accural_by_days,
        accural_by_hour=mg_leave_type.entitlement.accural_by_hour,
        accural_in=mg_leave_type.entitlement.accural_in,
        reset=mg_leave_type.entitlement.reset,
        reset_by=mg_leave_type.entitlement.reset_by,
        reset_on=mg_leave_type.entitlement.reset_on,
        reset_month_on=mg_leave_type.entitlement.reset_month_on,
        reset_with=mg_leave_type.entitlement.reset_with,
        reset_on_the=mg_leave_type.entitlement.reset_on_the,
        reset_carry_by=mg_leave_type.entitlement.reset_carry_by,
        reset_carry_max_unit=mg_leave_type.entitlement.reset_carry_max_unit,
        encashment=mg_leave_type.entitlement.encashment,
        encasment_by=mg_leave_type.entitlement.encasment_by,
        encashment_max_unit=mg_leave_type.entitlement.encashment_max_unit,
        prorate_accural=mg_leave_type.entitlement.prorate_accural,
        prorate_by=mg_leave_type.entitlement.prorate_by,
        round_of_to=mg_leave_type.entitlement.round_of_to,
        round_of_start=mg_leave_type.entitlement.round_of_start,
        round_of_end=mg_leave_type.entitlement.round_of_end,
        first_month_from=mg_leave_type.entitlement.first_month_from,
        first_month_to=mg_leave_type.entitlement.first_month_to,
        first_month_count=mg_leave_type.entitlement.first_month_count,
        opening_balance=mg_leave_type.entitlement.opening_balance,
        maximum_balance=mg_leave_type.entitlement.maximum_balance,
        deductible_holidays=mg_leave_type.entitlement.deductible_holidays,
        gender=gender,
        martial_status=martial_status,
        department=department,
        designation=designation,
        location=location,
        role=role,
        employee_type=employee_type,
        source_of_hire=source_of_hire,
        onboarding_status=mg_leave_type.applicable.onboarding_status,
        employee=mg_leave_type.applicable.employee,
        weekend_between_leave_period=mg_leave_type.restriction.weekend_between_leave_period,
        duraction_allowed=duration_allowed,
        allow_request_for_future_days=allow_request_for_future_days,
        leave_applied_only_on=leave_applied_only_on,
        leave_cannot_taken_with=leave_cannot_taken_with,
        holidays_between_leave_period=mg_leave_type.restriction.holidays_between_leave_period,
        applying_leaves_excel_balance=mg_leave_type.restriction.applying_leaves_excel_balance,
        allow_users_to_view=mg_leave_type.restriction.allow_users_to_view,
        balance_to_be_displayed=mg_leave_type.restriction.balance_to_be_displayed,
        allow_request_for_past_days=mg_leave_type.restriction.allow_request_for_past_days,
        maximum_leave_availed_per_application=mg_leave_type.restriction.maximum_leave_availed_per_application,
        minimum_leave_availed_per_application=mg_leave_type.restriction.minimum_leave_availed_per_application,
        maximim_number_consecutive_leave_allowed=mg_leave_type.restriction.maximim_number_consecutive_leave_allowed,
        minimum_gap_between_two_apps=mg_leave_type.restriction.minimum_gap_between_two_apps,
        enable_file_upload_option=mg_leave_type.restriction.enable_file_upload_option,
        maximum_number_of_specific_period=mg_leave_type.restriction.maximum_number_of_specific_period,    
        o_id=current_user.get('o_id'),
        created_by=current_user.get('id'),
        updated_by=current_user.get('id')
        )
        db.add(leave_type_obj)
    db.commit()
    db.refresh(leave_type_obj)
    response_data = {"message": "Created Successfully"}
    return JSONResponse(jsonable_encoder(response_data))





@leave_type.get("/mg_leave_type", response_model=List[Mg_LeaveTypeOut], tags=['leave_type'])
def get_all_mg_leave_type(current_user: User = Depends(autheniticate_user)):
    db = session()

    db_mg_leave_type = db.query(Mg_LeaveType).filter(
        Mg_LeaveType.is_deleted == False,
        Mg_LeaveType.o_id == current_user.get('o_id')
    ).all()

    if not db_mg_leave_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Leave Type Data found")

    result = []
    for datas in db_mg_leave_type:
        result.append(
            Mg_LeaveTypeOut(
                leave_type_name=datas.leave_type_name,
                leave_type_code=datas.leave_type_code,
                leave_type=datas.leave_type,
                unit = datas.unit,
                balance_based_on=datas.balance_based_on,
                description=datas.description,
                start_date=datas.start_date,
                end_date=datas.end_date,
                
                
            )
        )
    return JSONResponse(jsonable_encoder(result))


# @leave_type.put("/mg_leave_type/", tags=['leave_type'])
# def update_mg_leave_type(
#     leave_type_name: str,
#     mg_leave_type: Mg_LeaveTypeIn,
#     current_user: User = Depends(get_current_user)
# ):
#     db = SessionLocal()

#     db_mg_leave_type = db.query(Mg_LeaveType).filter(Mg_LeaveType.leave_type_name == leave_type_name).first()
#     if not db_mg_leave_type:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave Type Data not found")

#     if db_mg_leave_type.created_by != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied. You cannot Edit the Leave Type.")
#     start_date = mg_leave_type.start_date.split('T')[0]
#     end_date = mg_leave_type.end_date.split('T')[0]

#     db_mg_leave_type.leave_type_name=mg_leave_type.leave_type_name,
#     db_mg_leave_type.leave_type_code=mg_leave_type.leave_type_code,
#     db_mg_leave_type.leave_type=mg_leave_type.leave_type,
#     db_mg_leave_type.unit = mg_leave_type.unit,
#     db_mg_leave_type.balance_based_on=mg_leave_type.balance_based_on,
#     db_mg_leave_type.description=mg_leave_type.description,
#     db_mg_leave_type.start_date = start_date
#     db_mg_leave_type.end_date = end_date
#     db_mg_leave_type.updated_by = current_user.get('o_id')

#     db.commit()

#     return JSONResponse({"message": "Leave Type updated successfully"})


# @leave_type.delete("/mg_leave_type/", tags=['leave_type '])
# def delete_leave_type(leave_type_name: str, user: User = Depends(get_current_user)):
#     db = SessionLocal()
#     db_leave_type = db.query(Mg_LeaveType).filter(Mg_LeaveType.leave_type_name == leave_type_name).first()
#     if not db_leave_type:
#         raise HTTPException(status_code=404, detail=f"Academic year '{leave_type_name}' Not Found")

#     if db_leave_type.created_by != user.get('o_id'):
#         raise HTTPException(status_code=403, detail="Access denied. You cannot delete the Leave type data.")

#     db_leave_type.is_deleted = True
#     db.commit()
#     db.refresh(db_leave_type)
#     response_data = {"message": "Deleted Successfully"}
#     return JSONResponse(content=response_data)