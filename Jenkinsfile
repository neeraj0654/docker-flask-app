pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'dockerized-flask-app-flask'
        REPO_URL = 'https://github.com/neeraj0654/docker-flask-app.git'
        BRANCH_NAME = 'main' // Set your branch name here
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // This is to ensure that the correct branch is checked out
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    docker.build("${DOCKER_IMAGE_NAME}")
                }
            }
        }

        stage('Login to Docker') {
            steps {
                script {
                    // Log into Docker registry using credentials (replace with your actual credentialsId)
                    withDockerRegistry([credentialsId: 'docker-hub-credentials', url: 'https://index.docker.io/v1/']) {
                        echo 'Logged in to Docker registry.'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Push the Docker image to the registry
                    docker.image("${DOCKER_IMAGE_NAME}").push()
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    // Deploy the container on the desired host
                    docker.image("${DOCKER_IMAGE_NAME}").run('-d -p 5000:5000')
                }
            }
        }

        stage('Post Actions') {
            steps {
                echo 'Deployment complete.'
            }
        }
    }

    post {
        always {
            cleanWs() // Clean up the workspace after the build
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs above for errors.'
        }
    }
}
