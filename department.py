from fastapi import APIRouter,HTTPException,status,Depends
from schema import InsertDepartment,UpdateDepartment,DeleteDepartment
from model import Department
from typing import List
from database import session
from users.user import autheniticate_user

depart=APIRouter(tags=['department'])

@depart.post("/department")
def add_department(dep:InsertDepartment,user=Depends(autheniticate_user)):
    db=session()
    dep_result=db.query(Department).filter(Department.dept_name==dep.dept_name,Department.o_id==user['o_id'],Department.is_deleted==False).first()
    if dep_result:
        raise HTTPException(status_code=400,detail="Department already exists")
    dep_obj=Department(dept_name=dep.dept_name,dept_code=dep.dept_code,o_id=user['o_id'],description=dep.description)
    db.add(dep_obj)
    db.close()
    return {'message':"successfuly created"}

@depart.get("/department",response_model=List[InsertDepartment])
def retrive_department(user=Depends(autheniticate_user)):
    db=session()
    dep_result=db.query(Department).filter(Department.o_id==user['o_id'],Department.is_deleted==False).all()
    if not dep_result:
        raise HTTPException(status_code=404,detail="Department not found")
    result=[]
    for dep_one in dep_result:
        result.append(InsertDepartment(dept_name=dep_one.dept_name,dept_code=dep_one.dept_code,description=dep_one.description))
    db.close()
    return result

@depart.put("/department")
def update_department(dep:UpdateDepartment,user=Depends(autheniticate_user)):
    db=session()
    dep_result=db.query(Department).filter(Department.dept_name==dep.old_dept_name,Department.o_id==user['o_id'],Department.is_deleted==False).first()
    if not dep_result:
        raise HTTPException(status_code=404,detail="Department not found")
    new_dep_result=db.query(Department).filter(Department.dept_name==dep.new_dept_name,Department.is_deleted==False,Department.o_id==user['o_id']).first()
    if new_dep_result:
        raise HTTPException(status_code=400,detail="Department alread exists")
    dep_result.dept_code=dep.dept_code
    dep_result.dept_name=dep.new_dept_name
    dep_result.description=dep.description
    db.commit()
    db.close()
    return {'message':"Department successfuly update"}

@depart.delete("/department")
def delete_department(dep:DeleteDepartment,user=Depends(autheniticate_user)):
    db=session()
    dep_result=db.query(Department).filter(Department.dept_name==dep.dept_name,Department.o_id==user['o_id'],Department.is_deleted==False).first()
    if not dep_result:
        raise HTTPException(status_code=404,detail="Department not found")
    dep_result.is_deleted=True
    db.commit()
    db.close()
    return {"message":"Successfully deleted"}


    

    
    
    
        



