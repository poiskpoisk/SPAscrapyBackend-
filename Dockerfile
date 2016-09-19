FROM ubuntu:latest
RUN apt-get update && apt-get install --yes \
     python3-pip \
     python3 \
     git

RUN pip3 install --upgrade pip
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN pip3 install django
RUN pip3 install djangorestframework
RUN pip3 install django-cors-middleware 
RUN pip3 install lxml
RUN git clone https://github.com/poiskpoisk/testjob2backend
ENV DJANGO_SETTINGS_MODULE testjob2.settings
EXPOSE 8000
EXPOSE 80
EXPOSE 443
WORKDIR testjob2backend
CMD python3 manage.py runserver 0.0.0.0:8000