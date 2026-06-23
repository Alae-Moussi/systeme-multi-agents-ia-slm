```
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install flask flask_cors gunicorn

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```