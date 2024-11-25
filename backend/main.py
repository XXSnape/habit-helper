from fastapi import FastAPI

import uvicorn

from routers import router

app = FastAPI()
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
