from pydantic import BaseModel,EmailStr
from typing import Optional,List
from datetime import date


class WorkExperience(BaseModel):
    company_name:str
    job_title:str
    from_date:str
    to_date:str
    job_description:str

class EducationDetails(BaseModel):
    institute_name:str
    degree:str
    specialization:str
    date_of_completion:str

class DependentDetails(BaseModel):
    name:str
    relationship:str
    dob:str

class ReportingManager(BaseModel):
    first_name:str
    last_name:Optional[str]

class EmployeeIn(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    department:str
    designation:str
    location:str
    role:str
    manager:ReportingManager
    joining_date:str
    gender:str
    marital_staus:str
    employee_type:str
    source_of_hire:str
    nick_name:str
    dob:str
    about_me:str
    Expertise:str
    pan:str
    uan:str
    aadhaar:str
    ph_num:str
    seating_location:str
    Tags:str
    presentaddress:str
    permanentaddress:str
    person_ph_num:str
    personalemail_id:str
    work_experience:Optional[List[WorkExperience]]
    education_details:Optional[List[EducationDetails]]
    dependent_details:Optional[List[DependentDetails]]





class EmployeeOut(BaseModel):
    first_name:str
    last_name:str
    email:str
    department:str
    designation:str
    location:str
    role:str
    o_id:int
    manager:int
    added_by:int
    joining_date:str
    nick_name:str
    dob:str
    about_me:str
    Expertise:str
    pan:str
    uan:str
    aadhaar:str
    ph_num:str
    seating_location:str
    Tags:str
    presentaddress:str
    permanentaddress:str
    person_ph_num:str
    personalemail_id:str
    work_experience:str
    education_details:str
    dependent_details:str
    gender:str
    marital_staus:str
    employee_type:str
    source_of_hire:str

class Otpin(BaseModel):
    email:EmailStr
    password:str
    otp:str
