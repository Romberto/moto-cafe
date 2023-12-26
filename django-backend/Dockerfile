FROM python:3.10-alpine
WORKDIR /src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./src /src
CMD gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 proj.asgi:application
