# Customer-Ordering-System Api

A simple customer ordering system api built using Django rest framework. 

  
## Features

  ### 1. Authentication and authorization
  - Account Creation: Users create an account by providing necessary information such as username, email, and password.
  - User Login: Upon successful login, a token is generated. This token is set as a cookie in the user's browser and can also be passed in the 
    header of subsequent requests to authorize the user.
  - User Logout: When a user chooses to log out, the authorization token is revoked. This ensures that the user is no longer authenticated 
    and cannot access protected resources.

  ### 2. Products and categories 
  - System admins add products and categories to the system
  - customers/buyers can view all available products.

  ### 3. Order management 
  - Order Creation:
      1. Users can create orders and add products to them.
      2. When adding products to an order, users specify the quantity they wish to purchase.

  - Stock Verification:
      1. The system ensures that the order quantity does not exceed the available stock for each product.
      2. If the requested quantity exceeds the available stock, the user is notified and prevents the order from being placed.

  - Order Total Cost Calculation:
      1. Upon completing the order, users receive the total cost of their orders.
      2. The total cost includes the prices of all products in the order, considering the quantities specified.

  - Order Items Details:
      1. Users can view the details of each order, including the items contained within it.
      2. For each item in an order, users can see the product details and the quantity ordered.

  - Order Filtering:
      1. Users can filter orders based on their status (e.g., pending, processing, completed).
      2. This filtering functionality allows users to easily track the status of their orders and manage them efficiently.

  - Checkout 
      1. Users can checkout a pending order, after which the system sends an SMS to the user containing the order number for easier tracking
        and total cost of the order, and subsequently sets the order status to "placed".

## Technologies Used
1. Django Rest Framework
2. PostgreSQL
4. Docker and Docker compose 
5. Nginx and Gunicorn
6. Google Cloud Platform , Google Kubernetes Engine
7. Kubernetes
8. Drf spectacular, Swagger UI, and Rapidoc
9. CI/CD - Jenkins

## Running the app Locally 
Clone this repository to your machine

``` 
https://github.com/Kihara-Njoroge/Order-Management-System-API.git
```

Rename the ```.env.example``` and ```.env.db.example``` file found in the project's root directory to ```.env``` & ```.env.db``` and update the variables.

Ensure you have Docker, docker-compose, Minikube, kubectl, Jenkins installed.

## Build and Run:

```
docker compose build
docker compose up
```

 - Navigate to [http://localhost/api/v1/docs]  to view the API endpoints documentation.

#### Preview of the documentation UI
```
```


## Set Up Minikube Kubernetes Cluster
 - Provisioning a Minikube cluster for local development.

    ### Start Minikube cluster
    ```
    minikube start
    ```

    ### Set kubectl context to Minikube

    ```
    kubectl config use-context minikube
    ```

    ### Deploy the App on Minikube Kubernetes
    You can use the already defined Kubernetes YAML files for deployment, service, and ingress or define your own.

    ### Apply Kubernetes configurations
    ```
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    kubectl apply -f ingress.yaml
    ```

## Implement Jenkins CI/CD Pipeline
  - Set up Jenkins and configure a CI/CD pipeline to automate Docker builds and Kubernetes deployments. The jenkins pipeline builds 
    and pushes the builds to docker hub then deploys to github. 
  - Use GitHub webhooks to trigger Jenkins build jobs:
        1. In your GitHub repository settings, navigate to Webhooks.
        2. Add a new webhook and specify the payload URL of your Jenkins server, along with the appropriate endpoint (e.g., /github-webhook/).
        3. Select the events that should trigger the webhook (e.g., push events, pull request events).

    ### CI/CD Pipeline Workflow:
      Checkout: Checkout source code from GitHub
      Build and Push Docker Image: Build the Docker image from the Django application code, Push Docker image to Docker Hub
      Run Tests: Validate the application's functionality.
      Deploy to Minikube: Deploy the Django application to the Minikube Kubernetes cluster.


## Monitoring and Logging Setup (optional)

  - Minikube Monitoring and Logging Setup

  ## Overview

  Guide for setting up monitoring and centralized logging in a Minikube environment. The setup includes the following components:

  - **Monitoring:** Utilizing Prometheus for metric collection and Grafana for visualization.
  - **Logging:** Implementing centralized logging with Elasticsearch for log storage and Kibana for log visualization.


  ## Monitoring Setup

  ### Step 1: Start Minikube

  ```
  minikube start
  ```
  ### Step 2: Add Helm Repositories
  ```
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo add grafana https://grafana.github.io/helm-charts
   helm repo update
  ```
  ### Step 3: Install Prometheus and Grafana

  ```
  helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
  helm install grafana grafana/grafana -n monitoring

  ```

  ### Step 4: Port-forward

  ```
  kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n default 9090
  kubectl port-forward -n monitoring svc/grafana 3000:80
  ```
  -  Access Grafana at [http://localhost:9090]

  -  Access Grafana at [http://localhost:3000] (credentials: admin/admin).


  ## Logging Setup

  ### Step 1: Install Elasticsearch Operator

  ```
  helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace
  ```

  ### Step 2: Install Elasticsearch
  
  - Create elasticsearch.yaml:

    ```
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: quickstart
    spec:
      version: 7.15.2
      nodeSets:
      - name: default
        count: 1
        config:
          node.master: true
          node.data: true
          node.ingest: true
          node.store.allow_mmap: false
    ```
  -Apply the custom resource:
    
    ```
    kubectl apply -f elasticsearch.yaml
    ```
  ### Step 3: Install Kibana

  - Create kibana.yaml:
    ```
    apiVersion: kibana.k8s.elastic.co/v1
    kind: Kibana
    metadata:
      name: quickstart
    spec:
      version: 7.15.2
      count: 1
      elasticsearchRef:
        name: quickstart
        
    ```
  - Apply the custom resource:

    ```
    kubectl apply -f kibana.yaml

    ```
  - Step 4: Port-forward Kibana

  ```
  kubectl port-forward -n elastic-system svc/kibana-quickstart-kb-http 5601:5601
  ```
  - Access Kibana at [http://localhost:5601].

### Clean up

```
minikube stop
minikube delete
```







  