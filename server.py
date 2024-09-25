from flask import Flask
from flask import request, Response
from waitress import serve
import json

from chatbot import Chatbot

# Flask 인스터드 생성
app = Flask(__name__)

# Topic List
topics = [{'id':'aidiary', 'title':'aidiary', 'body':'futurework/api'},]

# 출력 template
def web_template(content):
    return f'''
            <html>
            <head>
            </head>
            <body>
                {content}
            </body>
            </html>
            '''
            
def response_template(content):
    return content            

# 127.0.0.1:5000/futurework/aidiary 으로 접근 
@app.route("/futurework/aidiary", methods=['POST'])

def aidiary():
    if request.method == 'POST':
        # 대화를 전달받음
        conversation = request.get_json()
        if not conversation:
            raise ValueError
                
    for topic in topics:
        if(topic["id"] == 'aidiary'):
            
            context = conversation["context"]
            text = conversation["text"]
            
            # chatbot
            aichatbot = Chatbot()
            user_input = text
            print(user_input)
            response = aichatbot.chat(user_input)
            
            # response = "response" # test
 
            content = f'''
                        <h2>
                        {topic["title"]}
                        </h2>
                        {topic["body"]}<br><br>
                        context : {context}<br><br>
                        text : {text}<br>
                        response : {response}<br>
                        '''       
            
            # result 불러오기
            ai_response = {
                "ai_response": response
                # "file" : open(f'{output_result}', 'r')
            }

            ai_response = Response(json.dumps(response_template(ai_response), ensure_ascii=False))
            ai_response.headers['Content-Type'] = 'application/json'
                
            return ai_response
            
if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
    #app.run(debug = True, host = '0.0.0.0', port = 5000)
    # 플라스크는 localhost라고 알려진 루프백 주소 127.0.0.1을 사용: IP와 관계없이 내 컴퓨터를 지목할 수 있음
    # 0.0.0.0을 사용: 외부서버에서도 접속가능
    # 플라스크는 테스트 프로토콜로 5000번 사용: 웹 서버가 실행중인 프로토콜 포트번포, 제품 서버에 사용되는 80번을 사용하지 않는다.