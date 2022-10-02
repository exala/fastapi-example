from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from fastapi.params import Body
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine) # NO NEED FOR THIS LINE SINCE ALEMBIC IS TAKING CARE OF EVERYTHING NOW, WE CAN DELETE IT IF WE WANT

app = FastAPI()

origins = ['*']
#fetch('http://localhost:8000').then(res=>res.json()).then(console.log) -- COMMAND TO RUN ON CONSOLE OF INSPECT
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router, prefix='/posts', tags=['Posts'])
app.include_router(user.router, prefix='/users', tags=['Users'])
app.include_router(vote.router, prefix='/votes', tags=['Votes'])
app.include_router(auth.router)

@app.get('/')
def root():
    return {"Hello" : "World"}




