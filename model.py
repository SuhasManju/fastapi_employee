from sqlalchemy import Column, String,Integer,Boolean,ForeignKey,TEXT,DateTime,Text,DATE
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
    gender=Column(String(10))
    marital_status=Column(String(10))
    employee_type=Column(String(10))
    source_of_hire=Column(String(10))
    o_id=Column(Integer)
    added_by=Column(Integer)
    updated_by=Column(Integer)
    joining_date=Column(DATE)
    nick_name=Column(String(50))
    dob=Column(DATE)
    about_me=Column(Text())
    Expertise=Column(Text())
    pan=Column(String(50))
    uan=Column(String(50))
    aadhaar=Column(String(50))
    ph_num=Column(String(50))
    seating_location=Column(String(10))
    Tags=Column(String(50))
    presentaddress=Column(String(50))
    permanentaddress=Column(String(50))
    person_ph_num=Column(String(50))
    personalemail_id=Column(String(50))
    workExperience=Column(Text())
    education_details=Column(Text())
    dependent_details=Column(Text())





class Mg_LeaveType(Base):
    __tablename__ = "mg_leave_type"
    id = Column(Integer, primary_key=True, index=True)
    leave_type_name = Column(String(50))
    leave_type_code = Column(String(20))
    leave_type = Column(String(20))
    unit = Column(String(30))
    balance_based_on = Column(String(50))
    description = Column(Text(),nullable=True)
    start_date = Column(String(50))
    end_date = Column(String(50))
    effictive_after = Column(String(100),nullable=True)
    effictive_from = Column(String(20),nullable=True)
    accural =Column(String(50),nullable=True)
    accural_by =Column(String(50),nullable=True) # accural by yearly,monthly etc
    accural_on=Column(String(50),nullable=True) #1st,2nd,3rd,4th etc
    accural_month_on = Column(String(50),nullable=True)#by month 
    accural_by_days=Column(String(10),nullable=True)
    accural_by_hour = Column(String(10),nullable=True)
    accural_in=Column(String(20),nullable=True)
    reset=Column(String(40),nullable=True)
    reset_by=Column(String(50),nullable=True)# by yearly,monthly etc
    reset_on=Column(String(50),nullable=True)
    reset_month_on = Column(String(50),nullable=True)
    reset_with = Column(String(50),nullable=True) # for carry_forward field and other
    reset_on_the = Column(String(50),nullable=True) #for storin number field
    reset_carry_by = Column(String(50),nullable=True) # for storing percentage or unit
    reset_carry_max_unit = Column(String(50),nullable=True)
    encashment = Column(String(10),nullable=True)
    encasment_by =Column(String(50),nullable=True)# encasment for storing percentage or unit
    encashment_max_unit=Column(String(50),nullable=True)
    prorate_accural=Column(String(50),nullable=True)
    prorate_by =Column(String(50),nullable=True)
    round_of_to =Column(String(50),nullable=True)
    round_of_start = Column(String(50),nullable=True)
    round_of_end = Column(String(50),nullable=True)
    first_month_from = Column(String(20),nullable=True)
    first_month_to =Column(String(20),nullable=True)
    first_month_count=Column(String(20),nullable=True)
    opening_balance = Column(String(50),nullable=True)
    maximum_balance=Column(String(50),nullable=True)
    deductible_holidays=Column(String(50),nullable=True)
    gender = Column(Text(),nullable=True)
    martial_status=Column(Text(),nullable=True)
    department = Column(Text(),nullable=True)
    designation=Column(Text(),nullable=True)
    location = Column(Text(),nullable=True)
    role = Column(Text(),nullable=True)
    employee_type =Column(Text(),nullable=True)
    source_of_hire = Column(Text(),nullable=True)
    onboarding_status=Column(String(40),nullable=True)
    employee=Column(Boolean,default=False)
    weekend_between_leave_period = Column(String(150),nullable=True)
    holidays_between_leave_period = Column(String(150),nullable=True)
    applying_leaves_excel_balance =Column(String(150),nullable=True)
    duraction_allowed =Column(Text(),nullable=True)
    allow_users_to_view = Column(String(50),nullable=True)
    balance_to_be_displayed = Column(String(50),nullable=True)
    allow_request_for_past_days =Column(String(50),nullable=True)
    allow_request_for_future_days =Column(Text(),nullable=True)
    maximum_leave_availed_per_application = Column(String(150),nullable=True)
    minimum_leave_availed_per_application = Column(String(150),nullable=True)
    maximim_number_consecutive_leave_allowed = Column(String(150),nullable=True)
    minimum_gap_between_two_apps = Column(String(150),nullable=True)
    enable_file_upload_option = Column(String(150),nullable=True)
    maximum_number_of_specific_period = Column(String(150),nullable=True)
    leave_applied_only_on =Column(Text(),nullable=True)
    leave_cannot_taken_with =Column(Text(),nullable=True)
    o_id=Column(Integer,ForeignKey("organization.o_id"))
    is_deleted = Column(Boolean, default=False)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    def __init__(self, **kwargs):
        super(Mg_LeaveType, self).__init__(**kwargs)
        self.updated_at = func.now()

    
class CurrentLeave(Base):
    __tablename__='currentleave'
    id=Column(Integer,primary_key=True,autoincrement=True)
    emp_id=Column(Integer,ForeignKey('employee.id'))
    leave_type=Column(Integer,ForeignKey("mg_leave_type.id"))
    num_of_leaves=Column(Integer)
    booked=Column(Integer)
    o_id=Column(Integer)
    def __init__(self, **kwargs):
        super(CurrentLeave, self).__init__(**kwargs)


class PersonalInformation(Base):
    __tablename__="PersonalInformation"
    id=Column(Integer,primary_key=True,autoincrement=True)
    first_name=Column(String(50))
    last_name=Column(String(50))
    middle_name=Column(String(50))
    gender=Column(String(50))
    location=Column(String(50))


    def __init__(self, **kwargs):
        super(PersonalInformation, self).__init__(**kwargs)

