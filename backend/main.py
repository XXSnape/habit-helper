from fastapi import FastAPI

import uvicorn

from routers import router


def main() -> None:
    """
    Запускает приложение
    """

    app = FastAPI()
    app.include_router(router, prefix="/api")
    uvicorn.run("main:app", host="0.0.0.0", reload=True)


if __name__ == "__main__":
    main()
