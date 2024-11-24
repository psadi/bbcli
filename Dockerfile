############################################################################
# Bitbucket CLI (bb): Work seamlessly with Bitbucket from the command line
#
# Copyright (C) 2022  P S, Adithya (psadi) (ps.adithya@icloud.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

FROM python:3.14.0a1-alpine

COPY dist/bb-*.tar.gz bb.tar.gz

RUN apk update && apk upgrade && apk add git && \
    git config --global --add safe.directory /app && \
    python3 -m pip --no-cache-dir install --upgrade pip && \
    python3 -m pip --no-cache-dir install bb.tar.gz && \
    pip3 cache purge && \
    apk cache clean && \
    rm -rf /var/cache/apk/* /tmp/* /root/.cache/pip/* bb.tar.gz

WORKDIR /app

ENTRYPOINT [ "bb" ]
