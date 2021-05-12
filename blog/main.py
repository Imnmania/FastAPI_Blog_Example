from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user


#========================= Initialize fastapi ==========================#
app = FastAPI()


#===================== CHECK EXISTING/ CREATE TABLES ===================#
models.Base.metadata.create_all(engine)


#========================== DEFINE ROUTES ===============================#
app.include_router(blog.router)
app.include_router(user.router)

