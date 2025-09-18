# backend/app/tasks.py
from datetime import datetime
from .services.market_service import fetch_from_api, _deep_get
from .services.market_scrapers import scrape_agmarknet_example
from .models import MarketSource
from .extensions import db
from celery_app import celery

@celery.task(name="app.tasks.fetch_all_sources")
def fetch_all_sources():
    with celery.app.app_context():
        sources = MarketSource.query.filter_by(enabled=True).all()
        for s in sources:
            # logic: detect if s.url is API or HTML, or store a type field
            if "api" in (s.url or "") or s.url.endswith(".json"):
                # use stored config (you need a field to store JSON config in DB or a config file)
                api_config = {}  # load mapping from config
                fetch_from_api(s, api_config)
            else:
                # call scraper per site - choose appropriate function based on s.name
                if "agmarknet" in (s.name or "").lower():
                    scrape_agmarknet_example(s)
                else:
                    scrape_agmarknet_example(s)  # fallback
