from fastapi import status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, auth2
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db

router = APIRouter(
    prefix='/api/posts',          # router.get('api/posts/..')
    tags=['Posts']                # representation in http://127.0.0.1:8000/docs
)


@router.get('/', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    posts = db.query(models.Post).all()
    return posts

    # cursor.execute('SELECT * FROM posts;')
    # posts = cursor.fetchall()
    # print(posts)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    new_post = models.Post(**post.dict())  # CONVERT INTO DICTIONARY AND UNPUCK
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    # ALWAYS WHEN WE ADD/EDIT SOME DATA
    db.add(new_post)
    db.commit()
    # THE SAME AS IN SQL -> RETURNING *;
    db.refresh(new_post)

    return new_post

    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
    #                                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()


@router.get('/{id}', response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')
    return post

    # cursor.execute("""SELECT * FROM posts WHERE id=%s;""", (id, ))
    # post = cursor.fetchone()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, )
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)

    print(post)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *;""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()


@router.put('/{id}', response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *;""",
    #                (post.title, post.content, post.published, id))

    # updated_post = cursor.fetchone()
    # conn.commit()
