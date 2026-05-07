from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas import Todo, TodoCreate, User
from app import crud
from app.db import get_db
from app.auth import get_current_active_user

router = APIRouter()


@router.post("/todos", response_model=Todo)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return crud.create_todo(db, todo, current_user.id)


@router.get("/todos", response_model=List[Todo])
def get_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return crud.get_todos(db, current_user.id)


@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    updated_todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_todo = crud.update_todo(db, todo_id, updated_todo, current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    success = crud.delete_todo(db, todo_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Deleted"}
