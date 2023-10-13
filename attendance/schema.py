
from pydantic import BaseModel,EmailStr
from typing import Optional,List
from datetime import datetime

class AttendanceIn(BaseModel):
    email:EmailStr
    checkin:Optional[str]
    checkout:Optional[str]
    location:List[float]

class AttendanceOut(BaseModel):
    email:str
    date:str
    checkin:str
    checkout:str
    total_hours:str
    status:str
