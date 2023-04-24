# Generate a container that generates requirements.txt
ARG PY_VERSION=3.9
FROM python:${PY_VERSION} as source

ARG DEV

ENV ENABLE_PIPENV=true

# Install pipenv
RUN pip install --upgrade pipenv

COPY Pipfile ./Pipfile

# Generate requirements.txt file from Pipfile
RUN if [ -z ${DEV} ]; \
    then \
        pipenv lock > requirements.txt; \
    else \
        pipenv lock --dev > requirements.txt; \
    fi

# Generate work image
FROM registry.access.redhat.com/ubi9/python-39

# Project maintainer
LABEL maintainer="frolland@redhat.com"

# Copy pipfile to default WORKDIR
COPY --from=source requirements.txt ./requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy application to default WORKDIR
COPY . ./

# Server port
EXPOSE 8880

# Server command
CMD [ "run", "python", "rose-server"]
