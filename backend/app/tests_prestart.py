from sqlalchemy.orm import Session
from faker import Faker

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path[0])

from app.models import User
from app.core.db import engine

fake = Faker()

def generate_user_data():
    return 

def seed_data():
    users_data = [
        {
            "name": "Alice",
            "emails": ["alice@example.com", "alice.work@example.com"]
        },
        {
            "name": "Bob",
            "emails": ["bob@example.com"]
        },
        {
            "name": "Charlie",
            "fullname": "Charlie Robintson",
            "emails": []
        }
    ]
    with Session(engine) as session:
        for udata in users_data:
            user = User()
            user_data = {
                "name": udata["name"],
                "fullname": udata.get("fullname")  # None, если нет
            }
            # Удаляем ключи с None, если хотите не передавать их вовсе
            user_data = {k: v for k, v in user_data.items() if v is not None}
            user = User(**user_data)
            user.addresses = [Address(email_address=email) for email in udata["emails"]]
            session.add(user)

        session.commit()


if __name__ == "__main__":
    seed_data()