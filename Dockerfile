FROM php:8.2-cli

RUN apt-get update && apt-get install -y node-typescript

RUN mkdir -p /ts
RUN mkdir -p /www/app
RUN mkdir -p /www/editor

WORKDIR /www
CMD ["php", "-S", "0.0.0.0:8000", "."]