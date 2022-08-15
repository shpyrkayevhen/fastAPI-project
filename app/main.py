from ctypes import util
from enum import auto
from turtle import pos, title, update
from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

from .database import engine, get_db
from . import models, schemas, utils
from sqlalchemy.orm import Session


from .routers import post, user, auth


# CREATING TABLE/S IN DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# CONNECT TO DATABASE
# try:
#    conn = psycopg2.connect(
#        host='localhost',
#        dbname='fastapi',
#        user='postgres',
#        password='yevhen199610')

#    cursor = conn.cursor(cursor_factory=RealDictCursor)
#    print("Connection to database was successfully")

# except Exception as error:
#    print(print(f'Failed to connect to database. Error type: {error}'))


@app.get('/')
async def root():
    pass
