import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
import json
import logging

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def parse_event_from_text(text):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    从以下文本中提取事件信息：
    "{text}"
    
    请以JSON格式返回以下信息：
    {{
        "title": "事件标题",
        "location": "地点（如果有）",
        "companions": "同行者（如果有）",
        "event_time": "事件时间（如果有，格式为YYYY-MM-DD HH:MM:SS）"
    }}
    
    如果某项信息不存在，则将其值设为null。请确保返回的是有效的JSON格式，不要添加任何额外的解释或文本。
    """
    
    try:
        response = model.generate_content(prompt)
        logger.debug(f"Gemini API raw response: {response.text}")
        
        # 尝试提取JSON部分
        json_start = response.text.find('{')
        json_end = response.text.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            json_str = response.text[json_start:json_end]
            logger.debug(f"Extracted JSON string: {json_str}")
            event_data = json.loads(json_str)
        else:
            raise ValueError("无法在响应中找到有效的JSON")
        
        # 验证必要的字段
        required_fields = ['title', 'location', 'companions', 'event_time']
        for field in required_fields:
            if field not in event_data:
                event_data[field] = None
        
        if event_data['event_time']:
            event_data['event_time'] = datetime.strptime(event_data['event_time'], "%Y-%m-%d %H:%M:%S")
        else:
            event_data['event_time'] = datetime.now()
        
        return event_data
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析错误: {str(e)}")
        logger.error(f"接收到的响应: {response.text}")
        raise Exception(f"解析事件信息失败: API返回的不是有效的JSON")
    except Exception as e:
        logger.error(f"解析事件时发生错误: {str(e)}")
        raise Exception(f"解析事件信息失败: {str(e)}")

def generate_health_advice(events):
    model = genai.GenerativeModel('gemini-pro')
    events_text = "\n".join([f"- {event.title} 在 {event.event_time}" for event in events])
    prompt = f"""
    基于以下最近的活动，为老年人生成个性化的养生建议：
    {events_text}
    
    请提供3-5条简短、实用的建议，考虑到老年人的身心健康需求。
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"生成健康建议时发生错误: {str(e)}")
        raise Exception(f"生成健康建议失败: {str(e)}")