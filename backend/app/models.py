from .extensions import db
from datetime import datetime

class CropPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(128), nullable=False)
    sow_date = db.Column(db.Date, nullable=False)
    harvest_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MarketSource(db.Model):
    __tablename__ = "market_sources"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    url = db.Column(db.String(1000))
    region = db.Column(db.String(200), nullable=True)
    last_synced = db.Column(db.DateTime)
    enabled = db.Column(db.Boolean, default=True)

class MarketPrice(db.Model):
    __tablename__ = "market_prices"
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey("market_sources.id"), nullable=True)
    crop = db.Column(db.String(200), nullable=False, index=True)
    variety = db.Column(db.String(200), nullable=True)
    unit = db.Column(db.String(50), nullable=True)  # e.g., 'kg', 'quintal'
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)  # date of price
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    source = db.relationship("MarketSource", backref="prices")

