pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        APP_DIR = 'app'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                echo "🧹 Cleaning up previous build files..."
                cleanWs()
            }
        }

        stage('Clone Repository') {
            steps {
                echo "📥 Cloning GitHub repository..."
                git url: 'https://github.com/neeraj0654/docker-flask-app.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "📦 Installing Python packages inside container..."
                sh '''
                docker run --rm -v $(pwd)/${APP_DIR}:/app python:3.11-slim bash -c "
                  cd /app &&
                  pip install -r requirements.txt
                "
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                echo "🔨 Building Docker images..."
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} build"
            }
        }

        stage('Run Containers') {
            steps {
                echo "🚀 Running containers with Docker Compose..."
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d"
                sh "sleep 5" // Give Flask time to boot
            }
        }

        stage('Test Health') {
            steps {
                echo "🔍 Testing if Flask app is running correctly..."
                script {
                    def response = sh(script: "curl -s http://localhost:5000 || true", returnStdout: true).trim()
                    if (!response.contains("Live System Updates")) {
                        error("❌ Flask app did not respond as expected.")
                    } else {
                        echo "✅ Flask app is live and responding!"
                    }
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline executed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check the build logs for details.'
        }
    }
}
