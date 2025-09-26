from ..database import SessionLocal
from ..crud.crud import get_user_by_username, get_user_interactions, get_posts_by_ids, get_popular_posts, get_posts_by_topic_project_code
from ..models import Post, Interaction, Tag
from sqlalchemy.orm import Session
from typing import List
from collections import Counter
import numpy as np


def get_personalized_recommendations(username: str, limit: int = 20) -> List[int]:
    db = SessionLocal()
    try:
        user = get_user_by_username(db, username)
        if not user:
            # Cold start: return popular posts
            popular = get_popular_posts(db, limit)
            return [p.id for p in popular]

        interactions = get_user_interactions(db, user.id)
        if not interactions:
            # Cold start
            popular = get_popular_posts(db, limit)
            return [p.id for p in popular]

        # Get interacted posts
        interacted_posts = [inter.post_id for inter in interactions]

        # Find similar posts based on tags and category
        similar_posts = []
        for inter in interactions:
            post = db.query(Post).filter(Post.id == inter.post_id).first()
            if post:
                # Posts in same category
                category_posts = db.query(Post).filter(Post.category_id == post.category_id, Post.id != post.id).all()
                similar_posts.extend([p.id for p in category_posts])
                # Posts with same tags
                post_tags = [pt.tag.name for pt in post.tags]
                for tag_name in post_tags:
                    tag_posts = db.query(Post).join(Post.tags).filter(Tag.name == tag_name, Post.id != post.id).all()
                    similar_posts.extend([p.id for p in tag_posts])

        # Remove duplicates and exclude interacted
        similar_posts = list(set(similar_posts) - set(interacted_posts))

        # Combine with interacted (as similar) and limit
        recommended = list(set(similar_posts + interacted_posts))[:limit]

        # Fallback if not enough
        if len(recommended) < limit:
            popular = get_popular_posts(db, limit - len(recommended))
            recommended.extend([p.id for p in popular if p.id not in recommended])

        return recommended[:limit]
    finally:
        db.close()


def get_category_recommendations(username: str, project_code: str, limit: int = 20) -> List[int]:
    db = SessionLocal()
    try:
        # First get personalized, then filter by project_code
        personalized = get_personalized_recommendations(username, limit * 2)
        posts = get_posts_by_ids(db, personalized)
        filtered = [p.id for p in posts if p.topic and p.topic.project_code == project_code]
        if len(filtered) < limit:
            # Add more from project_code
            project_posts = get_posts_by_topic_project_code(db, project_code, limit - len(filtered))
            filtered.extend([p.id for p in project_posts])
        return filtered[:limit]
    finally:
        db.close()
