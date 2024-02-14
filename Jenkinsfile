pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/Kihara-Njoroge/Order-Management-System-API.git'
      }
    }

    stage('Build and Push Docker Image') {
      steps {
        script {
          def dockerImage = 'babuuh/order-management-system-api'

          echo "Building Docker image: ${dockerImage}"

          // Build the Docker image using Docker Compose
          sh "docker compose build"

          // Push the built image using its ID
          withCredentials([usernamePassword(credentialsId: 'DockerHubCredentials', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
            echo "Pushing Docker image: ${dockerImage}"
            sh "echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin"
            sh "docker push ${dockerImage}"
          }
        }
      }
    }
    

    stage('Run Tests') {
      steps {
        script {
          sh 'sudo apt install -y python3.11-venv'
          sh '''
          /usr/bin/python3.11 -m venv venv
          . venv/bin/activate
          pip install pytest
          pytest test_example.py
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
