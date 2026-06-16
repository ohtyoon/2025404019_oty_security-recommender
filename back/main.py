from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Security Recommendation API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    env_type: str
    security_concern: str
    scale: str

@app.post("/recommend")
def calculate_recommendation(request: RecommendRequest):
    env = request.env_type
    concern = request.security_concern
    scale = request.scale

    architecture_grade = "Standard Security Baseline"
    main_solution = "종합 엔드포인트 및 네트워크 기본 보안 솔루션"
    action_plan = [
        "임직원 PC 백신 프로그램 설치 및 실시간 감시 활성화",
        "운영체제 및 주요 소프트웨어 정기 보안 패치 프로세스 수립"
    ]

    if "클라우드" in env:
        architecture_grade = "Cloud-Native Zero Trust Architecture"
        if "계정 권한" in concern:
            main_solution = "클라우드 Identity & Access Management (IAM) 통제 체계"
            action_plan = [
                "모든 클라우드 관리자 계정에 MFA(2차 인증) 필수 적용",
                "사용자별 최소 권한 원칙 기반 IAM Role 재정비",
                "AWS CloudTrail / 루트 계정 접근 로그 실시간 모니터링 및 알림 설정"
            ]
        elif "외부 해킹" in concern:
            main_solution = "경계 기반 네트워크 보안 및 WAF(웹 방화벽) 레이어 구축"
            action_plan = [
                "인바운드 보안 그룹 규칙 타이트닝 (불필요 포트 차단)",
                "AWS WAF 또는 Cloudflare를 연동하여 웹 애플리케이션 취약점 공격 차단",
                "VPC 내부 서브넷(Public/Private) 분리 및 가상 라우팅 격리"
            ]
        else:
            main_solution = "클라우드 데이터 암호화 및 백업 아키텍처"
            action_plan = [
                "AWS KMS 등을 이용한 저장 데이터 및 전송 데이터 암호화",
                "S3 버킷 퍼블릭 액세스 전면 차단 및 버킷 정책 검토",
                "교차 리전 데이터 자동 백업 및 복구 프로세스 시뮬레이션"
            ]

    elif "온프레미스" in env or "하이브리드" in env:
        architecture_grade = "Defense-in-Depth (심층 방어) 인프라 아키텍처"
        if "외부 해킹" in concern:
            main_solution = "차세대 방화벽(NGFW) 및 침입 차단 시스템(IPS) 도입"
            action_plan = [
                "네트워크 DMZ 구간 설정을 통한 내부 핵심 자산 망분리 보호",
                "주기적인 외부 IP 대역 포트 스캔 검사 및 불필요 서비스 데몬 중지",
                "서버 침입 탐지 시스템(HIDS) 도입을 통한 주요 설정 파일 변조 감시"
            ]
        else:
            main_solution = "엔터프라이즈 통합 접근 제어 및 백업 솔루션"
            action_plan = [
                "서버 접근 제어 솔루션 도입을 통한 작업 로그 무결성 확보",
                "랜섬웨어 감염 대비 네트워크가 분리된 독립 오프라인 백업 체계 구축"
            ]

    if scale == "중견/대기업":
        action_plan.append("통합 로그 분석 및 보안 관제를 위한 SIEM 솔루션 연동 검토")
    elif scale == "스타트업/소규모":
        action_plan.append("오픈소스 보안 도구를 활용한 비용 절감형 보안 운영")

    return {
        "architecture_grade": architecture_grade,
        "main_solution": main_solution,
        "action_plan": action_plan
    }