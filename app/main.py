from fastapi import FastAPI

from app.routers import wakeparks

app = FastAPI(title=__name__)
app.include_router(wakeparks.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
