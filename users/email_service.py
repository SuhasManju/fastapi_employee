import smtplib
from random import randint
import redis
import json
from users.userschema import UserIn
from pydantic import EmailStr
from fastapi import BackgroundTasks,HTTPException

def email_generate(background_tasks:BackgroundTasks,email:EmailStr,user:UserIn):
    smtp_obj=smtplib.SMTP('smtp.gmail.com',587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login('leeg13849@gmail.com','gdozktjbnsymujua')
    from_address='leeg13849@gmail.com'
    to_address=email
    otp=str(randint(1001,9999))
    subject='OTP to register'
    message=f"OTP to signup into your account {otp}"
    msg="Subject: "+subject+"\n"+message
    try:
        smtp_obj.sendmail(from_address,to_address,msg)
    except smtplib.SMTPRecipientsRefused:
        raise HTTPException(status_code=404,detail='Email not found')
    redis_client=redis.Redis(host='localhost',port=6379)
    #redis_client.set(name=email,value=otp,ex=300)

    redis_client.hmset(email,{'otp':otp,'data':json.dumps(user.model_dump()),'attempts':0})
    redis_client.expire(email,300)
