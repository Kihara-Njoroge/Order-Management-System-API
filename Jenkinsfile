pipeline {
  agent any

  environment {
    PROJECT_ID = 'savannar-test'
    CLUSTER_NAME = 'savannah-test-api'
    ZONE = 'africa-south1'
  }

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/Kihara-Njoroge/Order-Management-System-API.git'
      }
    }

    stage('Build Tag and Push Docker Image') {
      steps {
        script {
          def dockerImage = 'order-management-system-api'
          echo "Building Docker image: ${dockerImage}"

          withCredentials([usernamePassword(credentialsId: 'DockerHubCredentials', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
            sh "echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin"
            // Build the Docker image using Dockerfile
            sh "docker build -t ${DOCKERHUB_USERNAME}/${dockerImage} ."
            // Push the tagged image to Docker Hub
            sh "docker push ${DOCKERHUB_USERNAME}/${dockerImage}"
          }
        }
      }
    }

    stage('Deploy to GKE') {
      when {
        beforeAgent true
      }
      steps {
        script {
          withCredentials([file(credentialsId: 'gke-service-account-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
            sh "gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}"
            sh "gcloud config set project ${PROJECT_ID}"
            sh "gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE}"
            sh "kubectl apply -f k8s/deployment.yaml"
            sh "kubectl apply -f k8s/service.yaml"
            sh "kubectl apply -f k8s/ingress.yaml"
          }
        }
      }
    }
  }
}
