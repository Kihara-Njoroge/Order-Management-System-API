pipeline {
  agent any

  environment {
    PROJECT_ID = 'savannar-test'
    CLUSTER_NAME = 'savannah-test-api'
    ZONE = 'africa-south1-a'
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

    // stage('Run Tests') {
    //   steps {
    //     script {
    //       echo "Running Tests"

    //       sh 'sudo -S apt install -y python3.11-venv'
    //       sh '''
    //       /usr/bin/python3.11 -m venv venv
    //       . venv/bin/activate
    //       pip install pytest
    //       pytest test_example.py
    //       deactivate
    //       '''

    //       def exitCode = sh(returnStdout: true, script: 'echo $?').trim()
    //       if (exitCode == '0') {
    //         echo "Tests passed!"
    //       } else {
    //         echo "Tests failed! Exit code: ${exitCode}"
    //         // remember to add Slack notification
    //         echo "Tests failed!"

    //       }
    //     }
    //   }
    // }

    stage('Deploy to GKE') {
      when { expression {
        sh(returnStdout: true, script: 'echo $?').trim() == '0' // Run only if tests pass
      }}
      steps {
        script {
          withCredentials([file(credentialsId: 'gke-service-account-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
            sh "gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}"
            sh "gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE} --project ${PROJECT_ID}"
            sh "kubectl apply -f k8s/deployment.yaml"
            sh "kubectl apply -f k8s/service.yaml"
            sh "kubectl apply -f k8s/ingress.yaml"
          }
        }
      }
    }
  }
}
