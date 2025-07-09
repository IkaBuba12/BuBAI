from ext import app, db
from models import User

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Created new tables in database.db")

    with app.app_context():
        user = User.query.filter_by(email="gigitskipurishvili@gmail.com").first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print("User deleted successfully.")
        else:
            print("User not found.")


