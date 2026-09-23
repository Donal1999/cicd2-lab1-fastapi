from fastapi import FastAPI, HTTPException, status
from app.schemas import UserCreate


app = FastAPI(title="Lab1 - FastAPI User Api")
#array used as database 
users: list[UserCreate] = []
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello():
    return {"message": "Hello world"}

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(new_user: UserCreate):
    for existing_user in users:
        if existing_user.userid == new_user.userid:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User id already exists")

    users.append(new_user)
    return new_user

@app.get("/api/users")
def get_users():
    return users

@app.get("/api/users/{userid}")
def get_user(userid: int):
        for existing_user in users:
            if existing_user.userid == userid:
                return existing_user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
         )
