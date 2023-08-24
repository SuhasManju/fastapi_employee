from model import Base
import os
from sqlalchemy.orm import sessionmaker
import dotenv
dotenv.load_dotenv()
from sqlalchemy import create_engine
engine=create_engine(f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}/payroll",echo=True)
Base.metadata.create_all(bind=engine)
session=sessionmaker(bind=engine)