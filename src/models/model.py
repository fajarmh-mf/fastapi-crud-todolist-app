# user.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str
    created_at: datetime = Field(default_factory=datetime)
    updated_at: datetime = Field(default_factory=datetime)

    # Add a relationship to the Agenda model
    agendas: List["Agenda"] = Relationship(back_populates="user")

class Agenda(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    agenda: str
    is_done: bool
    created_at: datetime = Field(default_factory=datetime)
    updated_at: datetime = Field(default_factory=datetime)
    deleted_at: datetime = Field(default_factory=datetime)

    # Add a foreign key field to reference the User model
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # Add a relationship to the User model
    user: Optional["User"] = Relationship(back_populates="agendas")