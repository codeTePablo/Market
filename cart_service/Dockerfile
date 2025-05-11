FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

ENV FLASK_APP=cart_service.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]

