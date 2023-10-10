from fastapi import APIRouter,status,HTTPException,Depends
from database import session
from schema import DesignationResponse,UpdateDesignation
from typing import List
from model import Designation
from users.user import autheniticate_user

desig=APIRouter(tags=['Designation'])

@desig.post("/designation")
def add_designation(des:DesignationResponse,user=Depends(autheniticate_user)):
    db=session()
    des_result=db.query(Designation).filter(Designation.des_name==des.des_name,Designation.is_deleted==False,Designation.o_id==user["o_id"]).first()
    if des_result:
        raise HTTPException(status_code=400,detail="Designation already exists")
    des_obj=Designation(des_name=des.des_name,o_id=user['o_id'])
    db.add(des_obj)
    db.commit()
    db.close()
    return {"message":"Inserted successfuly"}

@desig.get("/designation",response_model=List[DesignationResponse])
def retrive_designation(user=Depends(autheniticate_user)):
    db=session()
    des_result=db.query(Designation).filter(Designation.o_id==user['o_id'],Designation.is_deleted==False).all()
    result=[]
    for des_one in des_result:
        result.append(DesignationResponse(des_name=des_one.des_name))
    return result

@desig.put("/designation")
def update_designation(des:UpdateDesignation,user=Depends(autheniticate_user)):
    db=session()
    old_des_result=db.query(Designation).filter(Designation.des_name==des.old_des_name,Designation.is_deleted==False,Designation.o_id==user['o_id']).first()
    if not old_des_result:
        raise HTTPException(status_code=400,detail="Old Department doesn't exists")
    new_des_result=db.query(Designation).filter(Designation.des_name==des.new_des_name,Designation.is_deleted==False,Designation.o_id==user['o_id']).first()
    if new_des_result:
        raise HTTPException(status_code=400,detail="New Designation already exists")
    old_des_result.des_name=des.new_des_name
    db.commit()
    db.close()
    return {"message":"Successfully updated"}

@desig.delete("/designation")
def delete_designation(des:DesignationResponse,user=Depends(autheniticate_user)):
    db=session()
    des_result=db.query(Designation).filter(Designation.des_name==des.des_name,Designation.o_id==user['o_id'],Designation.is_deleted==False).first()
    if not des_result:
        raise HTTPException(status_code=404,detail="Designation not found")
    des_result.is_deleted=True
    db.commit()
    db.close()
    return {"message":"Successfuly deleted"}