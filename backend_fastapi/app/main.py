from typing import Union, Optional, List
from fastapi import FastAPI, Depends, status, HTTPException
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.database import get_db
from db.models import User
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
load_dotenv()

app = FastAPI()

#user in scehma
class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password: Optional[str]=None
    imageUrl : Optional[str]=None

class UserOut(BaseModel):
    id:uuid.UUID
    name:str
    email: EmailStr
    imageUrl : Optional[str]

    created_At: datetime

    class Config():
        orm_mode=True









@app.get("/")
def read_root():
    return {"shit":"mix"}

@app.get("/items/{item_id}")
def read_item(item_id:int, q: Union[str, None]= None):
    return {"item_id":item_id, "q":q}


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in:UserCreate,
    session:AsyncSession= Depends(get_db)
    ):
    res = await session.execute(
        select(User).where(User.email == user_in.email)
    )

    if res.scalar_one_or_none:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Emails already register")
    
    new_user = User(
        id= uuid.uuid4(),
        name = user_in.name,
        email = user_in.email,
        password= user_in.password,
        imageUrl= user_in.imageUrl,   
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user 

@app.get("/users", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def get_users(
    session:AsyncSession=Depends(get_db)
    ):
    res = await session.execute(
        select(User)
    )

    users = res.scalars().all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    
    return users

