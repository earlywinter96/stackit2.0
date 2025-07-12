from app import create_app
from app.extensions import db
from sqlalchemy import inspect

print("🟡 Starting DB setup...")

app = create_app()
with app.app_context():
    print("🔄 Creating tables...")
    db.create_all()

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    print("📋 Tables created in PostgreSQL:")
    for t in tables:
        print(f" - {t}")

    print("✅ Done.")
