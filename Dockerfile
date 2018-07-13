FROM        python:3.7.0-slim
MAINTAINER  yeojin.dev@gmail.com

RUN         apt -y update && apt -y dist-upgrade
RUN         apt -y install build-essential
RUN         apt -y install nginx supervisor

COPY        ./requirements.txt /srv
RUN         pip install -r /srv/requirements.txt

FROM        eb-docker:base
MAINTAINER  yeojin.dev@gmail.com

ENV         BUILD_MODE              production
ENV         DJANGO_SETTINGS_MODULE  config.settings.${BUILD_MODE}
ENV         PROJECT_DIR             /srv/project

COPY        .   ${PROJECT_DIR}
WORKDIR     ${PROJECT_DIR}

RUN         cp -f ${PROJECT_DIR}/.config/${BUILD_MODE}/nginx.conf           /etc/nginx
RUN         cp -f ${PROJECT_DIR}/.config/${BUILD_MODE}/nginx_app.conf       /etc/nginx/sites-available
RUN         rm -f /etc/nginx/sites-enabled/*
RUN         ln -fs /etc/nginx/sites-available/nginx_app.conf                    /etc/nginx/sites-enabled

RUN         cp -f ${PROJECT_DIR}/.config/${BUILD_MODE}/supervisor_app.conf  /etc/supervisor/conf.d

CMD         supervisord -n