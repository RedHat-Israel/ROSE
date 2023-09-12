=======================
ROSE Driver Game Server
=======================

Overview
========
This server provides a simple HTTP endpoint for a driving game. The game receives JSON payloads containing information about car metadata and a game track filled with obstacles.
The server, using a driver's logic, returns the best action for the car to take next.

Requirements
============
* Python 3.8+
* Podman (optional, for containerization)

Installation
============
1. Clone the repository:

   .. code-block:: bash

      git clone <repository_url>
      cd <repository_directory>

2. Install the required Python packages:

   .. code-block:: bash

      pip install -r requirements.txt
      pip install -r requirements-dev.txt

Running the Server
==================
Run the server using:

.. code-block:: bash

   python main.py --port 8081 --driver <path to driver python file>

By default, the server will start on port 8081, default driver is ./mydriver.py .

Driver Logic
============
This server uses a default driver logic which chooses the next action randomly. For a custom driver logic, modify the `driver.py` file.

Podman Usage
============
1. Build the Podman image:

   .. code-block:: bash

      # Edit mydriver.py file.
      podman build -t rose-driver .

2. Run the container:

   .. code-block:: bash

      # Edit mydriver.py file, and create the best driver code,
      # once mydriver.py is ready build and run the container.
      podman build -t rose-driver .
      podman run -it --rm --network host rose-driver --port 8081

3. Run the container using local driver python file:

   .. code-block:: bash

      podman run -it --rm --network host -v <path to driver python file>:/mydriver.py:z rose-driver --driver /mydriver.py --port 8081

Kubernetes Deployment
=====================

You can deploy the application on a Kubernetes cluster using the provided configuration. 

Instructions:
-------------
1. Apply both the Deployment and Service:

.. code-block:: bash

   # Edit rose-driver.yaml and change the image to use your publically published image, image must be available from the registry,
   # you can't use local images when running inside a cluster, image must be pushed to a registry reachable from the cluster.
   #
   # Note: By modifying the deployment and service names, you can run more then one driver.
   kubectl apply -f rose-driver.yaml

2. Check the status of the deployment:

.. code-block:: bash

   kubectl get deployments rose-driver

3. Forward a local port to your pod for accessing the service locally:

.. code-block:: bash

   kubectl port-forward deployment/rose-driver-deployment 8081:8081

Now, the service will be accessible locally at http://localhost:8081.

Note: For production deployments, consider exposing the service using an Ingress controller or cloud provider specific solutions.

Contributing
============
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
=======
GPL-v2
