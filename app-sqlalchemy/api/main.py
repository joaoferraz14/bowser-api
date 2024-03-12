from ..orm import models
from ..adapters.database_connection import engine
from fastapi import FastAPI
from ..routers import post, user, status, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(status.router)
app.include_router(user.router)
app.include_router(auth.router)
