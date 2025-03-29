FROM tiangolo/uvicorn-gunicorn:python3.10 AS carlemany-backend-base

RUN pip install --upgrade pip

COPY requirements/base.txt /tmp/requirements/

RUN pip install -r /tmp/requirements/base.txt

RUN mkdir /backend-backend

WORKDIR /carlemany-backend

COPY . ./


FROM carlemany-backend-base AS carlemany-backend-dev

COPY requirements/dev.txt /tmp/requirements/

RUN pip install -r /tmp/requirements/dev.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "info", "--lifespan", "on"]


FROM carlemany-backend-base AS carlemany-backend-prod

COPY requirements/prod.txt /tmp/requirements/

RUN pip install -r /tmp/requirements/prod.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "error", "--lifespan", "on"]
