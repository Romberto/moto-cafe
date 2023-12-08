FROM python:3.10-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./src ./src
CMD gunicorn proj:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:443 --keyfile=/etc/letsencrypt/live/1566825-cw73062.twc1.net/privkey.pem --certfile=/etc/letsencrypt/live/1566825-cw73062.twc1.net/fullchain.pem
