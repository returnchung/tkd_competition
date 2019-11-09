FROM python:3.7.5-alpine3.10
WORKDIR /home/app
COPY index.py           .
COPY entrypoint.sh             .
RUN chmod +x entrypoint.sh
COPY requirements.txt   .
RUN mkdir -p app
COPY app                app
RUN mkdir -p secrets
RUN pip install -U pip \
    && pip install -r requirements.txt

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
ENTRYPOINT ["/home/app/entrypoint.sh"]
