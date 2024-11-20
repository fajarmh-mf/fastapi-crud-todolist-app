from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select
from ..config.db import get_session
from ..models.model import User
import bcrypt

router = APIRouter()


@router.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed

    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/", response_model=list[User])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
