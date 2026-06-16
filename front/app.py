import streamlit as st
import requests

st.set_page_config(page_title="보안 솔루션 추천 시스템", layout="centered")

st.title("맞춤형 정보보안 솔루션 및 아키텍처 추천 시스템")
st.write("학번: 2025404019 | 이름: 오태윤")
st.markdown("---")

st.subheader("기업 환경 및 보안 요구사항 입력")

env_type = st.selectbox(
    "1. 현재 운영 중이거나 구축 예정인 인프라 환경을 선택하세요.",
    ["클라우드 (AWS/Azure/GCP)", "온프레미스 (자체 서버실/IDC)", "하이브리드 (클라우드 + 자체 서버)"]
)

security_concern = st.radio(
    "2. 현재 가장 우선적으로 해결해야 하는 보안 우려 사항은 무엇인가요?",
    ["계정 권한 관리 및 내부자 위협", "외부 해킹 공격 및 네트워크 침입", "데이터 유출 및 랜섬웨어 방지"]
)

scale = st.select_slider(
    "3. 조직 및 시스템 인프라의 규모를 선택하세요.",
    options=["스타트업/소규모", "중소기업", "중견/대기업"]
)

st.markdown("---")

if st.button("맞춤형 보안 솔루션 추천받기"):
    with st.spinner("FastAPI 백엔드 엔진으로부터 보안 아키텍처를 계산 중입니다..."):
        try:
            backend_url = "http://fastapi-back:8000/recommend"
            
            payload = {
                "env_type": env_type,
                "security_concern": security_concern,
                "scale": scale
            }
            
            response = requests.post(backend_url, json=payload, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                
                st.success(f"추천된 보안 아키텍처 등급: {result['architecture_grade']}")
                
                st.subheader("핵심 추천 솔루션")
                st.info(f"{result['main_solution']}")
                
                st.subheader("필수 보안 체크리스트 및 이행 가이드")
                for i, step in enumerate(result["action_plan"], 1):
                    st.write(f"{i}. {step}")
                    
                st.caption("※ 본 추천은 Rule-based 보안 알고리즘에 의해 계산된 맞춤형 가이드라인입니다.")
            else:
                st.error("백엔드 서버로부터 올바른 응답을 받지 못했습니다.")
                
        except requests.exceptions.ConnectionError:
            st.error("FastAPI 백엔드 서버(fastapi-back)에 연결할 수 없습니다. Docker 컨테이너 통신 설정을 확인하세요.")