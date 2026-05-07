from sqlalchemy.orm import Session
from app import models, schemas


def get_todos(db: Session, user_id: int):
    return db.query(models.TodoModel).filter(models.TodoModel.owner_id == user_id).all()


def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.TodoModel(
        title=todo.title,
        completed=todo.completed,
        owner_id=user_id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, updated_todo: schemas.TodoCreate, user_id: int):
    db_todo = db.query(models.TodoModel).filter(
        models.TodoModel.id == todo_id,
        models.TodoModel.owner_id == user_id
    ).first()
    if db_todo:
        db_todo.title = updated_todo.title
        db_todo.completed = updated_todo.completed
        db.commit()
        db.refresh(db_todo)
        return db_todo
    return None


def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(models.TodoModel).filter(
        models.TodoModel.id == todo_id,
        models.TodoModel.owner_id == user_id
    ).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False


def get_user_by_username(db: Session, username: str):
    return db.query(models.UserModel).filter(models.UserModel.username == username).first()


def create_user(db: Session, username: str, hashed_password: str):
    db_user = models.UserModel(
        username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
