from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select
from ..config.db import get_session
from ..models.model import User
from pydantic import BaseModel
import bcrypt

router = APIRouter()

class UserLoginRequest(BaseModel):
    username: str
    password: str

# Define a response model
class LoginResponse(BaseModel):
    message: str


# Register Account
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

# Login
@router.post("/users/login", response_model=LoginResponse)
def login(body: UserLoginRequest, session: Session = Depends(get_session)):
    try:
        statement = select(User).where(User.username == body.username)
        user = session.exec(statement).one_or_none()
        
        if user is None or not bcrypt.checkpw(body.password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid username or password")
        
        # Return a successful login message
        return {"message": "Login successful", login: True}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error")

