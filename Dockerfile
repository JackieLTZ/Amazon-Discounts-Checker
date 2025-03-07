FROM python:3.12-alpine
LABEL mainteiner=Jackie

WORKDIR /app

RUN apk update && apk add --no-cache gcc musl-dev libffi-dev postgresql-dev

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]