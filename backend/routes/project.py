from pydantic import BaseModel
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from models import Projects, get_db, Paginate, ProjectMembers, Users
from auth import verify_token

router = APIRouter(tags=["project"])


class CreateProjectRequest(BaseModel):
    name: str
    description: str


class UpdateProjectRequest(BaseModel):
    name: str | None
    description: str | None


class PartialProject(BaseModel):
    id: int
    name: str


class ListProjectsResponse(BaseModel):
    projects: list[PartialProject]
    next_session: str


class InviteRequest(BaseModel):
    email: str


@router.get("s/create/{page_size}", response_model=ListProjectsResponse)
def create_project_pagination(
    page_size: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)
):
    paginate = Paginate(page_size)

    owned_projects = db.query(Projects.id, Projects.name).filter(
        Projects.owner_id == user_id
    )

    associated_projects = (
        db.query(Projects.id, Projects.name)
        .join(ProjectMembers, Projects.id == ProjectMembers.project_id)
        .filter(ProjectMembers.user_id == user_id)
    )

    combined_query = owned_projects.union(associated_projects)

    projects = paginate.apply(combined_query).all()
    paginate.next_page()

    projects = [PartialProject(id=project[0], name=project[1]) for project in projects]

    return ListProjectsResponse(projects=projects, next_session=paginate.to_token())


@router.get("s/{pagination}", response_model=ListProjectsResponse)
def list_projects(
    pagination: str, db: Session = Depends(get_db), user_id: int = Depends(verify_token)
):
    paginate = Paginate.from_token(pagination)

    owned_projects = db.query(Projects.id, Projects.name).filter(
        Projects.owner_id == user_id
    )

    associated_projects = (
        db.query(Projects.id, Projects.name)
        .join(ProjectMembers, Projects.id == ProjectMembers.project_id)
        .filter(ProjectMembers.user_id == user_id)
    )

    combined_query = owned_projects.union(associated_projects)

    projects = paginate.apply(combined_query).all()
    paginate.next_page()

    projects = [PartialProject(id=project[0], name=project[1]) for project in projects]

    return ListProjectsResponse(projects=projects, next_session=paginate.to_token())


@router.post("/", response_model=PartialProject)
def create_project(
    request: CreateProjectRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token),
):
    project = Projects(
        owner_id=user_id, name=request.name, description=request.description
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return PartialProject(id=project.id, name=project.name)


@router.patch("/{id}", response_model=PartialProject)
def update_project(
    id: int,
    request: UpdateProjectRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token),
):
    project = db.query(Projects).filter(Projects.id == id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if request.name is not None:
        project.name = request.name
    if request.description is not None:
        project.description = request.description
    db.commit()
    db.refresh(project)

    return PartialProject(id=project.id, name=project.name)


@router.delete("/{id}", response_model=PartialProject)
def delete_project(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)
):
    project = db.query(Projects).filter(Projects.id == id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(project)
    db.commit()

    return PartialProject(id=project.id, name=project.name)


@router.put("/{id}")
def invite_user(
    id: int,
    request: InviteRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token),
):
    project = db.query(Projects).filter(Projects.id == id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        guest = db.query(Users).filter(Users.email == request.email).first()

    guest = db.query(Users).filter(Users.email == request.email).first()
    if not guest:
        raise HTTPException(status_code=404, detail="User not found")

    pivot = ProjectMembers(project_id=id, user_id=guest.id)
    db.add(pivot)
    db.commit()
    db.refresh(pivot)
