# in main importam FastAPI, definim lifespan, cream app si includem routers, atat
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .db import engine, Base
from .routers import notes, ai, auth

import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    
    # deoarece am trecut pe alembic nu mai am nevoie de aceasta
    # Base.metadata.create_all(bind=engine)
    
    # shutdown
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(notes.router)
app.include_router(ai.router)
app.include_router(auth.router)

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )

# $env:DB_HOST="localhost"
# $env:DB_PORT="5432"
# $env:DB_USER="notes_user"
# $env:DB_PASSWORD="notes_password"
# $env:DB_NAME="notes_db"