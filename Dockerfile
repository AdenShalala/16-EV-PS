FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app//requirements.txt

COPY ./src /app/src

EXPOSE 8080

CMD ["python","./src/main.py"]