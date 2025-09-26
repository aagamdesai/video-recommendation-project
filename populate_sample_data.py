import sys
sys.path.append('app')

from app.database import SessionLocal, engine
from app.models import Base, User, Category, Topic, Post, Interaction, Tag, PostTag
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pydantic import BaseModel
from typing import List

# Create tables if not exist
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
db = Session()

# Sample data from task example
sample_user = {
    "first_name": "Sachin",
    "last_name": "Kinha",
    "name": "Sachin Kinha",
    "username": "sachin",
    "picture_url": "https://assets.socialverseapp.com/profile/19.png",
    "user_type": None,
    "has_evm_wallet": False,
    "has_solana_wallet": False
}

sample_category = {
    "id": 13,
    "name": "Flic",
    "count": 125,
    "description": "Where Creativity Meets Opportunity",
    "image_url": "https://socialverse-assets.s3.us-east-1.amazonaws.com/categories/NEW_COLOR.png"
}

sample_topic_owner = {
    "first_name": "Shivam",
    "last_name": "Flic",
    "name": "Shivam Flic",
    "username": "random",
    "picture_url": "https://assets.socialverseapp.com/profile/random1739306567image_cropper_1739306539349.jpg.png",
    "user_type": "hirer",
    "has_evm_wallet": False,
    "has_solana_wallet": False
}

sample_topic = {
    "id": 1,
    "name": "Social Media",
    "description": "Short form content making and editing.",
    "image_url": "https://ui-avatars.com/api/?size=300&name=Social%20Media&color=fff&background=random",
    "slug": "b9f5413f04ec58e47874",
    "is_public": True,
    "project_code": "flic",
    "posts_count": 18,
    "language": None,
    "created_at": datetime.now()
}

sample_post = {
    "id": 3104,
    "title": "testing-topic",
    "is_available_in_public_feed": True,
    "is_locked": False,
    "slug": "0dcff38b97c646a37ebcfa4f039c332812aa3857",
    "identifier": "QCp8ffL",
    "comment_count": 0,
    "upvote_count": 4,
    "view_count": 235,
    "exit_count": 149,
    "rating_count": 0,
    "average_rating": 84.0,
    "share_count": 0,
    "bookmark_count": 0,
    "video_link": "https://video-cdn.socialverseapp.com/sachin_d323e3b5-0012-4e55-85cc-b15dbe47a470.mp4",
    "thumbnail_url": "https://video-cdn.socialverseapp.com/sachin_d323e3b5-0012-4e55-85cc-b15dbe47a470.0000002.jpg",
    "gif_thumbnail_url": "https://video-cdn.socialverseapp.com/sachin_d323e3b5-0012-4e55-85cc-b15dbe47a470.gif",
    "contract_address": "",
    "chain_id": "",
    "chart_url": "",
    "created_at": datetime.now()
}

# Insert user
user = db.query(User).filter(User.username == "sachin").first()
if not user:
    user = User(**sample_user)
    db.add(user)
    db.commit()
    db.refresh(user)

# Insert category
category = db.query(Category).filter(Category.id == 13).first()
if not category:
    category = Category(**sample_category)
    db.add(category)
    db.commit()
    db.refresh(category)

# Insert topic owner
topic_owner = db.query(User).filter(User.username == "random").first()
if not topic_owner:
    topic_owner = User(**sample_topic_owner)
    db.add(topic_owner)
    db.commit()
    db.refresh(topic_owner)

# Insert topic
sample_topic["owner_id"] = topic_owner.id
topic = db.query(Topic).filter(Topic.id == 1).first()
if not topic:
    topic = Topic(**sample_topic)
    db.add(topic)
    db.commit()
    db.refresh(topic)

# Insert post
sample_post["owner_id"] = user.id
sample_post["category_id"] = category.id
sample_post["topic_id"] = topic.id
post = db.query(Post).filter(Post.id == 3104).first()
if not post:
    post = Post(**sample_post)
    db.add(post)
    db.commit()
    db.refresh(post)

# Insert tags and associations
tags_list = ["testing", "editing", "social-media"]
for tag_name in tags_list:
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    # Check if association exists
    existing = db.query(PostTag).filter(PostTag.post_id == post.id, PostTag.tag_id == tag.id).first()
    if not existing:
        post_tag = PostTag(post_id=post.id, tag_id=tag.id)
        db.add(post_tag)
        db.commit()

# Insert sample interaction for user
interaction = db.query(Interaction).filter(Interaction.user_id == user.id, Interaction.post_id == post.id).first()
if not interaction:
    interaction = Interaction(user_id=user.id, post_id=post.id, interaction_type="view", created_at=datetime.now())
    db.add(interaction)
    db.commit()

# Insert another popular post for cold start testing
popular_post_data = {
    "id": 3105,
    "title": "Popular Video",
    "is_available_in_public_feed": True,
    "is_locked": False,
    "slug": "popular-slug",
    "identifier": "POP123",
    "comment_count": 0,
    "upvote_count": 500,
    "view_count": 1000,
    "exit_count": 0,
    "rating_count": 0,
    "average_rating": 90.0,
    "share_count": 0,
    "bookmark_count": 0,
    "video_link": "https://example.com/popular.mp4",
    "thumbnail_url": "https://example.com/popular.jpg",
    "gif_thumbnail_url": "https://example.com/popular.gif",
    "contract_address": "",
    "chain_id": "",
    "chart_url": "",
    "created_at": datetime.now(),
    "owner_id": user.id,
    "category_id": category.id,
    "topic_id": topic.id
}
popular_post = db.query(Post).filter(Post.id == 3105).first()
if not popular_post:
    popular_post = Post(**popular_post_data)
    db.add(popular_post)
    db.commit()
    db.refresh(popular_post)

print("Sample data populated successfully.")

db.close()
