pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo "Cleaning up previous build files..."
                cleanWs()
            }
        }

        stage('Checkout Code') {
            steps {
                echo "Checking out code from Git..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing required Python packages (inside container)..."
                sh '''
                docker run --rm -v $(pwd)/app:/app python:3.11-slim bash -c "
                  cd /app &&
                  pip install -r requirements.txt
                "
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                echo "Building Docker containers..."
                sh 'docker-compose build'
            }
        }

        stage('Run Containers') {
            steps {
                echo "Starting services using Docker Compose..."
                sh 'docker-compose up -d'
            }
        }

        stage('Test Health') {
            steps {
                echo "Testing if Flask app is running..."
                script {
                    def response = sh(script: "curl -s http://localhost:5000 || true", returnStdout: true).trim()
                    if (!response.contains("Live System Updates")) {
                        error("Flask app did not respond properly!")
                    } else {
                        echo "✅ Flask server is up and serving correctly!"
                    }
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Deployment pipeline completed successfully!'
        }
        failure {
            echo '❌ Something went wrong during pipeline execution.'
        }
    }
}
