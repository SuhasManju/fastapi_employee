from sqlalchemy import Column, String,Integer,Boolean,ForeignKey,TEXT,DateTime,Text,DATE,Time
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
    is_deleted=Column(Boolean,default=False)

    

    def __init__(self,dept_name,dept_code,o_id,description: Optional[str]):
        self.dept_name=dept_name
        self.dept_code=dept_code
        self.o_id=o_id
        self.description=description
        self.is_deleted=False
        

class Designation(Base):
    __tablename__="designation"
    des_id=Column(Integer,primary_key=True,autoincrement=True)
    des_name=Column(String(50))
    o_id=Column(Integer,ForeignKey('organization.o_id'))
    is_deleted=Column(Boolean,default=False)


    

    def __init__(self,des_name,o_id):
        self.des_name=des_name
        self.o_id=o_id
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
    created_by=Column(Integer)
    updated_by=Column(Integer)
    admin=Column(Boolean)
    is_deleted=Column(Boolean,default=False)





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
    is_deleted=Column(Boolean,default=False)





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

class CalenderSettings(Base):
    __tablename__="CalenderSettings"
    id=Column(Integer,primary_key=True,autoincrement=True)
    location=Column(Integer,ForeignKey('worklocation.w_id'))
    week_starts_on=Column(String(50))
    work_week_start_on=Column(String(50))
    work_week_end_on=Column(String(50))
    half_full_day=Column(String(50))
    calender_starts=Column(String(50))
    calender_ends=Column(String(50))
    weekend_definition=Column(Text())
    statutory_weekend=Column(Boolean)
    created_by=Column(Integer)
    updated_by=Column(Integer)
    o_id=Column(Integer)
    def __init__(self,**kwargs):
        super(CalenderSettings,self).__init__(**kwargs)

class Shifts(Base):
    __tablename__="shifts"
    id=Column(Integer,primary_key=True,autoincrement=True)
    shift_name =Column(String(50))
    start_from = Column(Time)
    to_time =Column(Time)
    shift_margin =Column(Boolean,default=False)
    hours_befor_shift = Column(String(50))
    hours_after_shift=Column(String(50))
    weekend =Column(String(150))
    half_working_and_half_weekend =Column(Boolean,default=False)
    weekend_defination =Column(Text())
    department = Column(Text())
    location = Column(Text())
    division =Column(Text())
    created_by=Column(Integer)
    updated_by=Column(Integer)
    o_id=Column(Integer,ForeignKey("organization.o_id"))
    is_deleted= Column(Boolean,default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        super(Shifts, self).__init__(**kwargs)
        self.updated_at = func.now()

class EmployeeCalender(Base):
    __tablename__="employeecalender"
    id=Column(Integer,primary_key=True,autoincrement=True)
    emp_id=Column(Integer,ForeignKey("employee.id",ondelete="CASCADE",onupdate="CASCADE"),nullable=False)
    month=Column(Integer,nullable=False)
    calender=Column(Text())
    o_id=Column(Integer,ForeignKey("organization.o_id",ondelete="CASCADE",onupdate="CASCADE"))
    
    def __init__(self,**kwargs):
        super(EmployeeCalender,self).__init__(**kwargs)
        
class Attendance(Base):
    __tablename__='Attendance'
    id=Column(Integer,primary_key=True,autoincrement=True)
    emp_id=Column(Integer,ForeignKey("employee.id",ondelete="CASCADE",onupdate="CASCADE"),nullable=False)
    date=Column(DATE)
    check_in=Column(Time(),nullable=False)
    check_out=Column(Time())
    check_in_location_coord=Column(Text())
    check_out_location_coord=Column(Text())

    def __init__(self,**kwargs):
        super(Attendance,self).__init__(**kwargs)

    
class Attendance_General_settings(Base):
    __tablename__ = "attendance_general_settings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    effictive_from = Column(String(100))
    default_shift_time = Column(String(100))
    scale_view =Column(Boolean,default=False)
    total_hour_calculation =Column(Text())
    minimum_hours_required =Column(Text())
    strict_mode_manual=Column(Boolean,default=False)
    strict_mode_full_day=Column(String(50))
    strict_mode_half_day=Column(String(50))
    strict_shift_hours_full_day=Column(String(150))
    strict_shift_hour_half_day=Column(String(150))
    lenient_mode_manual =Column(Boolean,default=False)
    lenient_mode_per_day=Column(String(50))
    lenient_mode_shift =Column(String(50))
    show_overtime_deveation=Column(Boolean,default=False)
    maximum_hours_required=Column(Boolean,default=False)
    round_off =Column(Boolean,default=False)
    first_check_in = Column(String(50))
    last_check_out=Column(String(50))
    worked_hours=Column(String(50))     
    enable_tracking=Column(Boolean,default=False)
    location =Column(Text())
    start_time=Column(String(50))
    end_time=Column(String(50))
    shift_margin_enable=Column(Boolean,default=False)
    web_check_in_out=Column(Boolean,default=False)
    mobile_check_in_out=Column(Boolean,default=False)
    show_all_check_in_out=Column(Boolean,default=False)
    view_report_entries=Column(Boolean,default=False)
    edit_report_entries=Column(Boolean,default=False)
    edit_own_entries=Column(Boolean,default=False)
    show_attendance_report = Column(Text())
    show_balance_over_time=Column(Text())
    edit_balance_over_time=Column(Text())
    track_in_out_location=Column(Boolean,default=False)
    restrict_in_out_entries=Column(Boolean,default=False)
    view_emp_shift_map =Column(Text())
    edit_emp_shift_map=Column(Text())
    allow_changing_shifts=Column(Boolean,default=False)
    email_notification_modify=Column(Boolean,default=False)
    feeds_notification_modify=Column(Boolean,default=False)
    eligibility_shift_allowence=Column(String(50))
    make_reason_mandatory=Column(Boolean,default=False)
    o_id=Column(Integer,ForeignKey("organization.o_id"))
    is_deleted = Column(Boolean, default=False)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        super(Attendance_General_settings, self).__init__(**kwargs)
        self.updated_at = func.now()

class Absent_Schedule(Base):
    __tablename__="AbsentSchedule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(50),nullable=False)
    schedule_run=Column(Time(),nullable=False)
    process_data=Column(Integer,nullable=False)
    push_absense_to_leave_module=Column(Boolean())
    notify_through_email=Column(Boolean())
    department=Column(Text())
    designation=Column(Text())
    location=Column(Text())
    role=Column(Text())
    o_id=Column(Integer,ForeignKey("organization.o_id",ondelete='CASCADE',onupdate='CASCADE'))
    created_by=Column(Integer)
    updated_by=Column(Integer)
<<<<<<< HEAD
    is_deleted=Column(Boolean,default=False)
=======
>>>>>>> 3e67ed621641160a9c0a260a5c32f5e35fbccc23

    def __init__(self,**kwargs):
        super(Absent_Schedule,self).__init__(**kwargs)

class Present_Default(Base):
    __tablename__='PresentDefault'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50))
    users=Column(Text())
    effective_from = Column(DATE)
    effective_to = Column(DATE)
    reason= Column(Text())
    o_id=Column(Integer,ForeignKey("organization.o_id",ondelete='CASCADE',onupdate='CASCADE'))
    created_by=Column(Integer)
    updated_by=Column(Integer)
<<<<<<< HEAD
    is_deleted=Column(Boolean,default=False)
=======
>>>>>>> 3e67ed621641160a9c0a260a5c32f5e35fbccc23

    def __init__(self,**kwargs):
        super(Present_Default,self).__init__(**kwargs)
    
