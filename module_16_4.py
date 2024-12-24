from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
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


@app.post("/user", response_model=User)
async def create_user(
    user: User,
    username: Annotated[
        str,
        Path(
            min_length=5,
            max_length=20,
            description="Имя пользователя (от 5 до 20 символов)",
            example="UrbanUser"
        ),
    ],
    age: Annotated[
        int,
        Path(
            ge=18,
            le=120,
            description="Возраст пользователя (от 18 до 120 лет)",
            example=24
        ),
    ]
):
    # Проверка уникальности ID
    if any(existing_user.id == user.id for existing_user in users):
        raise HTTPException(status_code=400, detail="Пользователь с таким ID уже существует.")
    
    user.username = username
    user.age = age
    users.append(user)
    return user


@app.put("/user/{user_id}", response_model=User)
async def update_user(
    user_id: Annotated[
        int,
        Path(
            ge=0,
            description="ID пользователя для обновления",
            example=1
        ),
    ],
    username: Annotated[
        str,
        Path(
            min_length=5,
            max_length=20,
            description="Новое имя пользователя (от 5 до 20 символов)",
            example="UpdatedUser"
        ),
    ],
    age: Annotated[
        int,
        Path(
            ge=18,
            le=120,
            description="Новый возраст пользователя (от 18 до 120 лет)",
            example=30
        ),
    ]
):
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.username = username
            existing_user.age = age
            return existing_user
    
    raise HTTPException(status_code=404, detail="Пользователь не найден.")


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(
    user_id: Annotated[
        int,
        Path(
            ge=0,
            description="ID пользователя для удаления",
            example=1
        ),
    ]
):
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    
    raise HTTPException(status_code=404, detail="Пользователь не найден.")
