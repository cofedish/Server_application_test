from app import create_app, db
from app.models import User
from app.utils import generate_password_hash

app = create_app()

with app.app_context():
    # Создание администратора
    admin = User(username='admin', password_hash=generate_password_hash('admin'), is_admin=True)
    db.session.add(admin)
    db.session.commit()
    print("Admin user created")
