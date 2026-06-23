```
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install flask flask_cors gunicorn
EXPOSE 5000
CMD [ "gunicorn", "-b", ":5000", "app:app" ]
```