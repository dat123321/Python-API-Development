from app import models, oauth2, schemas
from fastapi import HTTPException, Response, status, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db

routers = APIRouter(
    prefix="/produce"
)


@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Produce_out)
def register_user(produce: schemas.Produce, db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    new_user = models.Produce(owner_id=current_user.id, **produce.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@routers.get("/", response_model=List[schemas.Produce_out])
async def fetch_produce(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    produce = db.query(models.Produce).all()
    return produce


@routers.get("/{id}", response_model=schemas.Produce_out)
async def get_produce(id, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    produce_byID = db.query(models.Produce).filter(models.Produce.id == id).first()
    if not produce_byID:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found ")
    return produce_byID


@routers.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    delete_query = db.query(models.Produce).filter(models.Produce.id == id)
    delete_produce = delete_query.first()
    if delete_produce is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if delete_produce.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform requested action")

    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
