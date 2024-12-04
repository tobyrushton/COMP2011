from faker import Faker
from app import db, models, app

fake = Faker()

with app.app_context():
    # create 100 fake users for the project
    for i in range(100):
        user = models.User(username=fake.user_name(), password_hash=fake.password())
        db.session.add(user)
        db.session.commit()

        # create 20 posts for each user
        for i in range(20):
            post = models.Post(body=fake.text(), user=user)
            db.session.add(post)
            db.session.commit()
