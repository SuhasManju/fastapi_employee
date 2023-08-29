from fastapi import APIRouter,HTTPException,BackgroundTasks,Depends,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from users.email_service import email_generate
from users.userschema import UserIn,Otpin,UserOut
from database import session
import jwt
import json
from datetime import datetime,timedelta
from model import User,Organization,Employee

user=APIRouter(tags=["Register"])
from passlib.hash import bcrypt
import redis
@user.post("/register")
def register_user(background_taks:BackgroundTasks,u:UserIn):
    db=session()
    result=db.query(User).filter(User.email==u.email).first()
    if result:
        raise HTTPException(status_code=409,detail='User already exists')

    

    background_taks.add_task(email_generate,background_taks,u.email,u)
    return {"message","otp sent"}

@user.post('/signupotp')

def validate_otp(o:Otpin):
    redis_client=redis.Redis(host='localhost',port=6379)
    db=session()
    try:
        otp=redis_client.hget(o.email,'otp').decode('utf-8')
    except:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail="Time out")
    if otp is None:
        raise HTTPException(status_code=404,detail="Not found")
    try:
        attempts=redis_client.hget(o.email,'attempts').decode('utf-8')
    except:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail="Time out")
    if int(attempts)>5:
        redis_client.delete(o.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Attempts exceeded')
    try:
        redis_client.hset(o.email,'attempts',int(attempts)+1)
    except:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT,detail="Time out")
    if otp!=o.otp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="OTP not matched")
    
    json_data=redis_client.hget(o.email,'data').decode('utf-8')
    data=json.loads(json_data)
    
    useradmin=User(
        name=data['name'],
        email=data['email'],
        password_hash=bcrypt.hash(data['password']),
        ph_num=data['ph_num']
    )
    useradmin.admin=True
    db.add(useradmin)
    db.commit()
    redis_client.delete(o.email)
    return {'message':'Successfull created'}


JWT_SECRET='e1fbc4d156244e20b21f5efea02a125f3da866fba96d345a4c07970424b3d65e'
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/login')
@user.post("/login")
def get_token(loginData:OAuth2PasswordRequestForm=Depends()):
    db=session()
    result=db.query(User).filter(User.email==loginData.username,User.is_deleted==False).first()
    if not result:
        raise HTTPException(status_code=404, detail='User not found')
    p=bcrypt.verify(loginData.password,result.password_hash)
    if not p:
        raise HTTPException(status_code=404,detail='Details not found')
    x=datetime.utcnow()+timedelta(days=7)
    userout=UserOut(
        email=result.email,
        exp=x,
         #change it back to result.o_id
        admin=result.admin,
        o_id=1

    )
    token=jwt.encode(userout.model_dump(),JWT_SECRET)
    return {"access_token":token,"token_type":'bearer'}

async def autheniticate_user(token: str =Depends(oauth2_scheme)):
    
        db=session()
        
        user=jwt.decode(token,JWT_SECRET,algorithms=['HS256'])
        print(user)
        result=db.query(User).filter(User.email==user['email']).first()
        print(result)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user couldnt be authenticate')
        return user
    
@user.get("/users/me")
async def find_user(user=Depends(autheniticate_user)):
    return user






