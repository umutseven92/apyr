import argparse

import uvicorn
from fastapi import FastAPI

from apyr.routers.apyr_endpoints import apyr_router
from apyr.routers.endpoints import endpoint_router

app = FastAPI()

app.include_router(apyr_router)
app.include_router(endpoint_router)


def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
