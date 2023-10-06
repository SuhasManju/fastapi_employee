from pydantic import BaseModel,validator
from typing import Optional,List,Union
from datetime import time,date
import json

class Applicable_For(BaseModel):
    department:Optional[List[str]]
    location:Optional[List[str]]
    division:Optional[List[str]]



class ShiftsIn(BaseModel):
    shift_name:str
    start_from:time
    to_time:time
    shift_margin:bool=False
    hours_befor_shift:str
    hours_after_shift:str
    weekend:str
    half_working_and_half_weekend:bool=False
    weekend_defination:str
    applicable_for:Optional[List[Applicable_For]]

    @validator('shift_name','start_from','to_time',pre=True)
    def is_inputvalid(cls,value):
        if len(value)==0:
            raise ValueError("Name cannot be empty")
        return value


class ShiftsOut(BaseModel):
    shift_name:str
    start_from:time
    to_time:time
    shift_margin:bool=False
    hours_befor_shift:str
    hours_after_shift:str
    weekend:str
    half_working_and_half_weekend:bool=False
    weekend_defination:str
    department: Optional[Union[List[str], str]] 
    location: Optional[Union[List[str], str]] 
    division: Optional[Union[List[str], str]] 


    class Config:
        orm_table = True

    @validator("department", "location","division", pre=True)
    def validate_list_or_string(cls, value):
        if isinstance(value, list):
            return value
        elif isinstance(value, str):
            try:
                # Try to parse the string as a JSON array
                parsed_value = json.loads(value)
                if isinstance(parsed_value, list):
                    return parsed_value
                else:
                    return [parsed_value]  # Treat it as a single-value list
            except json.JSONDecodeError:
                return [value]  # If parsing as JSON fails, treat it as a single-value list
        else:
            return None


class Shiftsupdate(BaseModel):
    old_shift_name:str
    shift_name:str
    start_from:time
    to_time:time
    shift_margin:bool=False
    hours_befor_shift:str
    hours_after_shift:str
    weekend:str
    half_working_and_half_weekend:bool=False
    weekend_defination:str
    applicable_for:Optional[List[Applicable_For]]



class Shift_Delete(BaseModel):
    shift_name:str
