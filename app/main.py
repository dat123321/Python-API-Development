from fastapi import FastAPI
from app import models
from app.routers import user, auth, produce
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user.routers)
app.include_router(auth.routers)
app.include_router(produce.routers)


@app.get("/")
async def root():
    return {"hello": "world"}


