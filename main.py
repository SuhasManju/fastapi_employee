from fastapi import FastAPI,APIRouter
from payschedule import paysche
from organization import org
from worklocation import workloc
from department import depart
from designation import desig
from users.user import user
from employee.employee import employee
from leave_type.leave_type import leave_type
from currentleave.currentleave import currentleave_router
from personalinformation.perinformation import perinformrouter
from calender_settings.calender import calender
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app_router=APIRouter()

app_router.include_router(org)
app_router.include_router(workloc)

app_router.include_router(depart)
app_router.include_router(desig)
app_router.include_router(paysche)
app_router.include_router(user)
app_router.include_router(employee)
app_router.include_router(leave_type)
app_router.include_router(currentleave_router)
app_router.include_router(perinformrouter)
app_router.include_router(calender)
app.include_router(app_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
