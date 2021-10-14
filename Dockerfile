FROM python:3-alpine

WORKDIR /code
COPY src/ .

CMD [ "python", "./server.py" ]