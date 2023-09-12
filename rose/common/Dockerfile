# Use Red Hat Universal Base Image (UBI) with Python
FROM registry.access.redhat.com/ubi8/python-38

# Set the working directory in the Docker container
WORKDIR /app/rose/common

# Make app.rose a python package
COPY __init__.py /app/rose/

# Copy the local package files to rose.common
COPY __init__.py /app/rose/common/
COPY actions.py /app/rose/common/
COPY obstacles.py /app/rose/common/

# Add the rose client package to the python path
ENV PYTHONPATH "${PYTHONPATH}:/app"
