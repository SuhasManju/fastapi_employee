from fastapi import APIRouter,HTTPException,BackgroundTasks,Depends,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from users.userschema import UserIn,Otpin,UserOut,UserOut1
from database import session
import jwt
import json
from datetime import datetime,timedelta
from model import User,Organization,Employee
import pika
user=APIRouter(tags=["Register"])
from passlib.hash import bcrypt
import redis

JWT_SECRET='e1fbc4d156244e20b21f5efea02a125f3da866fba96d345a4c07970424b3d65e'

@user.post("/register")
def register_user(u:UserIn):
    db=session()
    result=db.query(User).filter(User.email==u.email).first()
    if result:
        raise HTTPException(status_code=409,detail='User already exists')
    
    credentials=pika.PlainCredentials(username="guest",password="guest")
    paramenter=pika.ConnectionParameters(host='localhost',port=5672,credentials=credentials)
    connection=pika.BlockingConnection(paramenter)
    channel=connection.channel()
    channel.queue_declare(queue="email_service",durable=False)
    body={'email':u.email,'userdata':u.model_dump()}
    channel.basic_publish("",'email_service',body=json.dumps(body))
    connection.close()

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
    admin_employee=Employee(first_name=data['name'],role='admin',email=data['email'],added_by=useradmin.id)
    db.add(admin_employee)
    db.commit()
    redis_client.delete(o.email)
    x=datetime.utcnow()+timedelta(days=7)
    userout=UserOut(
        email=useradmin.email,
        exp=x,
         #change it back to result.o_id
        admin=useradmin.admin,
        o_id=0

    )
    token=jwt.encode(userout.model_dump(),JWT_SECRET)
    return {"access_token":token,"token_type":'bearer'}



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







