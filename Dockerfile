FROM python:3.7

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN pip install poetry

WORKDIR /apyr
COPY poetry.lock pyproject.toml /apyr/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /apyr

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "apyr.main:app"]

