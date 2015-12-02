FROM centos:latest

MAINTAINER David Vogel dvogel26@yahoo.com

RUN mkdir /opt/dvogel26
ADD data_generator.py /opt/dvogel26/

CMD [ "python", "-u", "/opt/dvogel26/data_generator.py" ]
