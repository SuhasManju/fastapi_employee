from pydantic import BaseModel,EmailStr
from typing import Optional

class CurrentLeaveOut(BaseModel):
    emp_name:str
    leave_type:str
    number_of_leaves:int
    booked:int

class CurrentLeaveCustom(BaseModel):
    emp_email:EmailStr
    leave_type:str
    no_leaves:int