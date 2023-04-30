from app import models, oauth2, schemas, utils
from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db

routers = APIRouter(
    prefix="/post"
)


@routers.get("/", response_model=List[schemas.User_out])
async def fetch_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).all()
    return user


@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User_out)
def register_user(user: schemas.User, db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user)):
    hashed_pass = utils.Hash(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@routers.get("/{id}")
async def get_post(id, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_byID = db.query(models.User).filter(models.User.id == id).first()
    if not post_byID:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found ")
    return post_byID


@routers.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    delete_Post = db.query(models.User).filter(models.User.id == id)
    if delete_Post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    delete_Post.delete(synchronize_session=False)
    db.commit()


@routers.put("/{id}", response_model=schemas.User)
async def update_Post(id: int, updated_post: schemas.User, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.User).filter(models.User.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found ")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
