# In main we import FastAPI, define lifespan, create app and include routers
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import notes, ai, auth

import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
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
