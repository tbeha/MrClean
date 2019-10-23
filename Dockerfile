# User Ubuntu as the base Image
FROM ubuntu
#
LABEL maintainer="Thomas Beha"
LABEL version="2.0"
LABEL copyright="Thomas Beha, 2019"
LABEL license="GNU General Public License v3"
LABEL DESCRIPTION="CTC SimpliVity Demo Clean Up Engine"
#
RUN apt-get update
RUN apt-get -y install python3.6 && \
	apt-get -y install python3-pip && \
	apt-get -y install vim && \
	apt-get -y install cron 
RUN /usr/bin/pip3 install requests && \
	/usr/bin/pip3 install fernet && \
	/usr/bin/pip3 install lxml
RUN mkdir /opt/mrclean && \
	mkdir /opt/mrclean/data
COPY ./mrclean.py /opt/mrclean
COPY ./SimpliVityClass.py /opt/mrclean
COPY ./vCenterClass.py /opt/mrclean
#COPY ./data/mrclean.xml /opt/mrclean/data
#COPY ./data/mrclean.key /opt/mrclean/data
#COPY ./data/BBNRefPolicies.json /opt/mrclean/data
RUN echo "0 22 * * * root /usr/bin/python3 /opt/mrclean/mrclean.py" >> /etc/crontab && \
    service cron restart
