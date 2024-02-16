FROM nginx:1.23.3
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d

# # Get the environment variables from the docker-compose
# ARG HOST_UID
# ARG HOST_GID
# ARG CONTAINER_USER

# # Create a user/group with the same UID/GID as the host user
# # This is to avoid permission issues with mounted volumes
# RUN groupadd -g $HOST_GID $CONTAINER_USER
# RUN useradd -m -u $HOST_UID -g $HOST_GID -o -s /bin/bash $CONTAINER_USER

# RUN usermod -u $HOST_UID -o nginx && groupmod -g $HOST_GID -o nginx

# USER $CONTAINER_USER