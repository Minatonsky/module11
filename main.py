import uvicorn
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi import FastAPI
from src.routes import contacts, auth, users
from src.conf.config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')


origins = [
    "http://localhost:8000"
    ]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, reload=True)