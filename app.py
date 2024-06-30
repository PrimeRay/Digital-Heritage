from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 加载 .env 文件
load_dotenv()

# 获取环境变量
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

print(f"API Key: {GOOGLE_API_KEY}")

# 配置 Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# 创建 Gemini 模型实例
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record_activity():
    activity = request.form['activity']
    
    prompt = f"我是老人，请帮我回顾日程，并给出养生建议：{activity}"
    
    print(f"Sending prompt to Gemini API: {prompt}")
    
    try:
        response = model.generate_content(prompt)
        print(f"Raw API response: {response}")
        
        if response.text:
            ai_response = response.text
        else:
            print("API response text is empty")
            ai_response = "API 返回了空响应。"
    except Exception as e:
        print(f"Error calling Gemini API: {str(e)}")
        ai_response = f"抱歉，无法获取AI建议。错误: {str(e)}"
    
    return jsonify({"summary": ai_response})

if __name__ == '__main__':
    app.run(debug=True)