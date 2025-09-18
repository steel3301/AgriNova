import random
import os
import requests
import logging
from ..extensions import db
from ..models import MarketSource, MarketPrice
from datetime import date, datetime, timedelta

def get_price_trends(crop='rice', days=90):
    """
    Placeholder: returns a list of {date: 'YYYY-MM-DD', price: float}
    Replace with live data source (APIs, scraped datasets, or database).
    """
    today = datetime.utcnow().date()
    data = []
    price = 100.0 + random.uniform(-5, 5)
    for i in range(days, 0, -1):
        d = today - timedelta(days=i)
        # simulate small random walk
        price += random.uniform(-1, 1)
        data.append({'date': d.isoformat(), 'price': round(price, 2)})
    return data

logger = logging.getLogger(__name__)

def fetch_from_api(source: MarketSource, api_config: dict):
    """
    api_config example:
    {
      "type": "json",
      "url": "https://example.gov/api/prices",
      "mapping": {
         "items_path": "data.prices",  # dot path to items
         "crop_field": "crop_name",
         "price_field": "price",
         "unit_field": "unit",
         "date_field": "date"  # or None => today
      }
    }
    """
    try:
        r = requests.get(api_config["url"], timeout=15)
        r.raise_for_status()
        payload = r.json()
        # simple dot-path resolver
        items = _deep_get(payload, api_config["mapping"].get("items_path")) or []
        for item in items:
            crop = item.get(api_config["mapping"]["crop_field"])
            price = float(item.get(api_config["mapping"]["price_field"]))
            unit = item.get(api_config["mapping"].get("unit_field", "")) or ""
            date_str = item.get(api_config["mapping"].get("date_field"))
            if date_str:
                d = date.fromisoformat(date_str)
            else:
                d = date.today()
            # persist
            rec = MarketPrice(
                source_id=source.id,
                crop=crop,
                variety=None,
                unit=unit,
                price=price,
                date=d
            )
            db.session.add(rec)
        source.last_synced = datetime.utcnow()
        db.session.commit()
    except Exception as e:
        logger.exception("API fetch failed: %s", e)

def _deep_get(obj, path):
    if not path:
        return obj
    parts = path.split(".")
    cur = obj
    for p in parts:
        if isinstance(cur, dict):
            cur = cur.get(p)
        else:
            return None
    return cur
