import uvicorn
from fastapi import FastAPI

from routers import router

app = FastAPI()

app.include_router(router)


def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
