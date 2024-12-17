from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/user")
async def get_user():
    return users


@app.post('/user/{username}/{age}')
async def users_info(username: str, age: int):
    new_user = User(id=len(users) + 1, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int):
    try:
        users[user_id - 1] = User(id=user_id, username=username, age=age)
        return users[user_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail="User was notfound")


@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    if user_id == users[user_id - 1].id:
        return users.pop(user_id - 1)
    else:
        raise HTTPException(status_code=404, detail="User was not found")




# python -m uvicorn Module_16.Lesson_4.module_16_4:app
