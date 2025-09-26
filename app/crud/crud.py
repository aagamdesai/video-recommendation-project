from sqlalchemy.orm import Session
from ..models import User, Post, Interaction, Category, Topic
from typing import List


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_posts_by_ids(db: Session, post_ids: List[int]):
    return db.query(Post).filter(Post.id.in_(post_ids)).all()


def get_all_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


def get_user_interactions(db: Session, user_id: int):
    return db.query(Interaction).filter(Interaction.user_id == user_id).all()


def get_popular_posts(db: Session, limit: int = 20):
    return db.query(Post).order_by(Post.view_count.desc()).limit(limit).all()


def get_posts_by_category(db: Session, category_id: int, limit: int = 20):
    return db.query(Post).filter(Post.category_id == category_id).order_by(Post.view_count.desc()).limit(limit).all()


def get_posts_by_topic_project_code(db: Session, project_code: str, limit: int = 20):
    return db.query(Post).join(Topic).filter(Topic.project_code == project_code).order_by(Post.view_count.desc()).limit(limit).all()


def create_user(db: Session, user_data):
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_post(db: Session, post_data):
    db_post = Post(**post_data)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def create_interaction(db: Session, interaction_data):
    db_interaction = Interaction(**interaction_data)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


def has_user_interaction(db: Session, user_id: int, post_id: int, interaction_type: str) -> bool:
    return db.query(Interaction).filter(
        Interaction.user_id == user_id,
        Interaction.post_id == post_id,
        Interaction.interaction_type == interaction_type
    ).first() is not None
