from sqlalchemy import Column,Integer,String,TIMESTAMP
from db.database import base

class UserLogin(base):
    __tablename__="signup"

    user_id= Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    created_at=Column(TIMESTAMP)
    updated_at=Column(TIMESTAMP)
    
   

