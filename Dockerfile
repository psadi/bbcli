FROM python:alpine3.16

COPY dist/bb-*.tar.gz bb.tar.gz

RUN python3 -m pip --no-cache-dir install bb.tar.gz;

ENTRYPOINT [ "bb" ]