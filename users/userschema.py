from pydantic import BaseModel,validator,EmailStr
from datetime import datetime
class UserIn(BaseModel):
    name:str
    email:EmailStr
    password:str
    ph_num:str

    @validator("ph_num",pre=True)
    def valid_ph_num(cls,value):
        try:
            int(value)
        except:
            raise ValueError("use only digits")
        if len(value)!=10:
            raise ValueError("Phone number length not satisfied")
        return value
    
class Otpin(BaseModel):
    email:EmailStr
    otp:str

class UserOut(BaseModel):
    
    email:str
    exp:datetime
    admin:bool
    o_id:int


    
