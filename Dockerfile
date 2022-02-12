FROM python:3.8-slim-buster
USER root

RUN apt-get update &&\
    apt-get install\
    gcc\
    musl-dev\
    nano\
    nginx\
    python3-dev\
    python3-pip\
    systemd\
    unzip\
    zip\
    -y \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ADD nginx_host /etc/nginx/sites-enabled/default
ADD entrypoint.sh /entrypoint.sh

RUN wget https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && python3 -m pip install -U pip \
    && python3 -m pip install -r /app/requirements.txt \
	&& rm get-pip.py

COPY ./app /app
WORKDIR /app

EXPOSE 80
RUN chmod +x entrypoint.sh
CMD  ["/entrypoint.sh"]
