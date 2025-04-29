pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'neerajbolla/dockerized-flask-app-flask'
        DOCKER_CREDENTIALS_ID = 'docker hub credentials'
        GIT_SSL_NO_VERIFY = 'true'  // This line disables SSL verification for Git operations
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo "📥 Cloning your Flask repo..."
                git branch: 'main', url: 'https://github.com/neeraj0654/docker-flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🔨 Building Docker image..."
                script {
                    docker.build(DOCKER_IMAGE, '.')
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                echo "🔐 Logging in to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'docker hub credentials', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh "echo \$PASSWORD | docker login -u \$USERNAME --password-stdin"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "📤 Pushing image to Docker Hub..."
                script {
                    docker.image(DOCKER_IMAGE).push("latest")
                }
            }
        }

        stage('Deploy Container') {
            steps {
                echo "🚀 Deploying container from pushed image..."
                script {
                    sh '''
                        docker ps -q --filter "name=flask-app" | grep . && docker stop flask-app || echo "No running container"
                        docker ps -a -q --filter "name=flask-app" | grep . && docker rm flask-app || echo "No container to remove"
                        docker run -d --name flask-app -p 5000:5000 neerajbolla/dockerized-flask-app-flask:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up...'
        }
        success {
            echo '✅ Flask app deployed successfully from Docker Hub!'
        }
        failure {
            echo '❌ Deployment failed. Check console output for errors.'
        }
    }
}
