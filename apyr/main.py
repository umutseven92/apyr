import argparse

import uvicorn
from fastapi import FastAPI

from apyr.routers.endpoints import endpoint_router

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="Port", default=8000, type=int)
args = parser.parse_args()

app = FastAPI()

app.include_router(endpoint_router)


def run():
    uvicorn.run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    run()
