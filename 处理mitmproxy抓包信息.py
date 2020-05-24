from mitmproxy import ctx
import json
# mitmweb -q -s example_script.py
questions = []

# 处理服务器响应的内容
def response(flow):
    # 获取响应对象
    text = flow.response.text
    if 'title' in text:
        data = json.loads(text)
        question = data["data"]["title"]
        if question not in questions:
            questions.append(question)
            print(f"当前题库数量{len(questions)}")
            with open(r"题库.txt",encoding='utf-8',mode = "a") as f:
                for answer in data["data"]["allAnswerList"]:
                    question+=f"@@@{answer['answer']}"
                f.write(question)
        print(data)

    