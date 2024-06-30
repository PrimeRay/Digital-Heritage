from flask import Blueprint, jsonify
from app.models.models import Event
from app.services.gemini_service import generate_health_advice
from datetime import datetime, timedelta

health_bp = Blueprint('health', __name__)

@health_bp.route('/health_advice', methods=['GET'])
def get_health_advice():
    # 获取过去一周的事件
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_events = Event.query.filter(Event.event_time >= one_week_ago).order_by(Event.event_time.desc()).all()
    
    advice = generate_health_advice(recent_events)
    
    return jsonify({
        "advice": advice,
        "events": [event.to_dict() for event in recent_events]
    })