from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import engine, get_db
from app.models import Base, UserDB
from app.schemas import UserCreate, UserRead

Base.metadata.create_all(bind=engine)



app = FastAPI(title="Lab3 - FastAPI SQLAlchemy User Api")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello():
    return {"message": "Hello world"}

@app.post("/api/users", 
          response_model=UserRead, 
          status_code=status.HTTP_201_CREATED,
)
def add_user(new_user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(**new_user.model_dump())
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="A user with this email or student_id already exists",
        )
    return db_user

@app.get("/api/users", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    statement = select(UserDB).order_by(UserDB.id)
    return db.execute(statement).scalars().all()

@app.get("/api/users/{userid}", response_model=UserRead)
def get_user(userid: int, db: Session = Depends(get_db)):
    db_user = db.get(UserDB, userid)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
         )
    return db_user

@app.delete("/api/users/{userid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(userid: int, db: Session = Depends(get_db)):
    db_user = db.get(UserDB, userid)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
         )  
    db.delete(db_user)
    db.commit()
    return
                

  

