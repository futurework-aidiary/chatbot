from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os

print("mj-start")

# OpenAI API Key
# project-aidiary
os.environ["OPENAI_API_KEY"] = "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"
# personal
# os.environ["OPENAI_API_KEY"] = "sk-EaRXGfNjr8rLvLTzDFPiO9W59kGszt5mjOejBi4j2pT3BlbkFJYPLUpLg9gLrMmKcYEDzQ83kOXSowBfGa-9AMu4f64A"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM
llm = ChatOpenAI(openai_api_key = OPENAI_API_KEY,
                 temperature=1,               # 창의성 (0.0 ~ 2.0) 
                 max_tokens=2048,             # 최대 토큰수
                 model_name='gpt-3.5-turbo',  # 모델명
                )
print("mj-llmdone")

# prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 아동과의 대화를 통해 하루 일상을 물어보며 감정과 상황을 파악하는 챗봇이야. 대화가 끝난 후에는 대화를 한 아동의 입장에서 일기를 요약해주는 기능도 있어."),
    ("user", "{input}")
])

chain = prompt | llm

print("mj-chatbot start")
#---------------------------------------
# response = llm.invoke("안녕")
# response = chain.invoke({"input": "안녕"})

# print(response.content)
make_diary = "지금까지 대화한 내용만 포함해서 일기를 작성해줘. 맨 위에는 오늘 날짜와 기분을 적어주고, 그 아래에 대화내용을 담은 일기를 10살 아이와 같이 적어줘."
while True:
    # 사용자 입력 받기
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("대화를 종료합니다. 일기 작성을 시작합니다.")        
        daily_diary = chain.invoke((make_diary))
        print(f"일기: {daily_diary.content}")
        break
    
    # 챗봇 응답 가져오기
    response = chain.invoke({"input": user_input})
    print(f"Chatbot: {response.content}")
