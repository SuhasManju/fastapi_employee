import smtplib
from random import randint
import redis
import json
import os
import dotenv
from pydantic import EmailStr
import pika

dotenv.load_dotenv()
credentials=pika.PlainCredentials(username=os.getenv("PIKA_USERNAME"),password=os.getenv("PIKA_PASSWORD"))
paramenter=pika.ConnectionParameters(host=os.getenv("PIKA_HOST"),port=5672,credentials=credentials)
connection=pika.BlockingConnection(paramenter)
channel=connection.channel()
channel.queue_declare(queue="email_service",durable=False)


def email_generate(ch,method,properties,body):
    data=json.loads(body)
    smtp_obj=smtplib.SMTP('smtp.gmail.com',587)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login(os.getenv('EMAIL_ID'),os.getenv('EMAIL_PASSWORD'))
    from_address=os.getenv('EMAIL_ID')
    to_address=data['email']
    otp=str(randint(1001,9999))
    subject='OTP to register'
    message=f"OTP to signup into your account {otp}"
    msg="Subject: "+subject+"\n"+message
    try:
        smtp_obj.sendmail(from_address,to_address,msg)
    except smtplib.SMTPRecipientsRefused:
        raise Exception(status_code=404,detail='Email not found')
    redis_client=redis.Redis(host='localhost',port=6379)
    #print(json.loads(body))

    redis_client.hset(data['email'],mapping={'otp':otp,'data':json.dumps(data['userdata']),'attempts':0})
    redis_client.expire(data['email'],300)

channel.basic_consume(queue='email_service',auto_ack=True,on_message_callback=email_generate)
channel.start_consuming()