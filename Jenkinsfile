pipeline {
  agent {
    docker {
      image 'python:3.11' // Use a Docker image with Python 3.11 preinstalled
      args '-u root' // Run Docker container as root to allow package installation
    }
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
            // Build the Docker image using Docker Compose
            sh "docker compose build"
            // Tag the Docker image to avoid access denied error
            sh "docker tag ${dockerImage} ${DOCKERHUB_USERNAME}/${dockerImage}"
            // Push the tagged image using
            sh "docker push ${DOCKERHUB_USERNAME}/${dockerImage}"
          }
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          sh '''
          python3.11 -m venv venv
          . venv/bin/activate
          pip install pytest
          pytest
          deactivate
          '''
        }
      }
    }

    stage('Deploy to Minikube') {
      steps {
        script {
          sh 'echo "Debug information"'

          withCredentials([file(credentialsId: 'kubeconfig-id', variable: 'KUBECONFIG')]) {
            sh "kubectl --kubeconfig=${KUBECONFIG} apply -f deployment.yaml"
            sh "kubectl --kubeconfig=${KUBECONFIG} apply -f service.yaml"
            sh "kubectl --kubeconfig=${KUBECONFIG} apply -f ingress.yaml"
          }

          sh 'echo "End of Debug information"'

          sh 'echo "DONE"'
        }
      }
    }
  }
}
