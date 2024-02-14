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
          def dockerImage = 'order-management-system-api'

          withCredentials([usernamePassword(credentialsId: 'DockerHubCredentials', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
            sh "echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin"
            sh "docker compose build"
            sh "docker tag ${dockerImage} ${DOCKERHUB_USERNAME}/${dockerImage}"
            sh "docker push ${DOCKERHUB_USERNAME}/${dockerImage}"
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
