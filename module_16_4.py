from fastapi import FastAPI, Path, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Хранилище пользователей
users = []

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users", response_model=List[User])
async def get_all_users():
    return users


@app.post("/user", response_model=str)
async def create_user(user: User):
    # Проверяем, существует ли пользователь с таким ID
    if any(existing_user.id == user.id for existing_user in users):
        raise HTTPException(status_code=400, detail="Пользователь с таким ID уже существует.")
    
    # Добавляем нового пользователя
    users.append(user)
    return f"Пользователь с ID {user.id} зарегистрирован."


@app.put("/user/{user_id}", response_model=str)
async def update_user(
    user_id: int = Path(ge=0, description="ID пользователя для обновления"),
    username: str = Path(min_length=5, max_length=20, description="Новое имя пользователя"),
    age: int = Path(ge=18, le=120, description="Новый возраст пользователя")
):
    # Ищем пользователя с указанным ID
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.username = username
            existing_user.age = age
            return f"Пользователь с ID {user_id} обновлен."
    
    raise HTTPException(status_code=404, detail="Пользователь не найден.")


@app.delete("/user/{user_id}", response_model=str)
async def delete_user(user_id: int = Path(ge=0, description="ID пользователя для удаления")):
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            users.pop(index)
            return f"Пользователь с ID {user_id} удален."
    
    raise HTTPException(status_code=404, detail="Пользователь не найден.")
