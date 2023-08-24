from model import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
engine=create_engine("mysql://root:Suhas123@localhost/payroll",echo=True)
Base.metadata.create_all(bind=engine)
session=sessionmaker(bind=engine)