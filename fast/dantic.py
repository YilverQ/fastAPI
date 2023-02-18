from datetime import date
from pydantic import BaseModel

# Un modelo de Pydantic
class User(BaseModel):
    id: int
    name: str
    joined: date


my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}
my_second_user: User = User(**second_user_data)

print(second_user_data)
print(my_user)
print(my_second_user)
print(type(my_second_user))