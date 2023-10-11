from pydantic import BaseModel,validator
from typing import List

class AbsentScheduleIn(BaseModel):
    name:str
    schedule_run:str
    process_data:int
    push_absense_to_leave_module:bool
    notify_through_email:bool
    department:List[str]
    designation:List[str]
    location:List[str]
    role:List[str]

    @validator('schedule_run')
    def validate_time(cls,value):
        x=value.split(":")
        if len(x)!=2:
            raise ValueError("Input not in time HH:MM format")
        return value
    
class AbsentScheduleOut(BaseModel):
    name:str
    schedule_run:str
    process_data:int
    push_absense_to_leave_module:bool
    notify_through_email:bool
    department:List[str]
    designation:List[str]
    location:List[str]
    role:List[str]

class AbsentScheduleUpdate(BaseModel):
    old_name:str
    name:str
    schedule_run:str
    process_data:int
    push_absense_to_leave_module:bool
    notify_through_email:bool
    department:List[str]
    designation:List[str]
    location:List[str]
    role:List[str]
    @validator('schedule_run')
    def validate_time(cls,value):
        x=value.split(":")
        if len(x)!=2:
            raise ValueError("Input not in time HH:MM format")
        return value

class AbsentScheduleDelete(BaseModel):
    name:str
    