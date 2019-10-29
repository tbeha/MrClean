# User Ubuntu as the base Image
FROM tb1378/svtpython
#
LABEL maintainer="Thomas Beha"
LABEL version="2.1"
LABEL copyright="Thomas Beha, 2019"
LABEL license="GNU General Public License v3"
LABEL DESCRIPTION="CTC SimpliVity Demo Clean Up Engine"
#
#RUN mkdir /opt/python/data
COPY ./mrclean.py /opt/python/
COPY ./mrclean.xml /opt/python/
COPY ./mrclean.key /opt/python/
COPY ./BBNRefPolicies.json /opt/python/
RUN echo "0 22 * * * root /usr/bin/python3 /opt/python/mrclean.py" >> /etc/crontab
#RUN service cron restart
CMD [ "cron", "-f" ]
