from pydantic import BaseModel
from typing import Optional,List



#organization

class InsertOrganization(BaseModel):
    
    org_name : str
    location : str
    industry : str
    org_date : str
    add_line1 : str
    add_line2 : Optional[str]
    state : str
    pincode : int
    city : str

class UpdateOrganization(BaseModel):
    existing_name: str
    new_name : str
    location : str
    industry : str
    org_date : str
    add_line1 : str
    add_line2 : Optional[str]
    state : str
    pincode : int
    city : str

class DeleteOrganization(BaseModel):
    org_name:str

class OrganizationResponse(BaseModel):
    
    org_name : str
    location : str
    industry : str
    org_date : str
    add_line1 : str
    add_line2 : Optional[str]
    state : str
    pincode : int
    city : str


#worklocation

class WorkLocationResponse(BaseModel):
    
    location_name: str
    add_line1 : str
    add_line2 : str
    state :str
    city: str
    pincode: int
    org_name:str
    
    

class InsertWorkLocation(BaseModel):
    location_name: str
    add_line1 :str
    add_line2 : Optional[str]
    state : str
    city: str
    pincode : int
    org_name :str
    
class UpdateWorkLocation(BaseModel):
    old_location_name: str
    new_location_name : str
    add_line1: str
    add_line2: str
    state: str
    city: str
    pincode : int
    old_org_name: str
    new_org_name : str
    

class DeleteWorkLocation(BaseModel):
    location_name : str
    org_name: str


#department

class InsertDepartment(BaseModel):

    dept_name: str
    dept_code : str
    description : Optional[str]
    org_name: str
    location_name : str
    

class DepartmentResponse(BaseModel):
    dept_name: str
    dept_code :str
    description : str
    org_name: str
    location_name: str

class UpdateDepartment(BaseModel):
    old_dept_name: str
    new_dept_name : str
    dept_code : str
    description : Optional[str]
    old_org_name: str
    new_org_name: str

    old_location_name: str
    new_location_name : str

class DeleteDepartment(BaseModel):
    dept_name :str
    org_name: str
    location_name: str

#designation

class InsertDesignation(BaseModel):
    des_name: str
    org_name: str
    location_name: str
    dept_name: str
    

class DesignationResponse(BaseModel):
   
    des_name:str
    org_name: str
    location_name: str
    dept_name: str
   

class UpdateDesignation(BaseModel):
    old_des_name: str
    new_des_name : str
    old_org_name: str
    new_org_name :str
    old_location_name: str
    new_location_name: str
    old_dept_name: str
    new_dept_name : str
  

class DeleteDesignation(BaseModel):
    des_name :str
    org_name: str
    location_name: str
    


#payschedule

class PayScheduleResponse(BaseModel):
    # p_id:int
    select_work_week:Optional[str]
    calculate_salary_based_on:Optional[str]
    pay_your_employee_on:Optional[str]
    start_first_payroll:Optional[str]
    salary_month_willbe_paidon:Optional[str]


class InsertPaySchedule(BaseModel):
    select_work_week :Optional[List[str]]
    calculate_salary_based_on:Optional[str]
    pay_your_employee_on:Optional[str]
    start_first_payroll:Optional[str]
    salary_month_willbe_paidon:Optional[str]


class InsertCompensatoryRequestSchedule(BaseModel):
    schedule_name:str
    time_of_schedule:str
    date:int
    roles:Optional[List[str]]
    departments:Optional[List[str]]
    designations:Optional[List[str]]
    locations:Optional[List[str]]
    groups:Optional[List[str]]
    users:Optional[List[str]]


