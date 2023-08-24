from fastapi import HTTPException,status,APIRouter
from database import session
from model import Organization,WorkLocation
from typing import List

from schema import *

org=APIRouter()
@org.get("/organization",response_model=List[OrganizationResponse],tags=['organization'])
async def get_organization():
    db=session()
    result=db.query(Organization).filter(Organization.is_deleted==False).all()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No data found')
    r=[]
    
    for i in result:
        v= OrganizationResponse(
           
            org_name=i.org_name,
            location=i.location,
            industry=i.industry,
            org_date=i.org_date,
            add_line1=i.add_line1,
            add_line2=i.add_line2,
            state=i.state,
            pincode=i.pincode,
            city=i.city)
        r.append(v)
        
    return r

@org.post("/organization",tags=['organization'])
async def insert_organization(o: InsertOrganization):
    db=session()
    result=db.query(Organization).filter(Organization.org_name==o.org_name,Organization.location==o.location,Organization.industry==o.industry,Organization.org_date==o.org_date,Organization.add_line1==o.add_line1,Organization.add_line2==o.add_line2,Organization.state==o.state,Organization.pincode==o.pincode,Organization.city==o.city,Organization.is_deleted==False).all()
    if result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="already exists")
    else:
        o1=Organization(o.org_name,o.location,o.industry,o.org_date,o.add_line1,o.state,o.pincode,o.city,o.add_line2)
        db.add(o1)
        db.commit()
        db.refresh(o1)
        o_id=o1.o_id
        workloc=WorkLocation(o.location,o.add_line1,o.state,o.city,o.pincode,o_id,o.add_line2)
        db.add(workloc)
        db.commit()

        message={'message':"Successful creation"}
        return message
    
@org.put("/organization",tags=['organization'])
async def update_organization(o : UpdateOrganization):
    db=session()
    old_result=db.query(Organization).filter(Organization.org_name==o.new_name,Organization.is_deleted==False).first()
    if old_result:
        raise HTTPException(status_code=409,detail="New organization already exists")
    result=db.query(Organization).filter(Organization.org_name==o.existing_name,Organization.is_deleted==False).all()
    if result:
        r=result[0]
        r.org_name=o.new_name
        r.location=o.location
        r.industry=o.industry
        r.org_date=o.org_date
        r.add_line1=o.add_line1
        r.add_line2=o.add_line2
        r.state=o.state
        r.city=o.city
        r.pincode=o.pincode
        db.commit()
        db.refresh(r)
        return {"message":"Successful updation"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Organization name not found")

@org.delete("/organization",tags=['organization'])
async def delete_organization(o : DeleteOrganization):
    db=session()
    result=db.query(Organization).filter(Organization.org_name==o.org_name,Organization.is_deleted==False).all()
    if result:
        r=result[0]
        r.is_deleted=True
        db.commit()
        return {"message":"Sucessful deletion"}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Organization name not found")