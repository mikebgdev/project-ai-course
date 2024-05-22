FROM python:3.11.5

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 3000 8000

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
