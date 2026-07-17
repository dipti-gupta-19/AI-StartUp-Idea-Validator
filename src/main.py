from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI
from .routers import authentication,ideas


from . import model
from .database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    model.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
def base():
    return {"greet":"hello"}

app.include_router(authentication.router)
app.include_router(ideas.router)