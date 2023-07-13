FROM python:3.11.4-alpine

COPY dist/bb-*.tar.gz bb.tar.gz

RUN apk update && apk upgrade && apk add git && \
    git config --global --add safe.directory /app && \
    python3 -m pip --no-cache-dir install bb.tar.gz && \
    pip3 cache purge && \
    apk cache clean && \
    rm -rf /var/cache/apk/* /tmp/* /root/.cache/pip/*

WORKDIR /app

ENTRYPOINT [ "bb" ]
