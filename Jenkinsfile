pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'neerajbolla'
        DOCKER_IMAGE_NAME = "${DOCKER_USERNAME}/dockerized-flask-app-flask"
        REPO_URL = 'https://github.com/neeraj0654/docker-flask-app.git'
        BRANCH_NAME = 'main' // Set your branch name here
        PATH = "/usr/local/bin:$PATH" // Ensure Docker is found
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Ensure the correct branch is checked out
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '/usr/local/bin/docker build -t ${DOCKER_IMAGE_NAME} .'
                }
            }
        }

        stage('Login to Docker') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                            echo 'Logged in to Docker registry.'
                        '''
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh '/usr/local/bin/docker push ${DOCKER_IMAGE_NAME}'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    sh '/usr/local/bin/docker run -d -p 5005:5000 ${DOCKER_IMAGE_NAME}'
                }
            }
        }

        stage('Post Actions') {
            steps {
                echo 'Deployment complete.'
            }
        }
    }
}
