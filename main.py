from fastapi import FastAPI,APIRouter
from payschedule import paysche
from organization import org
from worklocation import workloc
from department import depart
from designation import desig
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
app_router=APIRouter()

app_router.include_router(org)
app_router.include_router(workloc)

app_router.include_router(depart)
app_router.include_router(desig)
app_router.include_router(paysche)
app.include_router(app_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
