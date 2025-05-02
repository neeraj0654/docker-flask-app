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
                // This is to ensure that the correct branch is checked out
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Use full path to ensure docker command is found
                    sh '/usr/local/bin/docker build -t ${DOCKER_IMAGE_NAME} .'
                }
            }
        }

  stage('Login to Docker') {
    steps {
        script {
            // Log into Docker registry using credentials
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
                    // Push the Docker image to the registry
                    sh '/usr/local/bin/docker push ${DOCKER_IMAGE_NAME}'
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    // Deploy the container on the desired host
                    sh '/usr/local/bin/docker run -d -p 5004:5000 ${DOCKER_IMAGE_NAME}'
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
