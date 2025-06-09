# SukjeNogi Backend

숙제노기 프로젝트의 백엔드 서버입니다. FastAPI로 작성되었으며 캐릭터별 과제 관리 기능 등을 REST API로 제공합니다.

## 실행 방법

### Docker 사용
```bash
docker build -t sukjenogi-backend .
docker run -d --env-file .env -p 8000:8000 sukjenogi-backend
```

### docker-compose 사용
`docker-compose.yml` 파일에 필요한 환경변수를 정의한 뒤 다음 명령으로 실행할 수 있습니다.
```bash
docker compose up -d --build
```

서버가 시작되면 `http://localhost:8000` 에서 서비스에 접근할 수 있습니다.
