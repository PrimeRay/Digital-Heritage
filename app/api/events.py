from flask import Blueprint, request, jsonify
from app.models.models import Event, db
from app.services.gemini_service import parse_event_from_text
from datetime import datetime
import logging

events_bp = Blueprint('events', __name__)
logger = logging.getLogger(__name__)

@events_bp.route('/events', methods=['POST'])
def create_event():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    logger.info(f"Received event text: {text}")
    try:
        event_data = parse_event_from_text(text)
        logger.info(f"Parsed event data: {event_data}")
        
        new_event = Event(
            title=event_data.get('title', '未命名事件'),
            location=event_data.get('location'),
            companions=event_data.get('companions'),
            event_time=event_data.get('event_time', datetime.now())
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        return jsonify({"message": "事件已记录", "event": new_event.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"创建事件时发生错误: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@events_bp.route('/events', methods=['GET'])
def get_events():
    try:
        events = Event.query.order_by(Event.event_time.desc()).all()
        return jsonify([event.to_dict() for event in events])
    except Exception as e:
        logger.error(f"获取事件时发生错误: {str(e)}")
        return jsonify({"error": str(e)}), 500