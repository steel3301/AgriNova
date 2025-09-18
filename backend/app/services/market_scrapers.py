# backend/app/services/market_scrapers.py
import requests, logging
from bs4 import BeautifulSoup
from datetime import date, datetime
from ..extensions import db
from ..models import MarketSource, MarketPrice

logger = logging.getLogger(__name__)

def scrape_agmarknet_example(source: MarketSource):
    """
    Example scraper for a simple HTML table site.
    Adjust selectors to the real site.
    """
    try:
        r = requests.get(source.url, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # find table rows - adjust CSS selectors depending on the actual site
        table = soup.select_one("table#priceTable")  # example
        if not table:
            logger.warning("No price table found for %s", source.url)
            return
        rows = table.select("tr")[1:]  # skip header
        for tr in rows:
            cols = [td.get_text(strip=True) for td in tr.select("td")]
            # Example columns: [date, commodity, variety, market, price, unit]
            if len(cols) < 5:
                continue
            date_str = cols[0]
            try:
                d = datetime.strptime(date_str, "%d-%m-%Y").date()
            except Exception:
                d = date.today()
            crop = cols[1]
            price = float(cols[4].replace(",", ""))
            unit = cols[5] if len(cols) > 5 else "kg"
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
        logger.exception("Scrape failed: %s", e)
