from app import db, models
from sqlalchemy.orm import aliased
import random

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

def get_mutual_likes(user1, user2):
    # get all unique likes for each user
    liked_posts_user1 = set([like.post_id for like in user1.likes])
    liked_posts_user2 = set([like.post_id for like in user2.likes])
    
    # find intersection and return how many there are
    mutual_likes = liked_posts_user1.intersection(liked_posts_user2)
    return len(mutual_likes)

def get_recommendations(user):
    # get all posts
    all_posts = get_posts(user).all()
    recommendations = []

    for post, liked in all_posts:
        # dont recommend the user their own posts or ones they have already liked
        if post.user_id == user.id or liked:
            continue

        # get all users who liked the post
        users_who_liked = [like.user for like in post.likes]

        mutual_likes = 0

        # get mutual likes with each user who liked the post
        for other_user in users_who_liked:
            mutual_likes_count = get_mutual_likes(user, other_user)
            mutual_likes += mutual_likes_count
        
        # add a random factor so that the recommendations are not always the same
        random_factor = random.uniform(0.7, 1.4)
        score = mutual_likes * random_factor

        recommendations.append((post, liked, score))

    # sort the recommendations by score
    recommendations.sort(key=lambda x: x[2], reverse=True)

    # return the top 10 recommendations
    return [(post, liked) for post, liked, score in recommendations[:10]]




