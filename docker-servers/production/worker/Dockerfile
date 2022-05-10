FROM python:3.8

WORKDIR /home
RUN pip download Jam-Sesh-Worker
COPY .env .
RUN tar xvzf Jam-Sesh-Worker-2.0.0.tar.gz
RUN mv -v /home/Jam-Sesh-Worker-2.0.0/* /home
RUN pip install -r requirements.txt
#CMD tail -f /dev/null
ENTRYPOINT celery -A tasks worker --loglevel=info
