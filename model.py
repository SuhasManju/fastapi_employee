from sqlalchemy import Column, String,Integer,Boolean,ForeignKey,TEXT
from typing import Optional

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

        




    
