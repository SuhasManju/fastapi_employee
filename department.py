from fastapi import APIRouter,HTTPException,status,Query
from schema import DepartmentResponse,DeleteDepartment,InsertDepartment,UpdateDepartment
from model import Department,WorkLocation,Organization
from typing import List
from database import session
depart=APIRouter(tags=['department'])

@depart.get("/department",response_model=List[DepartmentResponse])
def get_department():
    db=session()
    result=db.query(Department).all()
    if not result:
        raise HTTPException(status_code=404,detail="Department not found")
    x=[]
    for r in result:
        org_result=db.query(Organization).filter(Organization.o_id==r.o_id,Organization.is_deleted==False).first()
        location_result=db.query(WorkLocation).filter(WorkLocation.w_id==r.w_id,WorkLocation.is_deleted==False).first()
        if not (org_result and location_result):
            continue
        org_name=org_result.org_name
        location_name=location_result.location_name
        i=DepartmentResponse(
            dept_name=r.dept_name,
            dept_code=r.dept_code,
            description=r.description,
            org_name=org_name,
            location_name=location_name
        )
        x.append(i)

    return x

@depart.get("/department/location",response_model=List[str])
def get_department_specific(org_name:str=Query(),location_name:str=Query()):
    db=session()
    org_result=db.query(Organization).filter(Organization.org_name==org_name,Organization.is_deleted==False).first()
    if not org_result:
        raise HTTPException(status_code=404,detail="Organization not found")
    o_id=org_result.o_id
    workloc_result=db.query(WorkLocation).filter(WorkLocation.location_name==location_name,WorkLocation.o_id==o_id,Organization.is_deleted==False).first()
    if not workloc_result:
        raise HTTPException(status_code=404, detail="Worklocation not found")
    w_id=workloc_result.w_id
    result=db.query(Department).filter(Department.o_id==o_id,Department.w_id==w_id,Department.is_deleted==False).all()
    if not result:
        raise HTTPException(status_code=404,detail="Department not found")
    x=[]
    for r in result:
        x.append(r.dept_name)
    return x



@depart.post("/department")
def post_department(d: InsertDepartment):
    db=session()
    org_result=db.query(Organization).filter(Organization.org_name==d.org_name,Organization.is_deleted==False).first()
    if not org_result:
        raise HTTPException(status_code=404,detail='Organization not found')
    o_id=org_result.o_id
    work_result=db.query(WorkLocation).filter(WorkLocation.location_name==d.location_name,WorkLocation.o_id==o_id,WorkLocation.is_deleted==False).first()
    if not work_result:
        raise HTTPException(status_code=404,detail="Worklocation not found")
    w_id=work_result.w_id
    dept_result=db.query(Department).filter(Department.dept_name==d.dept_name,Department.o_id==o_id,Department.w_id==w_id,Department.is_deleted==False).first()
    if dept_result:
        raise HTTPException(status_code=409, detail="Department already exists")
    dept=Department(d.dept_name,d.dept_code,o_id,w_id,d.description)
    db.add(dept)
    db.commit()
    return {"message":"Successful creation"}

@depart.put("/department")
def update_department(d: UpdateDepartment):
    db=session()
    old_org_result=db.query(Organization).filter(Organization.org_name==d.old_org_name,Organization.is_deleted==False).first()
    old_o_id=old_org_result.o_id
    if not old_org_result:
        raise HTTPException(status_code=404,detail='Organization not found')
    new_org_result=db.query(Organization).filter(Organization.org_name==d.new_org_name,Organization.is_deleted==False).first()
    if not new_org_result:
        raise HTTPException(status_code=404,detail='Organization not found')
    new_o_id=new_org_result.o_id
    old_workloc_result=db.query(WorkLocation).filter(WorkLocation.location_name==d.old_location_name,WorkLocation.o_id==old_o_id,WorkLocation.is_deleted==False).first()
    if not old_workloc_result:
        raise HTTPException(status_code=404, detail='Worklocation not found')
    old_w_id=old_workloc_result.w_id
    new_workloc_result=db.query(WorkLocation).filter(WorkLocation.location_name==d.new_location_name,WorkLocation.o_id==new_o_id,WorkLocation.is_deleted==False).first()
    if not new_workloc_result:
        raise HTTPException(status_code=404, detail='Worklocation not found')
    new_w_id=new_workloc_result.w_id
    old_dept_result=db.query(Department).filter(Department.dept_name==d.old_dept_name,Department.o_id==old_o_id,Department.w_id==old_w_id,Department.is_deleted==False).first()
    if not old_dept_result:
        raise HTTPException(status_code=404,detail="Department not found")
    new_dept_result=db.query(Department).filter(Department.dept_name==d.new_dept_name,Department.o_id==new_o_id,Department.w_id==new_w_id,Department.is_deleted==False).first()
    if new_dept_result:
        raise HTTPException(status_code=409,detail="Department already exists")
    old_dept_result.dept_name=d.new_dept_name
    old_dept_result.dept_code=d.dept_code
    old_dept_result.description=d.description
    old_dept_result.o_id=new_o_id
    old_dept_result.w_id=new_w_id
    db.commit()
    return {'message':'Updated successfuly'}

@depart.delete('/department')
def delete_department(d: DeleteDepartment):
    db=session()
    org_result=db.query(Organization).filter(Organization.org_name==d.old_org_name,Organization.is_deleted==False).first()
    o_id=org_result.o_id
    if not org_result:
        raise HTTPException(status_code=404,detail='Organization not found')
    work_result=db.query(WorkLocation).filter(WorkLocation.location_name==d.location_name,WorkLocation.o_id==o_id,WorkLocation.is_deleted==False).first()
    if not work_result:
        raise HTTPException(status_code=404,detail="Worklocation not found")
    w_id=work_result.w_id
    dept_result=db.query(Department).filter(Department.dept_name==d.dept_name,Department.o_id==o_id,Department.w_id==w_id,Department.is_deleted==False).first()
    if not dept_result:
        raise HTTPException(status_code=404,detail="Department not found")
    db.delete(dept_result)
    db.commit()
    return {"message": " Deleted successfuly"}

    

    
    
    
        



