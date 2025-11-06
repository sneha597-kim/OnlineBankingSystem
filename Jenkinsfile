pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo '📦 Checking out the repository...'
                git branch: 'main', url: 'https://github.com/sneha597-kim/OnlineBankingSystem.git'
            }
        }

        stage('Build Microservice Images') {
            steps {
                echo '🔨 Building Docker images for all microservices...'
                bat 'docker build -t auth-service ./auth-service'
                bat 'docker build -t account-service ./account-service'
                bat 'docker build -t transaction-service ./transaction-service'
            }
        }

       /* stage('Build Main App Image') {
            steps {
                echo '🏗️ Building main banking app image...'
                bat 'docker build -t banking-app .'
            }
        }*/

       stage('Run Containers') {
    steps {
        echo '🚀 Running all containers...'
        bat '''
        docker rm -f auth-service || true
        docker rm -f account-service || true
        docker rm -f transaction-service || true
        
        docker run -d --name auth-service -p 5001:5000 auth-service
        docker run -d --name account-service -p 5002:5000 account-service
        docker run -d --name transaction-service -p 5003:5000 transaction-service
        '''
    }
}
    }

    post {
        success {
            echo '✅ Build and deployment completed successfully!'
        }
        failure {
            echo '❌ Build failed. Check console output for details.'
        }
    }
}

