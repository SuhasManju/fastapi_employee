from pydantic import BaseModel,EmailStr


class ReportingManager(BaseModel):
    first_name:str
    last_name:str

class EmployeeIn(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    department:str
    designation:str
    location:str
    role:str
    manager:ReportingManager




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

class Otpin(BaseModel):
    email:EmailStr
    otp:str