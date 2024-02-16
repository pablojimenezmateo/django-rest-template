FROM python:3.10-bullseye

# The "proper" version of psycopg2 needs libpq-dev and gcc
RUN apt-get update
RUN apt-get -y install libpq-dev gcc postgresql-client gettext

# The context is specified in the docker-compose file
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Get the environment variables from the docker-compose
ARG HOST_UID
ARG HOST_GID
ARG CONTAINER_USER

# Create a user/group with the same UID/GID as the host user
# This is to avoid permission issues with mounted volumes
RUN groupadd -g $HOST_GID $CONTAINER_USER
RUN useradd -m -u $HOST_UID -g $HOST_GID -o -s /bin/bash $CONTAINER_USER

USER $CONTAINER_USER

# Entrypoint bash script
COPY ./app/entrypoint.sh /tmp/entrypoint.sh

CMD ["/bin/bash", "/tmp/entrypoint.sh"]
