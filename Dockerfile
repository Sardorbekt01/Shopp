FROM --platform=linux/amd64 python:3.9  as builder

WORKDIR /app

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

WORKDIR /app

EXPOSE 8000

CMD python manage.py collectstatic --noinput && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    uvicorn teaching_blog.asgi:application --host 0.0.0.0 --port 8000