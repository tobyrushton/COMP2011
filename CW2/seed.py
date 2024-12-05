import random
from faker import Faker
from app import db, models, app

fake = Faker()


with app.app_context():
    # delete all the data in the database
    modelsList = [models.User, models.Post, models.Like]
    for model in modelsList:
        db.session.query(model).delete()
    db.session.commit()
    
    users = []
    posts = []
    # create 100 fake users for the project
    for i in range(100):
        user = models.User(username=fake.user_name(), password_hash=fake.password())
        users.append(user)

        db.session.add(user)
        db.session.commit()

        # create 20 posts for each user
        for i in range(20):
            post = models.Post(body=fake.text(), user=user)
            posts.append(post)
            db.session.add(post)
            db.session.commit()
        
    
    # create 1000 fake likes for the project
    for i in range(1000):
        user = random.choice(users)
        post = random.choice(posts)
        like = models.Like(user=user, post=post)
        db.session.add(like)
        db.session.commit()
