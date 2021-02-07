import uvicorn
from fastapi import FastAPI

from apyr.routers.endpoints import endpoint_router

app = FastAPI()

app.include_router(endpoint_router)


def run():
    """Mock that API!"""

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
