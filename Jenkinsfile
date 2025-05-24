pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Build & Deploy') {
            steps {
                echo '🔄 기존 컨테이너 중지 중...'
                sh 'docker compose down'

                echo '🚀 새 이미지 빌드 및 컨테이너 실행 중...'
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
