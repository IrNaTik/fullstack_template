from sqlalchemy.orm import Session
from faker import Faker

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path[0])

from app.models import User
from app.core.db import engine
from app.core.security import get_password_hash
from app.crud import create_user
from app.core.schemas import UserRegister

fake = Faker()

def generate_user_data():
    return 

def seed_data():
    users_data = [
        {
            "password": "12343243242",
            "email": "1aaacddcc@example.com"
        },
        {
            "password": "1234324324",
            "email": "1aaabdddb@example.com"
        }
    ]
    
    session = Session(engine)
    with session.begin():
        with session.begin_nested():
            for udata in users_data:
                user_data = UserRegister(
                        password=udata["password"],
                        email=udata["email"]
                )

                try:
                    user = create_user(session=session, user_register=user_data, auto_commit=False)
                except ValueError as e:
                    print(e)
            session.rollback()
        # The nested transaction will be released here automatically
    # The outer transaction will be committed here automatically
    
            
        
        

if __name__ == "__main__":
    seed_data()