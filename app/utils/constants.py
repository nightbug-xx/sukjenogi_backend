# 서버 ID → 서버명
SERVER_MAP = {
    1: "아스테르",
    2: "세레브레이",
    3: "쿠아트",
    4: "루나리오",
    5: "알렉시아",
    6: "라사",
}

# 서버명 → 서버 ID (역방향 매핑)
SERVER_REVERSE_MAP = {v: k for k, v in SERVER_MAP.items()}
