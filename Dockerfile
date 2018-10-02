# Use official CentOS Python 2.7 image
# https://developer.fedoraproject.org/tools/docker/docker-images.html
FROM centos/python-27-centos7 AS base

# Project maintainer
LABEL maintainer="frolland@redhat.com"

# Required env vars
ENV LD_LIBRARY_PATH="/opt/rh/python27/root/usr/lib64/" \
    ENABLE_PIPENV=true

# Install pipenv
RUN pip install --upgrade pipenv

# Copy application to default WORKDIR
COPY . ./

# Install dependencies from pipfile
RUN pipenv install

# Server port
EXPOSE 8880

# Server command
ENTRYPOINT [ "pipenv" ]
CMD [ "run", "python", "rose-server"]
