FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY .env /app
WORKDIR /app
RUN pip download Jam-Sesh-Server
RUN tar xvzf Jam-Sesh-Server-2.0.0.tar.gz
RUN mv -v /app/Jam-Sesh-Server-2.0.0/* /app
#CMD tail -f /dev/null
RUN pip install -r /app/requirements.txt