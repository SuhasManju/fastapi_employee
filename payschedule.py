from model import PaySchedule

from fastapi import APIRouter,Depends,HTTPException,status
from schema import PayScheduleResponse,InsertPaySchedule
from database import session

paysche=APIRouter(tags=['payschedule'])

@paysche.get('/payschedule',response_model=list[PayScheduleResponse])
def get_payschedule():
    db=session()
    result=db.query(PaySchedule).all()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No payschedule were found")
    
    x=[]
    for r in result:

        i=PayScheduleResponse(
            
            select_work_week=r.select_work_week,
            calculate_salary_based_on=r.calculate_salary_based_on,
            pay_your_employee_on=r.pay_your_employee_on,
            start_first_payroll=r.start_first_payroll,
            salary_month_willbe_paidon=r.salary_month_willbe_paidon
            
        )
        
        x.append(i)

    return x

@paysche.post("/payschedule")
def post_payschedule(p:InsertPaySchedule):
    db=session()
   

    if len(p.select_work_week)<4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="minimum four work days required")

    for x in p.select_work_week:
        # pay=PaySchedule(=x,p.calculate_salary_based_on,p.pay_your_employee_on,p.start_first_payroll,p.salary_month_willbe_paidon,result.o_id)
        pay=PaySchedule(
            select_work_week=x,
            calculate_salary_based_on=p.calculate_salary_based_on,
            pay_your_employee_on=p.pay_your_employee_on,
            start_first_payroll=p.start_first_payroll,
            salary_month_willbe_paidon=p.salary_month_willbe_paidon,
            
        )
        db.add(pay)
        db.commit()
        #print(x,"dsgsg")

    return {"message":'insertion successful'}
