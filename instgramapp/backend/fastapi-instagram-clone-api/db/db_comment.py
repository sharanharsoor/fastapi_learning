from datetime import datetime
from sqlalchemy.orm import Session
from db.models import DbComment
from db.models import DbUser
from db.models import DbPost
from routers.schemas import CommentBase
from fastapi import HTTPException, status
from pprint import pprint

def create(db: Session, request: CommentBase):
    comment = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'username {request.username} not found')
    if comment.username != request.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='not valid user')

    #pprint(vars(comment))
    post = db.query(DbPost).filter(DbPost.id == request.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'post {request.post_id} not found')

    new_comment = DbComment(
    text = request.text,
    username = request.username,
    post_id = request.post_id,
    timestamp = datetime.now()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all(db: Session, post_id: int):
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()