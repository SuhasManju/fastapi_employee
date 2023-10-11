from pydantic import BaseModel,EmailStr,validator
from typing import Optional,List
from datetime import datetime

class PresentDefaultIn(BaseModel):
    name:str
    user:List[EmailStr]
    effective_from:str
    effective_to:str
    reason:str

    @validator("effective_from","effective_to",pre=True)
    def validate_time(cls,value):
        try:
            datetime.strptime(value,"%Y-%m-%d")
        except:
            raise ValueError("Not in dateformat")
        return value
    


class PresentDefaultUpdate(BaseModel):
    old_name:str
    name:str
    user:List[EmailStr]
    effective_from:str
    effective_to:str
    reason:str

    @validator("effective_from","effective_to",pre=True)
    def validate_time(cls,value):
        try:
            datetime.strptime(value,"%Y-%m-%d")
        except:
            raise ValueError("Not in dateformat")
        return value
    
class PresentDefaultDelete(BaseModel):
    name:str
