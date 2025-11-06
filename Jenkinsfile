pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/sneha597-kim/OnlineBankingSystem.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images for all microservices...'
                sh 'docker build -t auth-service ./auth-service'
                sh 'docker build -t account-service ./account-service'
                sh 'docker build -t transaction-service ./transaction-service'
            }
        }

        stage('Run Containers') {
            steps {
                echo 'Running all services...'
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        success {
            echo '✅ Build and deployment completed successfully!'
        }
        failure {
            echo '❌ Build failed. Check logs!'
        }
    }
}
