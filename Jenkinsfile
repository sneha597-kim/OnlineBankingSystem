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

       /*stage('Build Main App Image') {
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
/*
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Add in Jenkins credentials
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out the repository...'
                git branch: 'main', url: 'https://github.com/sneha597-kim/OnlineBankingSystem.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '🔨 Building Docker images for all microservices...'
                bat 'docker build -t auth-service ./auth-service'
                bat 'docker build -t account-service ./account-service'
                bat 'docker build -t transaction-service ./transaction-service'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing images to Docker Hub...'
                bat '''
                docker login -u %DOCKERHUB_CREDENTIALS_USR% -p %DOCKERHUB_CREDENTIALS_PSW%
                docker tag auth-service sneha597/auth-service:latest
                docker tag account-service sneha597/account-service:latest
                docker tag transaction-service sneha597/transaction-service:latest
                docker push sneha597/auth-service:latest
                docker push sneha597/account-service:latest
                docker push sneha597/transaction-service:latest
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo '🚀 Deploying all services with Docker Compose...'
                bat '''
                docker-compose down || true
                docker-compose up -d --build
                '''
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD Pipeline executed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}*/
