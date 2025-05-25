pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                // 필요한 경우 워크스페이스 초기화
                deleteDir()
                git credentialsId: 'nightbug', url: 'https://gitea.biryu2000.kr/nightbug/sukjenogi-backend.git', branch: 'master'
            }
        }

        stage('Build & Deploy') {
            steps {
                sh 'docker compose down || true' // 실패해도 계속
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
