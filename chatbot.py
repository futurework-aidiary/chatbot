from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.memory import ConversationBufferMemory
# from langchain.memory import ConversationSummaryBufferMemory
import os

print("chatbot start")

# OpenAI API Key
# project-aidiary
os.environ["OPENAI_API_KEY"] = "<Key>"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM
llm = ChatOpenAI(openai_api_key = OPENAI_API_KEY,
                temperature=1,               # 창의성 (0.0 ~ 2.0) 
                max_tokens=2048,             # 최대 토큰수
                model_name='gpt-3.5-turbo',  # 모델명
                )

memory = ConversationBufferMemory(
        llm=llm,
        max_token_limit=2048,
        memory_key="history",
        return_messages=True,
)
#---------------------------------------
# response = llm.invoke("안녕")
# response = chain.invoke({"input": "안녕"})
context = "너는 아동과의 대화를 통해 하루 일상을 물어보며 감정과 상황을 파악하는 챗봇이야. 마지막 말에 이어서 대화를 진행해줘."
        
make_diary = "대화가 끝난 후에는 대화를 한 아동의 입장에서 일기를 요약해주는 기능도 있어. 지금까지 대화한 내용만 포함해서 일기를 작성해줘. 맨 위에는 오늘 날짜와 기분을 적어주고, 그 아래에 대화내용을 담은 일기를 10살 아이와 같이 적어줘."

class Chatbot():
    def __init__(self):
        
        # prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"{context}\n"), # system
            MessagesPlaceholder(variable_name="history"), # chat history: input_variable
            ("user", "{input}") # user: input_variable
        ])

        self.chain = prompt | llm

        print("chat start")

    def load_memory(self):
        return memory.load_memory_variables({}).get("history", "")
    
    def chat(self, user_input):
        
        # while True:
        #     # 사용자 입력 받기
        #     user_input = input("You: ")
        chat_history = self.load_memory()
        
        if user_input.lower() in ["exit", "quit"]:
            print("대화를 종료합니다. 일기 작성을 시작합니다.")
 
            daily_diary = self.make_diary(chat_history)
            
            return daily_diary
        
        response = self.chain.invoke({"input": user_input,
                                        "history": chat_history})
        memory.save_context(
            {"human": user_input},
            {"ai": response.content}
        )
        
        return response.content
    
    def make_diary(self, chat_history):
        daily_diary = self.chain.invoke({"input": make_diary,
                                        "history": chat_history})
        return daily_diary.content
    
    def __del__(self):
        print("chat end")
    
    # # 챗봇 응답 가져오기
    # response = self.chain.invoke({"input": user_input})
    # print(f"Chatbot: {response.content}")
