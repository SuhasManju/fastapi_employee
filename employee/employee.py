from fastapi import APIRouter,status,Depends,HTTPException,BackgroundTasks
from database import session
from model import Employee,User
from users.user import autheniticate_user
from employee.employee_schema import EmployeeIn,EmployeeOut,Otpin

import redis
import json
from passlib.hash import bcrypt
import pika

employee=APIRouter(tags=['Employee'])

@employee.post("/employee")
def add_employee(emp_data:EmployeeIn,user=Depends(autheniticate_user)):
    db=session()
    if user['admin']!=True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You don't have the privlage to add employee")
    admin_result=db.query(User).filter(User.email==user['email']).first()
    if not admin_result:
        raise HTTPException(status_code=404,detail='Admin not found')
    user_result=db.query(Employee).filter(Employee.email==emp_data.email).first()
    if user_result:
        raise HTTPException(status_code=409,detail="Employee already exists")
    user_result1=db.query(Employee).filter(Employee.first_name==emp_data.first_name,Employee.last_name==emp_data.last_name).first()
    if user_result1:
        raise HTTPException(status_code=409,detail="Employee already exists")
    if emp_data.manager.last_name:
        manager_result=db.query(Employee).filter(Employee.first_name == emp_data.manager.first_name , Employee.last_name==emp_data.manager.last_name).first()
        if not manager_result:
            raise HTTPException(404,detail='Manager not found')
    else:
        manager_result=db.query(Employee).filter(Employee.first_name==emp_data.manager.first_name).first()
        if not manager_result:
            raise HTTPException(404,detail="Manager not found")
    
    emp=EmployeeOut(
        first_name=emp_data.first_name,
        last_name=emp_data.last_name,
        email=emp_data.email,
        department=emp_data.department,
        designation=emp_data.designation,
        location=emp_data.location,
        role=emp_data.role,
        manager=manager_result.id,
        o_id=user['o_id'],
        added_by=admin_result.id
    )
    credentials=pika.PlainCredentials(username="guest",password="guest")
    paramenter=pika.ConnectionParameters(host='localhost',port=5672,credentials=credentials)
    connection=pika.BlockingConnection(paramenter)
    channel=connection.channel()
    channel.queue_declare(queue="employee_email_service")
    body={'email':user['email'],'userdata':emp.model_dump()}
    channel.basic_publish("",'employee_email_service',body=json.dumps(body))
    connection.close()
   
    return {"message":'OTP sent'}

@employee.post("/employeeotp")
def confirm_employee(o:Otpin):
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
    emp=Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        department=data['department'],
        designation=data['designation'],
        location=data['location'],
        role=data['role'],
        manager=data['manager'],
        o_id=data['o_id']

    )
    emp.added_by=data['added_by']
    emp.updated_by=data['added_by']
    db.add(emp)
    db.commit()
    add_user=User(
        name=data['first_name']+" "+data['last_name'],
        email=data['email'],
        password_hash=bcrypt.hash(o.password),
        ph_num=None
                  )
    if emp.role=='admin':
        add_user.admin=True
    else:
        add_user.admin=False
    add_user.created_by=data['added_by']
    add_user.updated_by=data['added_by']
    db.add(add_user)
    db.commit()
    return {'message':'employee successfully added'}
    


    
    
    
    
    