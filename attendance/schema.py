
from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class AttendanceIn(BaseModel):
    email:EmailStr
    checkin:Optional[datetime]
    checkout:Optional[datetime]