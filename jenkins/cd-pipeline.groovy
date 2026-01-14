pipeline {
    agent {
        docker {
            image 'alpine/helm:3.12.0'
        }
    }

    environment {
        REGISTRY = "nexus.mydomain1234.shop/food-ordering-system" //Change the Repo
        IMAGE_TAG = "${BUILD_NUMBER}"
        APP_NAME = "food-ordering"
        NAMESPACE = "food-order"
        HELM_CHART = "helm-chart/food-ordering"
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        
        stage('Helm Version') {
            steps {
                sh 'helm version'
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/GimhanPerera/food-order-system-microservice-application-v1.git'
            }
        }
        

        stage('Deploy with Helm') {
            steps {
                withCredentials([file(
                    credentialsId: 'k3s-kubeconfig',
                    variable: 'KUBECONFIG'
                )]) {
                    sh '''
                      helm upgrade --install $APP_NAME $HELM_CHART \
                        --namespace $NAMESPACE \
                        --create-namespace \
                        --set adminUi.image=$REGISTRY \
                        --set adminUi.image=1
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful 🚀"
        }
        failure {
            echo "Deployment failed ❌"
        }
    }
}
