from openai import OpenAI
import streamlit as st
from streamlit import _bottom


st.set_page_config(
   page_title="국무조정실 공공업무용 챗봇",
   page_icon="🧊",
   layout="wide",
)

st.markdown(
    """
    <style>
        .reportview-container .markdown-text-container {
            display: flex;
            justify-content: flex-end;
        }
        .block-container {
            padding-top: 4rem;
            padding-bottom: 2rem;
            padding-left: 4rem;
            padding-right: 4rem;
        }
    </style>
    <div class='caption' style='text-align: right;'> 양산시 ChatGPT 연구 학습 동호회 개발</div>
    """,
    unsafe_allow_html=True
)

st.title("국무조정실 공공업무용 챗봇(GPT-4o-mini)")
# API 키 입력창 생성
api_key = st.text_input("OpenAI API 키를 입력하세요:", type="password")

st.warning("**1. ChatGPT 활용방법 및 주의사항 안내를 확인 후 이용하시기 바랍니다.**\n\n"
           "**2. 공공업무용 챗봇은 최근 14개의 대화만 기억하여 답변하며, 브라우저를 새로 고침하면 대화 내용이 삭제됩니다.**\n\n")
if api_key:
    client = OpenAI(api_key=api_key)
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    if "messages" not in st.session_state: 
        st.session_state["messages"] = [{"role": "assistant", "content": "공직자 여러분 안녕하세요! 무엇을 도와드릴까요?"}]

        
    if "deleted_messages" not in st.session_state:
        st.session_state.deleted_messages = []

    avatars = {
        "user": "data_image/gok.png",
        "assistant": "data_image/gpt.png"
    }

    # 메시지를 최대 14개로 제한하는 함수
    def limit_messages():
        max_messages = 14
        while len(st.session_state.messages) > max_messages:
            deleted_message = st.session_state.messages.pop(0)  # 가장 오래된 메시지 삭제
            st.session_state.deleted_messages.append(deleted_message)  # 삭제된 메시지를 저장


    for message in st.session_state.messages:
        avatar = avatars.get(message["role"], None)
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("궁금한 내용을 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=avatars["user"]):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=avatars["assistant"]):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        limit_messages()  # 메시지 수 제한 함수 호출

        st.write(f"현재 메시지 수: {len(st.session_state.messages)}")
else:
    st.warning("API 키를 입력해 주세요.")

st.markdown(
"""
<style>
    section[data-testid="stSidebar"] {
        width: 470px !important; #사이드바 열었을때 창 크기
    }
</style>
""",
unsafe_allow_html=True,
)
with st.sidebar:

    st.sidebar.title("📣 ChatGPT 활용방법 및 주의사항 안내")
    st.write('<div style="text-align:right;"><strong>< 2023.05. 행정안전부 발행 기준 ></strong></div>', unsafe_allow_html=True)    
    # 간단한 요약
    
    summary = (
    "ChatGPT가 공공부문 업무 효율성을 높이기 위해 사용되지만, "
    "**:red[거짓 정보 생성]** 및 **:red[개인정보 유출]** 등의 문제를 발생시킬 수 있으니 아래 내용을 준수해 주세요.\n"
    )
    st.success(summary, icon=None)

    st.write("**📛 비공개 정보 및 개인정보를 입력하지 말 것**")
    st.write("**📛 인공지능 답변을 사실여부 검증 없이 이용하지 말 것**")

    pdf_file_path = "공무원을 위한_챗GPT 활용방법 및 주의사항 안내서.pdf"
    if st.download_button(
        label="공무원을 위한 ChatGPT 활용 및 주의사항 다운로드",
        data=open(pdf_file_path, "rb").read(),  # 파일을 읽어서 데이터로 설정
        file_name="공무원을 위한_챗GPT 활용방법 및 주의사항 안내서.pdf",
        mime="application/pdf"
        ):
        st.success("다운로드가 시작됩니다.")
        
    st.header("1. ChatGPT 소개")
    st.write("챗GPT(ChatGPT)는 OpenAI社의 초거대 언어모델인 GPT-3.5, GPT-4를 기반으로 동작하는 인공지능 챗봇 서비스")
    st.write("문장 내 앞서 등장한 단어를 기반으로 뒤에 어떤 단어가 등장해야 문장이 자연스러운지를 예측하여 대화의 맥락을 이해하고, 대화를 기억하는 등 사람처럼 응답하는 능력을 지님")

    st.header("2. ChatGPT 공공기관 활용 분야")
    
    st.subheader("가. 정보탐색능력 활용")
    st.write("새로운 콘텐츠 발굴과 문제 해결 방안을 위한 기획 및 보고서 작성, 구체적 질문을 통해 아이디어를 얻고 미확정 정책 유출에 주의해야 합니다.")
    with st.expander("**✔️ 아이디어 탐색 프롬프트(예시)**", expanded=False):
        st.write("1. 저출산 문제를 해결하기 위한 정책을 수립하려고 합니다. 돌봄, 사회적 인식, 고용, 정부 지원 등 다양한 측면에서 아이디어를 제시해 주세요.")
        st.write("2. 청년 일자리 증가를 위한 아이디어를 해외사례와 매칭하여 알려주세요. 지원 관련 금액과 기간 등 구체적인 수치도 포함해 주세요.")
        st.write("3. 지역화폐를 시민들이 잘 활용하도록 하기 위해 양산시는 어떤 노력을 해야 할까요? ")
        st.write("4. 해외에서 인공지능을 활용한 행정 서비스에 대해 열 가지를 알려주세요.")
        st.write("5. 플라스틱 신분증을 모바일 전자신분증으로 전환했을 때 장점과 단점은 무엇일까요?")

    with st.expander("**✔️ 국내외 자료조사 프롬프트(예시)**", expanded=False):
        st.write("1. 한국을 제외한 나라에서 정년(연금수령 연령) 연장 사례와 그에 관련된 연구내용에 대해 알려주세요.")
        st.write("2. 남성의 육아휴직이 저출산에 미치는 영향에 대해 연구된 내용들을 알려주세요.")
        st.write("3. 공식적 자료를 활용하여 애플의 스마트폰 매출액과 삼성전자의 스마트폰 매출액을 2019년 1분기부터 2020년 3분기까지 비교해주세요. 해당 자료의 출처도 말해주세요.")
        st.write("4. 자연어  처리  인공지능  알고리즘에  대한  논문인  ‘Attention  is  all you need’에 대해 비전공자도 알기 쉽게 설명해주세요")

    
    st.subheader("나. 언어능력 활용")
    st.write("보도자료, 인사말, 강의 자료 등 대외 공개 자료의 효율적 작성을 위해 초안이 필요할 경우, 미확정 정책이나 비공개 정보, 개인정보를 입력할 때 정보 유출에 주의해야 합니다.")
    with st.expander("**✔️ 보도자료 등 초안 작성 프롬프트(예시)**", expanded=False):
        st.write("1. 초거대 AI 공공부문 활용방안 세미나 개최계획을 기초로 보도자료로 만들려고 합니다. 아래 계획을 참고하여 보도자료를 만들어 주세요. 첫 문단에는 행사 개요와 목적, 둘째 문단에는 세미나 내용, 셋째 문단에는 공개토론을 통한 세미나의 기대효과를 넣어서 작성해주세요.")
        st.write("2. 인공지능의 공공부문 도입을 주제로 하는 세미나에서 인사말을 해야 하는데 초안을 1,500자 내외로 작성해주세요.")
        st.write("3. 청년 창업 지원에 대한 정부의 정책을 대학 졸업생들에게 쉽게 설명 하려 하는데 어떤 내용과 순서로 설명하면 좋을까요?")
    with st.expander("**✔️ 외부자료 요약 프롬프트(예시)**", expanded=False):
        st.write("1. ‘윤석열 대통령은 14일 디지털플랫폼정부 추진 과정에서 인공지능 (AI)‧소프트웨어 분야 등 전후방 효과가 클 것이라고 밝혔다...(생략)...’ 위 기사내용을 100자 내외로 요약해주세요")
        st.write("2. AI 기술이 발전할수록 사이버 범죄와 사생활 유출 가능성이 높아지고 있다. AI는 사람처럼 실수하지 않고 차별과 편견 없이...(생략)...’위 논문의 핵심을 10가지로 요약해주세요")
    with st.expander("**✔️ 언어 간 번역 프롬프트(예시)**", expanded=False):
        st.write("1. ‘La  direction  interministérielle  du  numérique  (DINUM)  est  en charge de la transformation numérique de l’État au bénéfice du citoyen comme de l’agent, ...(생략)...‘위 불어 자료를 한국어로 번역해주세요")
        st.write("2. ‘챗GPT가 공무원의 업무혁신을 이끈다 - 초거대 인공지능 공공부문 활용방안 세미나 개최 ...(생략)...’ 위 보도자료를 미국 언론보도 스타일로 번역해주세요.")


    st.subheader("다. 컴퓨터능력 활용")
    with st.expander("**✔️ 업무용 응용프로그램 사용법 탐색 프롬프트(예시)**", expanded=False):
        st.write("1. 엑셀 표에 입력된 값들 중 50을 넘는 값을 노란색으로 표시해주는 방법에 대해 알려주세요.")
        st.write("2. 2021년부터 2023년까지 사업 예산에 대한 연평균 증가율을 엑셀로 구하는 방법에 대해 알려주세요.")
    with st.expander("**✔️ 업무 자동화 프로그램 제작 프롬프트(예시)**", expanded=False):
        st.write("1. (엑셀 취합) 자료 조사로 기관들이 제출한 엑셀파일들을 하나의 파일로 취합하는 엑셀 매크로를 만들어주세요. -> 챗GPT는 엑셀 안에서 사용되는 프로그램(VBA) 코드를 생성")
        st.write("2. (기사 검색‧정리) ㅇㅇㅇ 뉴스에서 행정안전부와 관련된 기사를 찾아 제목, 링크, 내용을 정리하는 프로그램을 만들어주세요 -> 챗GPT는 파이썬 등의 프로그래밍 언어로 프로그램 코드를 생성")
 

