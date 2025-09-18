from flask import Blueprint, request, jsonify, current_app
from ..extensions import db
from ..models import CropPlan, MarketPrice
from ..services.ai_service import ask_ai
from ..services.market_service import get_price_trends
from datetime import datetime, timedelta
api_bp = Blueprint('api', __name__)
import requests
from sqlalchemy import func


CROP_PLANS = {
    "Wheat": [
        ("Sowing", 0),
        ("First Irrigation", 20),
        ("Fertilizer (Urea)", 30),
        ("Second Irrigation", 40),
        ("Weeding", 50),
        ("Pesticide Spray", 70),
        ("Harvesting", 120),
    ],
    "Rice": [
        ("Nursery Preparation", 0),
        ("Transplanting", 20),
        ("First Fertilizer Dose", 30),
        ("Irrigation", 40),
        ("Weeding", 60),
        ("Second Fertilizer Dose", 70),
        ("Harvesting", 150),
    ],
    "Maize": [
        ("Sowing", 0),
        ("First Irrigation", 15),
        ("Fertilizer (DAP)", 20),
        ("Second Irrigation", 30),
        ("Pesticide Spray", 45),
        ("Harvesting", 100),
    ]
}

@api_bp.route('/crop-schedule', methods=['POST'])
def crop_schedule():
    data = request.json
    crop = data.get("crop")
    sow_date_str = data.get("sow_date")

    if crop not in CROP_PLANS:
        return jsonify({"ok": False, "error": "Invalid crop"}), 400

    try:
        sow_date = datetime.fromisoformat(sow_date_str).date()
    except Exception:
        return jsonify({"ok": False, "error": "Invalid sow_date"}), 400

    plan = CROP_PLANS[crop]
    schedule = []
    for activity, offset in plan:
        activity_date = sow_date + timedelta(days=offset)
        schedule.append({"task": activity, "date": activity_date.isoformat()})

    return jsonify({"ok": True, "schedule": schedule})

@api_bp.route('/ai/query', methods=['POST'])
def ai_query():
    payload = request.json or {}
    text = payload.get('text')
    image_data = payload.get('image')  # base64 optional
    if not text and not image_data:
        return jsonify({'error': 'text or image required'}), 400
    try:
        response = ask_ai(text=text, image_base64=image_data)
        return jsonify({'ok': True, 'response': response})
    except Exception as e:
        current_app.logger.exception('AI query failed')
        return jsonify({'ok': False, 'error': str(e)}), 500

@api_bp.route('/crops', methods=['POST'])
def crops():
    """
    AI-powered crop planning.
    Accepts:
    {
        "query": "Create a farming plan for rice in monsoon season"
    }
    Returns AI-generated schedule:
    [
        {"date": "YYYY-MM-DD", "event": "Activity", "reason": "...", "significance": "..."},
        ...
    ]
    """
    data = request.json or {}
    query_text = data.get("query")
    if not query_text:
        return jsonify({'error': 'query text required'}), 400

    # Optional: pass a format spec to AI
    format_spec = data.get("format_spec") or (
        "Return JSON array in the format: "
        '[{"date": "YYYY-MM-DD", "event": "Activity", "reason": "Why this task", "significance": "Importance of this event"}]'
    )

    ai_prompt = f"{query_text}\n{format_spec}"

    try:
        response = ask_ai(text=ai_prompt)
        ai_schedule = response.get("text", "[]")

        print(ai_schedule)
        
        # Convert AI string response to Python list
        import json
        try:
            schedule_list = json.loads(ai_schedule)
        except Exception:
            return jsonify({'ok': False, 'error': 'Invalid AI JSON response'}), 500

        # Optional: store in DB
        saved_plans = []
        for step in schedule_list:
            plan = CropPlan(
                crop_name=data.get("crop_name", "AI_Crop"),
                sow_date=step.get("date"),
                harvest_date=step.get("date"),
                notes=f"{step.get('event')} - {step.get('reason')} - {step.get('significance')}"
            )
            db.session.add(plan)
            db.session.flush()
            saved_plans.append({
                "id": plan.id,
                "date": step.get("date"),
                "event": step.get("event"),
                "reason": step.get("reason"),
                "significance": step.get("significance")
            })
        db.session.commit()

        return jsonify({'ok': True, 'schedule': saved_plans})

    except Exception as e:
        current_app.logger.exception("Crop planning failed")
        return jsonify({'ok': False, 'error': str(e)}), 500

@api_bp.route('/market/trends', methods=['GET'])
def market_trends():
    crop = request.args.get('crop', 'rice')
    days = int(request.args.get('days', 90))
    try:
        chart = get_price_trends(crop=crop, days=days)
        return jsonify({'ok': True, 'data': chart})
    except Exception as e:
        current_app.logger.exception('market trends failed')
        return jsonify({'ok': False, 'error': str(e)}), 500



@api_bp.route("/market/latest", methods=["GET"])
def market_latest():
    """
    Query params:
      crop (optional)
      region (optional)  -- filter later if region stored
    Returns: latest price per source for crop(s)
    """
    crop = request.args.get("crop")
    q = db.session.query(
        MarketPrice.crop,
        func.avg(MarketPrice.price).label("avg_price"),
        func.min(MarketPrice.price).label("min_price"),
        func.max(MarketPrice.price).label("max_price"),
        MarketPrice.date
    )
    if crop:
        q = q.filter(MarketPrice.crop.ilike(f"%{crop}%"))
    q = q.group_by(MarketPrice.crop, MarketPrice.date).order_by(MarketPrice.date.desc()).limit(100)
    rows = q.all()
    result = [{"crop": r.crop, "avg_price": r.avg_price, "min_price": r.min_price, "max_price": r.max_price, "date": r.date.isoformat()} for r in rows]
    return jsonify({"ok": True, "data": result})

@api_bp.route("/market/history", methods=["GET"])
def market_history():
    """
    Params: crop (required), days (optional)
    Returns time series of prices for the given crop.
    """
    crop = request.args.get("crop")
    days = int(request.args.get("days", 90))
    if not crop:
        return jsonify({"ok": False, "error": "crop required"}), 400
    from datetime import date, timedelta
    since = date.today() - timedelta(days=days)
    rows = MarketPrice.query.filter(MarketPrice.crop.ilike(f"%{crop}%"), MarketPrice.date >= since).order_by(MarketPrice.date).all()
    data = [{"date": r.date.isoformat(), "price": r.price, "source": r.source.name if r.source else None} for r in rows]
    return jsonify({"ok": True, "data": data})
