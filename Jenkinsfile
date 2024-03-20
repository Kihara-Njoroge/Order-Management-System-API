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
            // Build the Docker image using Docker Compose
            sh "docker compose build --no-cache"
            // Tag the Docker image to avoid access denied error
            sh "docker tag ${dockerImage} ${DOCKERHUB_USERNAME}/${dockerImage}"
            // Push the tagged image using
            sh "docker push ${DOCKERHUB_USERNAME}/${dockerImage}"
          }
        }
      }
    }


    // stage('Deploy to GKE') {
    //   when { expression {
    //     sh(returnStdout: true, script: 'echo $?').trim() == '0' // Run only if tests pass
    //   }}
    //   steps {
    //     script {
    //       withCredentials([file(credentialsId: 'gke-service-account-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
    //         sh "gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}"
    //         sh "gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE} --project ${PROJECT_ID}"
    //         sh "kubectl apply -f k8s/deployment.yaml"
    //         sh "kubectl apply -f k8s/service.yaml"
    //         sh "kubectl apply -f k8s/ingress.yaml"
    //       }
    //     }
    //   }
    // }

      stage('Deploy to Minikube') {
      steps {
        script {
          sh 'echo "Debug information"'

          withCredentials([file(credentialsId: 'kubeconfig-id', variable: 'KUBECONFIG')]) {
            sh "kubectl --kubeconfig=${KUBECONFIG} apply -f k8/sdeployment.yaml"
            sh "kubectl --kubeconfig=${KUBECONFIG} apply -f k8s/service.yaml"
            sh "kubectl --kubeconfig=${KUBECONFIG} apply -f 4k8s/ingress.yaml"

            sh 'echo "End of Debug information"'

          }

          sh 'echo "DONE"'

        
      }
    }
  }
  }
}
