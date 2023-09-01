from pydantic import BaseModel
from typing import Optional,List

class Entitlement(BaseModel):
    effictive_after:Optional[str]
    effictive_from:Optional[str]
    accural:Optional[str]
    accural_by:Optional[str]
    accural_on:Optional[str]
    accural_month_on:Optional[str]
    accural_by_days:Optional[str]
    accural_by_hour:Optional[str]
    accural_in:Optional[str]
    reset:Optional[str]
    reset_by:Optional[str]
    reset_on:Optional[str]
    reset_month_on:Optional[str]
    reset_with:Optional[str]
    reset_on_the:Optional[str]
    reset_carry_by:Optional[str]
    reset_carry_max_unit:Optional[str]
    encashment:Optional[str]
    encasment_by:Optional[str]
    encashment_max_unit:Optional[str]
    prorate_accural:Optional[str]
    prorate_by:Optional[str]
    round_of_to:Optional[str]
    round_of_start:Optional[str]
    round_of_end:Optional[str]
    first_month_from:Optional[str]
    first_month_to:Optional[str]
    first_month_count:Optional[str]
    opening_balance:Optional[str]
    maximum_balance:Optional[str]
    deductible_holidays:Optional[str]

class Apllicable(BaseModel):
    gender:Optional[list[str]]
    martial_status:Optional[list[str]]
    department:Optional[list[str]]
    designation:Optional[list[str]]
    location:Optional[list[str]]
    role:Optional[list[str]]
    employee_type:Optional[list[str]]
    source_of_hire:Optional[list[str]]
    onboarding_status:Optional[str]
    employee:Optional[bool]=False
    exception_designation:str
    exception_department:str
    exception_source_of_hire:str
    exception_role:str
    exception_employee_type:str
    exception_onboarding_status:str
    exceptional_location:str



class Restriction(BaseModel):
    weekend_between_leave_period: Optional[str]
    holidays_between_leave_period:Optional[str]
    applying_leaves_excel_balance:Optional[str]
    duration_allowed:List[Optional[str]]
    allow_users_to_view:Optional[str]
    balance_to_be_displayed:Optional[str]
    allow_request_for_past_days:Optional[str]
    allow_request_for_future_days:List[Optional[str]]
    maximum_leave_availed_per_application:Optional[str]
    minimum_leave_availed_per_application:Optional[str]
    maximim_number_consecutive_leave_allowed:Optional[str]
    minimum_gap_between_two_apps:Optional[str]
    enable_file_upload_option:Optional[str]
    maximum_number_of_specific_period:Optional[str]
    leave_applied_only_on:List[Optional[str]]
    leave_cannot_taken_with:List[Optional[str]]



class Mg_LeaveTypeIn(BaseModel):
    leave_type_name:str
    leave_type_code:str
    leave_type:str
    unit:str
    balance_based_on:str
    description:Optional[str]
    start_date: str
    end_date :str
    entitlement:Entitlement
    applicable:Apllicable
    restriction:Restriction
   
   

class Mg_LeaveTypeOut(BaseModel):
    leave_type_name:str
    leave_type_code:str
    leave_type:str
    unit:str
    balance_based_on:str
    description:Optional[str]
    start_date: str
    end_date :str
    gender: List[str]
    marital_status:List[str]
    department:List[str]


    class config:
        orm_table = True