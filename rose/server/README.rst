=======================
ROSE Engine Game Server
=======================

Overview
========
This server provides a simple HTTP endpoint for a driving game.

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

   python main.py --port 8080

By default, the server will start on port 8080.

Podman Usage
============
1. Build the Podman image:

   .. code-block:: bash

      podman build -t rose-engine .

2. Run the container:

   .. code-block:: bash

      podman run -it --rm --network host rose-engine

Kubernetes Deployment
=====================

You can deploy the application on a Kubernetes cluster using the provided configuration. 

Instructions:
-------------
1. Apply both the Deployment and Service:

.. code-block:: bash

   kubectl apply -f rose-engine.yaml

2. Check the status of the deployment:

.. code-block:: bash

   kubectl get deployments rose-engine

3. Forward a local port to your pod for accessing the service locally:

.. code-block:: bash

   kubectl port-forward deployment/rose-engine-deployment 8880:8880

Now, the service will be accessible locally at http://localhost:8880.

Note: For production deployments, consider exposing the service using an Ingress controller or cloud provider specific solutions.

Contributing
============
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License
=======
GPL-v2
