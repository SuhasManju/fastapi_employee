from fastapi import APIRouter,status,Depends,HTTPException,BackgroundTasks
from database import session
from model import Employee,User
from users.user import autheniticate_user
from employee.employee_schema import EmployeeIn,EmployeeOut,Otpin
from datetime import datetime
from employee.employe_background import addcurrentleave

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
    try:
        joining_date=(datetime.strptime(emp_data.joining_date,"%Y/%m/%d"))
        dob=datetime.strptime(emp_data.dob,"%Y/%m/%d")
    except:
        raise HTTPException(status_code=422,detail="Date object not found")
    work_experience=[]
    for i in emp_data.work_experience:
        work_experience.append(i.model_dump())
    education_details=[]
    for i in emp_data.education_details:
        education_details.append(i.model_dump())
    dependent_details=[]
    for i in emp_data.education_details:
        education_details.append(i.model_dump())
    print(dob.date())
    print(joining_date.date())
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
        added_by=admin_result.id,
        joining_date=str(joining_date.date()),
        nick_name=emp_data.nick_name,
        dob=str(dob.date()),
        about_me=emp_data.about_me,
        Expertise=emp_data.Expertise,
        pan=emp_data.pan,
        uan=emp_data.uan,
        aadhaar=emp_data.aadhaar,
        ph_num=emp_data.ph_num,
        seating_location=emp_data.seating_location,
        Tags=emp_data.Tags,
        presentaddress=emp_data.presentaddress,
        permanentaddress=emp_data.permanentaddress,
        person_ph_num=emp_data.person_ph_num,
        personalemail_id=emp_data.personalemail_id,
        work_experience=json.dumps(work_experience),
        education_details=json.dumps(education_details),
        dependent_details=json.dumps(dependent_details),
        gender=emp_data.gender,
        marital_staus=emp_data.marital_staus,
        employee_type=emp_data.employee_type,
        source_of_hire=emp_data.source_of_hire
    )
    credentials=pika.PlainCredentials(username="guest",password="guest")
    paramenter=pika.ConnectionParameters(host='localhost',port=5672,credentials=credentials)
    connection=pika.BlockingConnection(paramenter)
    channel=connection.channel()
    channel.queue_declare(queue="employee_email_service",durable=False)
    body={'email':emp.email,'userdata':emp.model_dump()}
    channel.basic_publish("",'employee_email_service',body=json.dumps(body))
    connection.close()
   
    return {"message":'OTP sent'}

@employee.post("/employeeotp")
def confirm_employee(backGroundTasks:BackgroundTasks,o:Otpin):
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
        gender=data['gender'],
        marital_status=data['marital_staus'],
        employee_type=data['employee_type'],
        source_of_hire=data['source_of_hire'],
        manager=data['manager'],
        o_id=data['o_id'],
        joining_date=data['joining_date'],
        nick_name=data['nick_name'],
        dob=data['dob'],
        about_me=data['about_me'],
        Expertise=data['Expertise'],
        pan=data['pan'],
        uan=data['uan'],
        aadhaar=data['aadhaar'],
        ph_num=data['ph_num'],
        seating_location=data['seating_location'],
        Tags=data['Tags'],
        presentaddress=data['presentaddress'],
        permanentaddress=data['permanentaddress'],
        person_ph_num=data['person_ph_num'],
        personalemail_id=data['personalemail_id'],
        workExperience=data['work_experience'],
        education_details=data['education_details'],
        dependent_details=data['dependent_details']

    )
    emp.added_by=data['added_by']
    emp.updated_by=data['added_by']
    db.add(emp)
    db.commit()
    add_user=User(
        name=data['first_name']+" "+data['last_name'],
        email=data['email'],
        password_hash=bcrypt.hash(o.password),
        ph_num=data['ph_num']
                  )
    if emp.role=='admin':
        add_user.admin=True
    else:
        add_user.admin=False
    add_user.created_by=data['added_by']
    add_user.updated_by=data['added_by']
    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    backGroundTasks.add_task(addcurrentleave,backGroundTasks,emp.id,emp.o_id)
    db.commit()
    return {'message':'employee successfully added'}
    


    
    
    
    
    