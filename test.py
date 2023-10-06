from database import session
from pprint import pprint
import json
from datetime import datetime

db=session()
o_id=1
from model import CalenderSettings
result=db.query(CalenderSettings).filter(CalenderSettings.o_id==1).first()
calender=json.loads(result.weekend_definition)
pprint(calender)
