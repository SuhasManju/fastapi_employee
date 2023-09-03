import smtplib
from random import randint
import redis
import json
#from users.userschema import UserIn
from pydantic import EmailStr
import pika

credentials=pika.PlainCredentials(username="guest",password="guest")
paramenter=pika.ConnectionParameters(host='localhost',port=5672,credentials=credentials)
connection=pika.BlockingConnection(paramenter)
channel=connection.channel()
channel.queue_declare(queue="employee_email_service",durable=False)


def email_generate(ch,method,properties,body):
    data=json.loads(body)

    smtp_obj=smtplib.SMTP('smtp.gmail.com',587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login('leeg13849@gmail.com','gdozktjbnsymujua')
    from_address='leeg13849@gmail.com'
    to_address=data['email']
    otp=str(randint(1001,9999))
    subject=" Sent a request to join there organization"
    message=f"OTP {data['email']} to signup into your account {otp}"
    try:
        smtp_obj.sendmail(from_address,to_address,message)
    except smtplib.SMTPRecipientsRefused:
        raise Exception(status_code=404,detail='Email not found')
    redis_client=redis.Redis(host='localhost',port=6379)
    #print(json.loads(body))

    redis_client.hset(data['userdata']['email'],mapping={'otp':otp,'data':json.dumps(data['userdata']),'attempts':0})
    redis_client.expire(data['userdata']['email'],300)

channel.basic_consume(queue='employee_email_service',auto_ack=True,on_message_callback=email_generate)
channel.start_consuming()