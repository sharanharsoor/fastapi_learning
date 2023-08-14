from schemas import UserBase, UserDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from typing import List

router = APIRouter(
  prefix='/user',
  tags=['user']
)

# Create user
'''
Steps involved in creating the user in DB:
1. Import required libraries: sqlalchemy, passlib, bcrypt
2. Create database definition and run it in main.py
3. Create database models (tables)
4. Create functionality to write to database
5. Create schemas
    1. Data from user: UserBase
    2. Response to user: UserDisplay
6. Create API operation
'''

@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
  return db_user.create_user(db, request)

# Read all users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
  return db_user.get_all_users(db)

# Read one user
@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
  return db_user.get_user(db, id)

# Update user
@router.post('/{id}/update')
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
  return db_user.update_user(db, id, request)

# Delete user
@router.get('/delete/{id}')
def delete(id: int, db: Session = Depends(get_db)):
  return db_user.delete_user(db, id)