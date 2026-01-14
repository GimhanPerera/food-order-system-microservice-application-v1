pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {
        REGISTRY     = "nexus.mydomain1234.shop/food-ordering-system"
        SONAR_SERVER = "sona-server-1"
        DOCKER_CREDS = "nexus"
	APPLICATION_SERVICE = "admin-ui"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/test-cicd']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/GimhanPerera/food-order-system-microservice-application-v1.git',
                        credentialsId: 'github-credentials'
                    ]]
                ])
            }
        }

        stage('Init') {
            steps {
                script {
                    env.GIT_SHA   = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    env.IMAGE_TAG = "${env.GIT_SHA}-${env.BUILD_NUMBER}"
                }
            }
        }

        stage('Pipeline') {
            when {
                changeset "**/application-code/k8-application-code/${APPLICATION_SERVICE}/**"
            }
            stages {

                stage('Sonar Scan') {
                    steps {
                        withSonarQubeEnv("${SONAR_SERVER}") {
                            sh """
                                $SONAR_RUNNER_HOME/bin/sonar-scanner \
                                  -Dsonar.projectKey=admin-backend \
                                  -Dsonar.sources=application-code/k8-application-code/${APPLICATION_SERVICE} \
                                  -Dsonar.host.url=$SONAR_HOST_URL \
                                  -Dsonar.login=$SONAR_AUTH_TOKEN
                            """
                        }
                    }
                }

                stage('Quality Gate') {
                    steps {
                        timeout(time: 5, unit: 'MINUTES') {
                            waitForQualityGate abortPipeline: true
                        }
                    }
                }

                stage('Trivy FS Scan - Admin Backend') {
                    steps {
                        sh """
                            trivy fs \
                              --severity HIGH,CRITICAL \
                              --exit-code 1 \
                              application-code/k8-application-code/${APPLICATION_SERVICE}
                        """
                    }
                }

                stage('Build Image') {
                    steps {
                        script {
                            docker.build(
                                "${REGISTRY}/${APPLICATION_SERVICE}:${IMAGE_TAG}",
                                "application-code/k8-application-code/${APPLICATION_SERVICE}"
                            )
                        }
                    }
                }

                stage('Trivy Image Scan') {
                    steps {
                        sh """
                            trivy image \
                              --severity HIGH,CRITICAL \
                              --exit-code 1 \
                              ${REGISTRY}/${APPLICATION_SERVICE}:${IMAGE_TAG}
                        """
                    }
                }

                stage('Push Image') {
                    steps {
                        script {
                            docker.withRegistry("https://${REGISTRY}", DOCKER_CREDS) {
                                docker.image("${REGISTRY}/${APPLICATION_SERVICE}:${IMAGE_TAG}").push()
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build ${BUILD_NUMBER} completed successfully"
        }
        failure {
            echo "❌ Build ${BUILD_NUMBER} failed"
        }
        always {
            cleanWs()
        }
    }
}
