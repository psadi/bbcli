FROM python:alpine3.18

COPY dist/bb-*.tar.gz bb.tar.gz

RUN apk add git; \
    git config --global --add safe.directory /app; \
    python3 -m pip --no-cache-dir install bb.tar.gz;

WORKDIR /app

ENTRYPOINT [ "bb" ]
