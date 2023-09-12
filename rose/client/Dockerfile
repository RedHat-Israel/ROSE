# quay.io/rose/rose-common
# Use Red Hat Universal Base Image (UBI) with Python
# with:
#   /app/rose/common package
#   PYTHONPATH "${PYTHONPATH}:/app"
FROM quay.io/rose/rose-common

# Set the working directory in the Docker container
WORKDIR /app/rose/client

# Copy the local package files to the container's workspace
COPY . /app/rose/client

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the main.py file when the container launches
ENTRYPOINT ["python", "main.py", "--listen", "0.0.0.0"]
CMD ["--driver", "./mydriver.py", "--port", "8081"]
