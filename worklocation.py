from fastapi import FastAPI,HTTPException,status,APIRouter,Depends, Query
from database import session
from model import Organization, WorkLocation,Department,Designation
from typing import List
from schema import *

workloc=APIRouter(tags=['Worklocation'])

@workloc.get("/worklocation",response_model=List[WorkLocationResponse])
async def get_worklocation():
    db=session()
    workloc_result=db.query(WorkLocation).filter(WorkLocation.is_deleted==False).all()
    x=[]
    for r in workloc_result:
        org_result=db.query(Organization).filter(Organization.o_id==r.o_id,Organization.is_deleted==False).first()
        if not org_result:
            continue
        org_name=org_result.org_name
        i=WorkLocationResponse(
            location_name=r.location_name,
            add_line1=r.add_line1,
            add_line2=r.add_line2,
            state=r.state,
            city=r.city,
            pincode=r.pincode,
            org_name=org_name
        )
        x.append(i)
    return x


@workloc.post("/worklocation")
async def post_worklocation(w : WorkLocationResponse):
    db=session()
    org_result=db.query(Organization).filter(Organization.org_name==w.org_name,Organization.is_deleted==False).first()
    if not org_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Organization name not found')
    o_id=org_result.o_id
    result=db.query(WorkLocation).filter(WorkLocation.location_name==w.location_name,WorkLocation.o_id==o_id,WorkLocation.is_deleted==False).first()
    if result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Worklocation already exists")
    work=WorkLocation(w.location_name,w.add_line1,w.state,w.city,w.pincode,o_id,w.add_line2)
    db.add(work)
    db.commit()
    return {'message':'Successful insertion'}

@workloc.put('/worklocation')
async def put_worklocation(w: UpdateWorkLocation):
    db=session()
    old_org_result=db.query(Organization).filter(Organization.org_name==w.old_org_name,Organization.is_deleted==False).first()
    if not old_org_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Organization name not found')
    old_o_id=old_org_result.o_id
    new_org_result=db.query(Organization).filter(Organization.org_name==w.new_org_name,Organization.is_deleted==False).first()
    if not new_org_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Organization name not found')
    new_o_id=new_org_result.o_id
    old_work_result=db.query(WorkLocation).filter(WorkLocation.location_name==w.old_location_name,WorkLocation.o_id==old_o_id,WorkLocation.is_deleted==False).first()
    if not old_work_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Worklocation not found')
    new_work_result=db.query(WorkLocation).filter(WorkLocation.location_name==w.new_location_name,WorkLocation.o_id==new_o_id,WorkLocation.is_deleted==False).first()
    if new_work_result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='Worklocation already exists')
    
    old_work_result.location_name=w.new_location_name
    old_work_result.add_line1=w.add_line1
    old_work_result.add_line2=w.add_line2
    old_work_result.state=w.state
    old_work_result.pincode=w.pincode
    old_work_result.city=w.city
    old_work_result.o_id=new_o_id
    db.commit()

    return {"message": "Successful updation"}

@workloc.delete("/worklocation")
async def delete_worklocation(w: DeleteWorkLocation):
    db=session()
    org_result=db.query(Organization).filter(Organization.org_name==w.org_name,Organization.is_deleted==False).first()
    if not org_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Organization name not found')
    o_id=org_result.o_id
    result=db.query(WorkLocation).filter(WorkLocation.location_name==w.location_name,WorkLocation.o_id==o_id,WorkLocation.is_deleted==False).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Worklocation not found')
    result.is_deleted=True
    db.commit()
    return {"message": "Successful deletion"}

@workloc.get("/worklocation/organization",response_model=List[str])
def get_specific_worklocation(org_name:str=Query()):
    db=session()
    org_result=db.query(Organization).filter(Organization.org_name==org_name,Organization.is_deleted==False).first()
    if not org_result:
        raise HTTPException(status_code=404,detail='Organization not found')
    o_id=org_result.o_id
    result=db.query(WorkLocation).filter(WorkLocation.o_id==o_id,WorkLocation.is_deleted==False).all()
    if not result:
        raise HTTPException(status_code=404,detail="Worklocation not found")
    x=[]
    for r in result:
        x.append(r.location_name)

    return x