from fastapi import APIRouter,status,HTTPException,Query
from database import  session
from schema import DesignationResponse,DeleteDesignation,InsertDesignation,UpdateDesignation
from typing import List
from model import Designation,Department,WorkLocation,Organization
desig=APIRouter(tags=['Designation'])

@desig.get('/designation',response_model=List[DesignationResponse])
def get_designation():
    db=session()
    result=db.query(Designation).all()
    if not result:
        raise HTTPException(status_code=404,detail="Designation not found")
    x=[]
    for r in result:
        org_result=db.query(Organization).filter(Organization.o_id==r.o_id).first()
        location_result=db.query(WorkLocation).filter(WorkLocation.w_id==r.w_id).first()
        dept_result=db.query(Department).filter(Department.d_id==r.d_id).first()
        if not (org_result and location_result and dept_result):
            continue
        org_name=org_result.org_name
        location_name=location_result.location_name
        dept_name=dept_result.dept_name
        i=DesignationResponse(
            des_name=r.des_name,
            org_name=org_name,
            location_name=location_name,
            dept_name=dept_name
        )
        x.append(i)

    return x

@desig.post("/designation")
def post_designation(d: InsertDesignation):
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
    if not dept_result:
        raise HTTPException(status_code=404,detail="Department not found")
    d_id=dept_result.d_id
    desig_result=db.query(Designation).filter(Designation.d_id==d_id,Designation.w_id==w_id,Designation.o_id==o_id,Designation.is_deleted==False).first()
    if desig_result:
        raise HTTPException(status_code=409,detail='Designation already exists')
    des=Designation(
        des_name=d.des_name,
        o_id=o_id,
        w_id=w_id,
        d_id=d_id
    )
    db.add(des)
    db.commit()
    return {"mesage":"Successfully created"}

@desig.put("/designation")
def update_designation(d: UpdateDesignation):
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
    old_d_id=old_dept_result.d_id
    if not old_dept_result:
        raise HTTPException(status_code=404,detail="Department not found")
    new_dept_result=db.query(Department).filter(Department.dept_name==d.new_dept_name,Department.o_id==new_o_id,Department.w_id==new_w_id,Department.is_deleted==False).first()
    new_d_id=new_dept_result.d_id
    if not new_dept_result:
        raise HTTPException(status_code=404,detail="Department not found")
    old_des_result=db.query(Designation).filter(Designation.des_name==d.old_des_name,Designation.o_id==old_o_id,Designation.w_id==old_w_id,Designation.d_id==old_d_id,Designation.is_deleted==False).first()
    if not old_des_result:
        raise HTTPException(status_code=404,detail='Designation not found')
    new_des_result=db.query(Designation).filter(Designation.des_name==d.new_des_name,Designation.o_id==new_o_id,Designation.w_id==new_w_id,Designation.d_id==new_d_id,Designation.is_deleted==False).first()
    if new_des_result:
        raise HTTPException(status_code=409,detail="Designation already exists")
    
    old_des_result.des_name=d.new_des_name
    old_des_result.o_id=new_o_id
    old_des_result.w_id=new_w_id
    old_des_result.d_id=new_d_id
    db.commit()
    return {"message":"Updated successfully"}

@desig.delete("/designation")
def delete_designation(d:DeleteDesignation):
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
    d_id=dept_result.d_id
    des_result=db.query(Designation).filter(Designation.des_name==d.des_name,Designation.o_id==o_id,Designation.w_id==w_id,Designation.d_id==d_id,Designation.is_deleted==False).first()
    if not des_result:
        raise HTTPException(status_code=404,detail="Designation not found")
    des_result.is_deleted=True
    db.commit()
    return {"message":"Deleted successfuly"}


@desig.get("/designation/department",response_model=List[str])
def get_specific_designation(org_name:str=Query(),location_name:str=Query(),dept_name:str=Query()):
    db=session()
    org_result=db.query(Organization).filter(Organization.org_name==org_name,Organization.is_deleted==False).first()
    if not org_result:
        raise HTTPException(status_code=404,detail="Organization not found")
    o_id=org_result.o_id
    workloc_result=db.query(WorkLocation).filter(WorkLocation.o_id==o_id,WorkLocation.location_name==location_name,WorkLocation.is_deleted==False).first()
    if not workloc_result:
        raise HTTPException(status_code=404,detail="Worklocation not found")
    w_id=workloc_result.w_id
    dept_result=db.query(Department).filter(Department.dept_name==dept_name,Department.o_id==o_id,Department.w_id==w_id,Department.is_deleted==False).first()
    if not dept_result:
        raise HTTPException(status_code=404,detail="Department not found")
    d_id=dept_result.d_id
    desig_result=db.query(Designation).filter(Designation.o_id==o_id,Designation.w_id==w_id,Designation.d_id==d_id,Designation.is_deleted==False).first()
    if not desig_result:
        raise HTTPException(status_code=404,detail="Designation not found")
    x=[]
    for r in desig_result:
        x.append(r.des_name)

    return x
    


