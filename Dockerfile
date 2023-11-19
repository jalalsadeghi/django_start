FROM jalalsadeghi/docker_base:0.2.1

COPY ./requirements /requirements
COPY ./scripts /scripts
COPY ./src /src

WORKDIR src

EXPOSE 8000

RUN /py/bin/pip install -r /requirements/development.txt

RUN chmod -R +x /scripts && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    adduser --disabled-password --no-create-home backend && \
    chown -R backend:backend /vol &&\
    chmod -R 755 /vol

ENV PATH="/scripts:/py/bin:$PATH"

USER backend

CMD ["run.sh"]
