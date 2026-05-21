from services.ugc.app import create_app
from services.ugc.models import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8001, debug=True)
