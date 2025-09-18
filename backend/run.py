from app import create_app
from app.extensions import db
from app.models import CropPlan

app = create_app()

# optional: create DB tables in dev
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
