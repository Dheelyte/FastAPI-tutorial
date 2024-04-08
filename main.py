from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from database import engine 
from database import Base

from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import models
import schema
from fastapi import APIRouter
from database import get_db

app = FastAPI()

# Create a session factory using the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


models.Base.metadata.create_all(bind=engine)


@app.get('/posts', response_model=List[schema.CreatePost])
def test_posts(db: Session = Depends(get_db)):

    post = db.query(models.Post).all()


    return  post

@app.post('/posts/create', status_code=status.HTTP_201_CREATED, response_model=List[schema.CreatePost])
def test_posts_sent(post_post:schema.CreatePost, db:Session = Depends(get_db)):

    new_post = models.Post(**post_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return [new_post]


@app.get('/posts/{id}', response_model=schema.CreatePost, status_code=status.HTTP_200_OK)
def get_test_one_post(id:int ,db:Session = Depends(get_db)):

    idv_post = db.query(models.Post).filter(models.Post.id == id).first()

    if idv_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return idv_post

@app.delete('/posts/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_test_post(id:int, db:Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)


    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id} you requested for does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()



@app.put('/posts/update/{id}', response_model=schema.CreatePost)
def update_test_post(update_post:schema.PostBase, id:int, db:Session = Depends(get_db)):

    updated_post =  db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    updated_post.update(update_post.dict(), synchronize_session=False)
    db.commit()


    return  updated_post.first()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/users/{user_id}")
# async def get_user(user_id: int):
#     # Create a new session
#     db = SessionLocal()
#     # Retrieve the user from the database using the user_id
#     user = db.query(User).filter(User.id == user_id).first()
#     # Close the session
#     db.close()
#     return {"user": user}