from pydantic import BaseModel,validator
from typing import Optional,List

class WeekendDefinition(BaseModel):
    Sunday:Optional[List[int]]
    Monday:Optional[List[int]]
    Tuesday:Optional[List[int]]
    Wednesday:Optional[List[int]]
    Thursday:Optional[List[int]]
    Friday:Optional[List[int]]
    Saturday:Optional[List[int]]
    


class CalenderSettingResponse(BaseModel):
    location:str
    week_start_on:str
    work_week_start_on:str
    work_week_end_on:str
    half_full_day:bool
    calender_starts:str
    calender_ends:str
    weekend_definition:WeekendDefinition
    statutory_weekend:bool
