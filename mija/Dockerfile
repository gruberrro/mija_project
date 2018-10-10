# mija project
# Version: 1.0

FROM python:3.7.0-stretch
EXPOSE 8000
# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim
# Project Files and Settings
ARG PROJECT=mija_project
ARG PROJECT_DIR=/var/www/${PROJECT}
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
ADD . /mija
COPY requirements.txt .
RUN pip install -r requirements.txt

# migrations
CMD python /mija/manage.py migrate

# Server
CMD python /mija/manage.py runserver 0.0.0.0:8000