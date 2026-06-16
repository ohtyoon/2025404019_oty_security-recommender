import streamlit as st
import requests
import os

# 페이지 기본 설정
st.set_page_config(page_title="DevSecOps 추천 엔진", page_icon="🛡️", layout="wide")

st.title("🛡️ 개발 환경 맞춤형 보안 가이드 및 도구 추천 서비스")
st.write("본인의 프로젝트 환경을 선택하면, 안전한 서비스를 빌드하기 위한 아키텍처 가이드와 필수 보안 컴포넌트를 추천합니다.")
st.markdown("---")

# 환경변수로부터 FastAPI 주소를 읽어오되, 없으면 기본값(로컬주소) 사용
# 로컬 테스트용: http://localhost:8000
# EC2 배포 시: 백엔드 실행 시 환경변수로 지정하거나, 배포 전 아래 하드코딩 부분 수정 가능
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("프로젝트 명세 입력")
    
    project_type = st.selectbox(
        "1. 프로젝트 애플리케이션 유형",
        ["Web Application (Frontend/Backend)", "Mobile Application (Android/iOS)", "IoT/Embedded Service", "Game Server"]
    )
    
    language = st.radio(
        "2. 주요 개발 언어 및 프레임워크",
        ["Python (FastAPI, Django, Flask)", "Java (Spring Boot)", "JavaScript / TypeScript (Node.js, Next.js)", "Go / Rust"]
    )
    
    deployment_env = st.selectbox(
        "3. 아키텍처 및 배포 환경",
        ["AWS EC2 / Docker Container", "AWS Lambda (Serverless)", "Vercel / Netlify (Jamstack)", "On-Premise Server"]
    )
    
    security_priority = st.selectbox(
        "4. 가장 집중해야 하는 보안 영역",
        ["데이터 암호화 및 프라이버시", "사용자 인증 및 권한 인가(Auth)", "오픈소스 및 코드 취약점 스캔", "DDoS 및 악성 트래픽 방어"]
    )
    
    submit_btn = st.button("맞춤형 보안 아키텍처 분석 요청")

with col2:
    st.subheader("실시간 보안 엔진 분석 결과")
    
    if submit_btn:
        payload = {
            "project_type": project_type,
            "language": language,
            "deployment_env": deployment_env,
            "security_priority": security_priority
        }
        
        try:
            with st.spinner("FastAPI 백엔드 엔진에서 추천 결과를 연산 중입니다"):
                response = requests.post(f"{BACKEND_URL}/recommend", json=payload, timeout=5)
                
            if response.status_coords == 200 or response.status_code == 200:
                result = response.json()
                
                risk = result.get("risk_level", "Medium")
                if risk == "Critical":
                    st.error(f"예상 프로젝트 기본 위험도: {risk}")
                elif risk == "High":
                    st.warning(f"예상 프로젝트 기본 위험도: {risk}")
                else:
                    st.info(f"예상 프로젝트 기본 위험도: {risk}")
                
                st.markdown("### 추천 보안 라이브러리 및 도구")
                tools = result.get("recommended_libraries_and_tools", [])
                if tools:
                    for tool in tools:
                        st.markdown(f"- `{tool}`")
                else:
                    st.write("추천된 전용 도구가 없습니다.")
                    
                st.markdown("### 단계별 개발 보안 조치 조언 (Action Items)")
                guides = result.get("security_action_items", [])
                for idx, guide in enumerate(guides, 1):
                    st.write(f"**{idx}.** {guide}")
                    
                with st.expander("FastAPI 제공 원본 데이터 확인 (JSON)"):
                    st.json(result)
                    
        except requests.exceptions.ConnectionError:
            st.error(f"백엔드 서버({BACKEND_URL})에 연결할 수 없습니다. FastAPI 가동 상태 및 포트/환경변수를 확인하세요.")
        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
    else:
        st.info("왼쪽 양식을 입력하고 버튼을 누르면 FastAPI가 동적으로 생성한 추천 보안 아키텍처가 여기에 표시됩니다.")