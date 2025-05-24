pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Build & Deploy') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d --build'
            }
        }
    }

    post {
        failure {
            echo '❌ 배포 실패!'
        }
        success {
            echo '✅ 배포 성공!'
        }
    }
}