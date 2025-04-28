from pydantic import BaseModel
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from models import Projects, get_db, ProjectMembers, Todos
from auth import verify_token

from typing import Optional

router = APIRouter(tags=["todo"])


class TodoModel(BaseModel):
    title: str
    priority: int
    project_id: int
    user_id: int
    content: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None
    created_at: Optional[datetime] = None

    def __init__(self, db_model: Todos):
        self.title = db_model.title
        self.priority = db_model.priority
        self.project_id = db_model.project_id
        self.user_id = db_model.user_id
        self.content = db_model.content
        self.due_date = db_model.due_date
        self.is_completed = db_model.is_completed
        self.created_at = db_model.created_at


class ListTodoResponse(BaseModel):
    todos: list[TodoModel]


@router.get("s/{project_id}", response_model=ListTodoResponse)
async def list_todos(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token),
):
    owned_projects = db.query(Projects.id, Projects.name).filter(
        Projects.owner_id == user_id
    )

    associated_projects = (
        db.query(Projects.id, Projects.name)
        .join(ProjectMembers, Projects.id == ProjectMembers.project_id)
        .filter(ProjectMembers.user_id == user_id)
    )

    combined_query = owned_projects.union(associated_projects)

    project = combined_query.filter(Projects.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    todos = db.query(Todos).filter(Todos.project_id == project_id).all()
    return ListTodoResponse(todos=[TodoModel(db_model=todo) for todo in todos])
