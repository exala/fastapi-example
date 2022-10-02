from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter()

#@router.get('/', response_model = List[schemas.Post])
@router.get('/', response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 20, skip: int = 0, search: Optional[str] = ''):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #posts_query = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    #posts = posts_query.all()
    #NOW WE HAVE POSTS WITH VOTES
    posts_query = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(models.Vote, models.Post.id == models.Vote.post_id,
                                                                                             isouter=True).group_by(models.Post.id)\
                                                                            .filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    posts = posts_query.all()
    return posts

@router.post('/', status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""",
                    #(post.title, post.content))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(owner_id = current_user.id, **post.dict()) #this **.post.dict() actually the dictionary items of post and is easier
    db.add(new_post)
    db.commit() #Same as RETURNING in SQL
    db.refresh(new_post) #Same as RETURNING in SQL
    return new_post

@router.get('/{id}', response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    #NOW WE HAVE SINGLE POST WITH VOTES
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label('Votes')).join(models.Vote,
                                                                                             models.Post.id == models.Vote.post_id,
                                                                                             isouter=True).group_by(models.Post.id)\
                                                                                            .filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return post

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} does not exist")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    #No need for refresh or RETURNING here as it is deleting
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #               (post.title, post.content, post.published, id,))
    #updated_post = cursor.fetchone()
    #conn.commit()
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post_query.first()