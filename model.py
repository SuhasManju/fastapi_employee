from sqlalchemy import Column, String,Integer,Boolean,ForeignKey,TEXT,DateTime
from typing import Optional
from sqlalchemy.sql import func

from sqlalchemy.orm import declarative_base
Base=declarative_base()
class Organization(Base):
    __tablename__='organization'
    o_id=Column(Integer,primary_key=True, autoincrement=True)
    org_name=Column(String(50))
    location=Column(String(50))
    industry=Column(String(50))
    org_date=Column(String(30))
    add_line1=Column(String(100))
    add_line2=Column(String(100),nullable=True)
    state=Column(String(50))
    pincode=Column(Integer)
    city=Column(String(50))
    is_deleted=Column(Boolean,default=False)

    def __init__(self,org_name,location,industry,org_date,add_line1,state,pincode,city,add_line2:Optional[str]=None):
        self.org_name=org_name
        self.location=location
        self.industry=industry
        self.add_line1=add_line1
        self.add_line2=add_line2
        self.state=state
        self.city=city
        self.pincode=pincode
        self.org_date=org_date
        self.is_deleted=False



class WorkLocation(Base):
    __tablename__='worklocation'
    w_id=Column(Integer,primary_key=True,autoincrement=True)
    location_name=Column(String(50))
    add_line1=Column(String(100))
    add_line2=Column(String(100),nullable=True)
    state=Column(String(50))
    city=Column(String(50))
    pincode=Column(Integer)
    o_id=Column(Integer,ForeignKey("organization.o_id"))
    is_deleted=Column(Boolean,default=False)
    

    def __init__(self, location_name,add_line1,state,city,pincode,o_id,add_line2:Optional[str]):
        self.location_name=location_name
        self.add_line1=add_line1
        self.add_line2=add_line2
        self.state=state
        self.city=city
        self.pincode=pincode
        self.o_id=o_id
        self.is_deleted=False
       
        


class Department(Base):
    __tablename__='department'
    d_id=Column(Integer, primary_key=True,autoincrement=True)
    dept_name=Column(String(50))
    dept_code=Column(String(50))
    description=Column(TEXT,nullable=True)
    o_id=Column(Integer,ForeignKey('organization.o_id'))
    w_id=Column(Integer,ForeignKey('worklocation.w_id'))
    is_deleted=Column(Boolean,default=False)

    

    def __init__(self,dept_name,dept_code,o_id,w_id,description: Optional[str]):
        self.dept_name=dept_name
        self.dept_code=dept_code
        self.o_id=o_id
        self.description=description
        self.w_id=w_id
        self.is_deleted=False
        

class Designation(Base):
    __tablename__="designation"
    des_id=Column(Integer,primary_key=True,autoincrement=True)
    des_name=Column(String(50))
    o_id=Column(Integer,ForeignKey('organization.o_id'))
    w_id=Column(Integer,ForeignKey('worklocation.w_id'))
    d_id=Column(Integer,ForeignKey('department.d_id'))
    is_deleted=Column(Boolean,default=False)


    

    def __init__(self,des_name,o_id,w_id,d_id):
        self.des_name=des_name
        self.o_id=o_id
        self.w_id=w_id
        self.d_id=d_id
        self.is_deleted=False
        
        
class PaySchedule(Base):
    __tablename__='payschedule'
    p_id=Column(Integer,primary_key=True,autoincrement=True)
    select_work_week=Column(String(50))
    calculate_salary_based_on =Column(String(50))
    pay_your_employee_on=Column(String(50))
    start_first_payroll=Column(String(50))
    salary_month_willbe_paidon=Column(String(50))
    # o_id=Column(Integer,ForeignKey("organization.o_id"))


    def __init__(self,select_work_week,calculate_salary_based_on,pay_your_employee_on,start_first_payroll,salary_month_willbe_paidon):
        self.select_work_week=select_work_week
        self.calculate_salary_based_on=calculate_salary_based_on
        self.pay_your_employee_on=pay_your_employee_on
        self.start_first_payroll=start_first_payroll
        self.salary_month_willbe_paidon=salary_month_willbe_paidon
        # self.o_id=o_id



class CompensatoryRequestScheduler(Base):
    __tablename__='compensatoryrequestscheduler'
    sch_id=Column(Integer,primary_key=True,autoincrement=True)
    schedule_name=Column(String(100))
    time_of_schedule=Column(String(50))
    date=Column(Integer)
    d_id=Column(Integer,ForeignKey('department.d_id'))
    des_id=Column(Integer,ForeignKey("designation.des_id"))
    w_id=Column(Integer,ForeignKey('worklocation.w_id'))
    include_overtime_done=Column(Boolean)


        
class User(Base):
    __tablename__='users'
    id=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String(100))
    email=Column(String(100),unique=True)
    password_hash=Column(String(256))
    ph_num=Column(String(20))
    admin=Column(Boolean)
    created_by=Column(Integer)
    updated_by=Column(Integer)
    is_deleted=Column(Boolean,default=False)

    def __init__(self,name,email,password_hash,ph_num):
        self.name=name
        self.email=email
        self.password_hash=password_hash
        self.ph_num=ph_num


class Employee(Base):
    __tablename__='employee'
    id=Column(Integer,primary_key=True,autoincrement=True)
    first_name=Column(String(50))
    last_name=Column(String(50))
    email=Column(String(50))
    department=Column(String(50))
    designation=Column(String(50))
    location=Column(String(50))
    role=Column(String(50))
    manager=Column(Integer)
    o_id=Column(Integer)
    added_by=Column(Integer)
    updated_by=Column(Integer)



    # def __init__(self,first_name,last_name,email,department,designation,location,role,manager,o_id):
    #     self.first_name=first_name
    #     self.last_name=last_name
    #     self.email=email
    #     self.department=department
    #     self.designation=designation
    #     self.location=location
    #     self.role=role
    #     self.manager=manager
    #     self.o_id=o_id

# class Organization(Base):
#     __tablename__ = 'organization'
#     id = Column(Integer, primary_key=True, index=True,autoincrement=True)
#     organization_name = Column(String(150),nullable=False)
#     organization_type =Column(String(100))
#     location=Column(String(50))
#     is_deleted =Column(Boolean,default =False)
#     created_by =Column(Integer)
#     updated_by =Column(Integer)
#     created_at = Column(DateTime, default=func.now())
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

#     def __init__(self, **kwargs):
#         super(Organization, self).__init__(**kwargs)
#         self.updated_at = func.now()



    
