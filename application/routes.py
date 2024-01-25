from datetime import timedelta
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import desc
from sqlalchemy.orm import Session

from application import auth, models, schemas, security
from application.database import get_db

router = APIRouter()


@router.post("/register/", response_model=schemas.UserInDBBase)
async def register(user_in: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, username=user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(**user_in.dict(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = auth.get_user(db, username=form_data.username)
    if not user or not security.pwd_context.verify(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = (timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




@router.post("/create-todo/", response_model=schemas.Todo)
async def create_todo(todo_create: schemas.TodoCreate, current_user: schemas.UserInDB = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    todo = models.Todo(**todo_create.model_dump(), user_id=current_user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo



@router.get("/get-todo/{todo_id}", response_model=schemas.Todo)
async def read_todo(todo_id: int, db: Session = Depends(get_db), current_user: schemas.UserInDB = Depends(auth.get_current_user)):
    user_id=current_user.id

    todo = db.query(models.Todo).filter(models.Todo.id == todo_id and models.Todo.user_id==user_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo



@router.get("/get-all-todos/", response_model=list[schemas.Todo])
async def read_all_todos(current_user: schemas.UserInDB = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).order_by(models.Todo.due_date,desc(models.Todo.due_date.is_(None))).all()

    return todos



@router.put("/update-todo/{todo_id}", response_model=schemas.Todo)
async def update_todo(
    todo_id: int,
    todo_update: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserInDB = Depends(auth.get_current_user)
):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update only the fields provided in todo_update
    for key, value in todo_update.dict().items():
        setattr(db_todo, key, value)

    db_todo.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_todo)
    return db_todo



# @router.put("/update-todo/{todo_id}", response_model=schemas.Todo)
# async def update_todo(todo_id: int, todo_update: schemas.TodoCreate, db: Session = Depends(get_db),current_user: schemas.UserInDB = Depends(auth.get_current_user)):
#     db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     if db_todo is None:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     for key, value in todo_update.dict().items():
#         setattr(db_todo, key, value)
#     db.commit()
#     db.refresh(db_todo)
#     return db_todo




@router.delete("/delete-todo/{todo_id}", response_model=schemas.Todo )
async def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: schemas.UserInDB = Depends(auth.get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return todo
