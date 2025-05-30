# from __future__ import annotations
# from typing import List
# from datetime import datetime
# from uuid import UUID, uuid4
# from sqlmodel import SQLModel, Field, Relationship
# from sqlalchemy import CheckConstraint

# class User(SQLModel, table=True):
#     __tablename__ = "user"
#     __table_args__ = (
#         CheckConstraint("role IN ('PM', 'Developer', 'Designer')", name="check_role"),
#     )

#     id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
#     email: str = Field(nullable=False, unique=True, index=True)
#     username: str = Field(nullable=False, unique=True, index=True)
#     password_hash: str = Field(nullable=False)
#     role: str = Field(nullable=False)
#     created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
#     updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

#     # Use string-based forward references
#     projects: List["Project"] = Relationship(back_populates="pm")
#     assigned_issues: List["Issue"] = Relationship(back_populates="assigned_to", sa_relationship_kwargs={"foreign_keys": "[Issue.assigned_to_id]"})
#     created_issues: List["Issue"] = Relationship(back_populates="created_by", sa_relationship_kwargs={"foreign_keys": "[Issue.created_by_id]"})


from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from pydantic import EmailStr

class UserRole(str, Enum):
    PM = "PM"
    DEVELOPER = "Developer"
    DESIGNER = "Designer"

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=100)
    role: UserRole
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    password_hash: str = Field(max_length=255)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Relationships
    managed_projects: List["Project"] = Relationship(back_populates="project_manager")
    created_issues: List["Issue"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "Issue.created_by_id"}
    )
    assigned_issues: List["Issue"] = Relationship(
        back_populates="assignee",
        sa_relationship_kwargs={"foreign_keys": "Issue.assigned_to_id"}
    )

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    created_at: datetime

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    email: Optional[str] = None