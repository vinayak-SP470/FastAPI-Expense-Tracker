from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register/")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Username already taken",
                "success": False,
                "statuscode": 400,
                "message": "Registration failed. Please choose a different username."
            }
        )

    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(
        status_code=201,
        content={
            "user_name": new_user.username,
            "success": True,
            "statuscode": 201,
            "message": "User registered successfully."
        }
    )


@router.post("/token/")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = auth.authenticate_user(db, user.username, user.password)
    if not db_user:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid username or password",
                "success": False,
                "statuscode": 400,
                "message": "Login failed. Please check your username and password and try again."
            }
        )

    access_token = auth.create_access_token(
        data={"sub": db_user.username}, 
        expires_delta=timedelta(minutes=30)
    )

    refresh_token = auth.create_refresh_token(
        data={"sub": db_user.username}, 
        expires_delta=timedelta(days=7)
    )

    return {
        "data": {
            "access_token": access_token, 
            "refresh_token": refresh_token
        },
        "success": True,
        "statuscode": 200,
        "message": "Login successful."
    }

@router.post("/refresh/")
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    username = auth.verify_refresh_token(refresh_token)
    if not username:
        return JSONResponse(
            status_code=401,
            content={
                "error": "Invalid refresh token",
                "success": False,
                "statuscode": 401,
                "message": "Token verification failed. Please log in again."
            }
        )
    new_access_token = auth.create_access_token(
        data={"sub": username}, 
        expires_delta=timedelta(minutes=30)
    )

    return {
        "data": {
            "access_token": new_access_token,
        },
        "success": True,
        "statuscode": 200,
        "message": "New access token generated successfully."
    }

