from fastapi import FastAPI

from app.routers import wakeparks
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(title=__name__)
origins = [
    "http://localhost:8080",
]

app.include_router(wakeparks.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
