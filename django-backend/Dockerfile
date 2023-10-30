FROM python:3.10-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./src ./src
# Выполняем makemigrations перед запуском Gunicorn
RUN python ./src/manage.py makemigrations
# Затем выполняем migrate для применения миграций
RUN python ./src/manage.py migrate
CMD gunicorn -w 3 --chdir ./src proj.wsgi --bind 0.0.0.0:8000
