pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Clone Repository') {
            steps {
                git 'https://github.com/neeraj0654/docker-flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("dockerized-flask-app-flask")
                }
            }
        }

        stage('Login to Docker') {
            steps {
                script {
                    withDockerRegistry([credentialsId: 'docker-credentials', url: 'https://index.docker.io/v1/']) {
                        echo 'Logged in to Docker registry.'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.image('dockerized-flask-app-flask').push()
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    docker.image('dockerized-flask-app-flask').run('-d -p 5000:5000')
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
