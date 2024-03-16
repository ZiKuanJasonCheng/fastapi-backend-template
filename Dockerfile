FROM my-base-image:latest
ENV PORT 8886
COPY ./prestart.sh /app
COPY ./app /app/app
COPY ./gunicorn_conf.py /gunicorn_conf.py