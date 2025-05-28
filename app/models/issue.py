# from __future__ import annotations
# from typing import Optional
# from datetime import datetime
# from uuid import UUID, uuid4
# from sqlmodel import SQLModel, Field, Relationship
# from sqlalchemy import CheckConstraint

# class Issue(SQLModel, table=True):
#     __tablename__ = "issue"
#     __table_args__ = (
#         CheckConstraint("status IN ('Assigned', 'In Progress', 'Review', 'Completed')", name="check_status"),
#         CheckConstraint("priority IN ('Low', 'Medium', 'High', 'Critical')", name="check_priority"),
#         CheckConstraint("type IN ('Bug', 'Task', 'Feature')", name="check_type"),
#     )

#     id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
#     title: str = Field(nullable=False)
#     description: Optional[str] = Field(default=None)
#     status: str = Field(nullable=False)
#     priority: str = Field(nullable=False)
#     type: str = Field(nullable=False)
#     project_id: UUID = Field(nullable=False, foreign_key="project.id")
#     assigned_to_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
#     created_by_id: UUID = Field(nullable=False, foreign_key="user.id")
#     created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
#     updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

#     # Relationships
#     project: Optional["Project"] = Relationship(back_populates="issues")
#     assigned_to: Optional["User"] = Relationship(back_populates="assigned_issues", sa_relationship_kwargs={"foreign_keys": "[Issue.assigned_to_id]"})
#     created_by: Optional["User"] = Relationship(back_populates="created_issues", sa_relationship_kwargs={"foreign_keys": "[Issue.created_by_id]"})


from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class IssueStatus(str, Enum):
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    COMPLETED = "COMPLETED"

class IssuePriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IssueType(str, Enum):
    BUG = "BUG"
    TASK = "TASK"
    FEATURE = "FEATURE"
    ENHANCEMENT = "ENHANCEMENT"

class IssueBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    priority: IssuePriority
    issue_type: IssueType

class Issue(IssueBase, table=True):
    __tablename__ = "issues"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    status: IssueStatus = Field(default=IssueStatus.OPEN)
    project_id: UUID = Field(foreign_key="projects.id")
    assigned_to_id: Optional[UUID] = Field(foreign_key="users.id", default=None)
    created_by_id: UUID = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Relationships
    project: Optional["Project"] = Relationship(back_populates="issues")
    assignee: Optional["User"] = Relationship(
        back_populates="assigned_issues",
        sa_relationship_kwargs={"foreign_keys": "Issue.assigned_to_id"}
    )
    creator: Optional["User"] = Relationship(
        back_populates="created_issues",
        sa_relationship_kwargs={"foreign_keys": "Issue.created_by_id"}
    )

class IssueCreate(IssueBase):
    project_id: UUID

class IssueResponse(IssueBase):
    id: UUID
    status: IssueStatus
    project_id: UUID
    assigned_to_id: Optional[UUID] = None
    created_by_id: UUID
    created_at: datetime

class IssueAssign(SQLModel):
    assigned_to_id: UUID

class IssueStatusUpdate(SQLModel):
    status: IssueStatus

class IssueWithDetails(IssueResponse):
    project_title: str
    assignee_name: Optional[str] = None
    creator_name: str