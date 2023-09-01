from pydantic import BaseModel
from typing import Optional

class CurrentLeaveOut(BaseModel):
    emp_name:str
    leave_type:str
    number_of_leaves:int
    booked:int