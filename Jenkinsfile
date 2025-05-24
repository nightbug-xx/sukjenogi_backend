pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://gitea.biryu2000.kr/nightbug/sukjenogi-backend.git', branch: 'master'
            }
        }

        stage('Build & Deploy') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d --build'
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