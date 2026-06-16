from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Security Architecture Recommender API")

# CORS 설정: Streamlit 컨테이너가 어디서든 접근할 수 있도록 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 사용자 입력 값을 받기 위한 데이터 모델 정의
class RecommendationRequest(BaseModel):
    project_type: str        # 예: Web, Mobile App, IoT, Game Server
    language: str            # 예: Python, Java, JavaScript, Go
    deployment_env: str      # 예: AWS EC2, AWS Lambda, On-Premise, Vercel
    security_priority: str   # 예: 데이터 암호화, 인증/인가, 취약점 스캔, DDoS 방어

@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Security API is running"}

@app.post("/recommend")
def get_security_recommendation(request: RecommendationRequest):
    # 기본값 구조 설계 (개인별 논리적 차별성 포인트)
    recommended_tools = []
    guide_steps = []
    risk_level = "Medium"
    
    # 1. 언어 및 프레임워크별 보안 라이브러리/도구 추천 (Rule-based)
    lang = request.language.lower()
    if "python" in lang:
        recommended_tools.extend(["Bandit (정적 분석)", "Safety (의존성 점검)", "Cryptography"])
    elif "java" in lang:
        recommended_tools.extend(["SpotBugs (FindSecBugs)", "Dependency-Check", "Spring Security"])
    elif "javascript" in lang or "node" in lang:
        recommended_tools.extend(["npm audit / Snyk", "Helmet.js", "Jose (JWT 라이브러리)"])
    else:
        recommended_tools.extend(["SonarQube", "OWASP Dependency-Check"])

    # 2. 프로젝트 유형별 가이드 및 위험도 설정
    proj = request.project_type.lower()
    if "web" in proj:
        risk_level = "High"
        guide_steps.append("OWASP Top 10 취약점(SQL Injection, XSS) 방어 코드를 적용하세요.")
        guide_steps.append("Session 만료 시간을 짧게 유지하고, JWT 검증 로직을 강화하세요.")
    elif "mobile" in proj:
        risk_level = "High"
        guide_steps.append("소스코드 난독화(ProGuard 등) 및 API Key 노출 방지를 위한 암호화를 적용하세요.")
        guide_steps.append("로컬 스토리지에 민감한 평문 데이터를 저장하지 마세요.")
    else:
        guide_steps.append("기본 포트 접근을 차단하고, 내부 통신망 분리를 검토하세요.")

    # 3. 배포 환경별 클라우드 보안 설정 추천
    env = request.deployment_env.lower()
    if "aws" in env:
        recommended_tools.append("AWS IAM (최소 권한 원칙)")
        guide_steps.append("AWS Security Group(보안 그룹)을 설정하여 인바운드 포트를 최소화하세요.")
        if "ec2" in env:
            guide_steps.append("EC2 인스턴스의 OS 커널 및 패키지를 주기적으로 업데이트(apt-get upgrade)하세요.")
    elif "vercel" in env or "lambda" in env:
        guide_steps.append("Serverless 환경에 맞춰 환경 변수(Environment Variables)를 철저히 은닉하세요.")

    # 4. 사용자의 핵심 관심 보안 분야 보완
    priority = request.security_priority
    if "암호화" in priority:
        guide_steps.append("DB 내 비밀번호는 반드시 bcrypt/argon2 등의 단방향 해시 알고리즘으로 저장하세요.")
    elif "인증" in priority:
        guide_steps.append("Multi-Factor Authentication(MFA) 도입 및 OAuth 2.0 표준을 준수하세요.")
    elif "취약점" in priority:
        guide_steps.append("CI/CD 파이프라인(GitHub Actions)에 도커 이미지 스캔(Trivy) 단계를 통합하세요.")
    elif "ddos" in priority:
        risk_level = "Critical"
        recommended_tools.append("Cloudflare / AWS WAF (웹 방화벽)")

    # 최종 JSON 응답 생성
    return {
        "requested_config": {
            "project_type": request.project_type,
            "language": request.language,
            "deployment_env": request.deployment_env,
            "security_priority": request.security_priority
        },
        "risk_level": risk_level,
        "recommended_libraries_and_tools": recommended_tools,
        "security_action_items": guide_steps
    }