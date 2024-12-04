from app import db, models
from sqlalchemy.orm import aliased

# returns the builder to get posts, just add filter
def get_posts(user):
    liked_posts = aliased(models.Like)

    # this returns a builder to get posts that will return a list of tuples with the post and a boolean
    return db.session.query(models.Post,
                            db.case(
                                    (liked_posts.user_id == user.id, True),
                                    else_=False
                            ).label('liked_by_user')
                            ) \
                .join(liked_posts, liked_posts.post_id == models.Post.id, isouter=True)