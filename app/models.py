from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    name = Column(String, nullable=True)
    username = Column(String, unique=True, index=True)
    picture_url = Column(String, nullable=True)
    user_type = Column(String, nullable=True)
    has_evm_wallet = Column(Boolean, default=False)
    has_solana_wallet = Column(Boolean, default=False)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    count = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    slug = Column(String, unique=True, index=True)
    is_public = Column(Boolean, default=True)
    project_code = Column(String, index=True)
    posts_count = Column(Integer, default=0)
    language = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    title = Column(String)
    is_available_in_public_feed = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    slug = Column(String, unique=True, index=True)
    identifier = Column(String, unique=True, index=True)
    comment_count = Column(Integer, default=0)
    upvote_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    exit_count = Column(Integer, default=0)
    rating_count = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    share_count = Column(Integer, default=0)
    bookmark_count = Column(Integer, default=0)
    video_link = Column(String)
    thumbnail_url = Column(String, nullable=True)
    gif_thumbnail_url = Column(String, nullable=True)
    contract_address = Column(String, nullable=True)
    chain_id = Column(String, nullable=True)
    chart_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    owner = relationship("User")
    category = relationship("Category")
    topic = relationship("Topic")
    tags = relationship("Tag", secondary="post_tags")
    interactions = relationship("Interaction", back_populates="post")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class PostTag(Base):
    __tablename__ = "post_tags"

    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    interaction_type = Column(String)  # 'view', 'like', 'inspire', 'rating'
    rating_value = Column(Float, nullable=True)  # for ratings
    created_at = Column(DateTime, default=func.now())

    user = relationship("User")
    post = relationship("Post", back_populates="interactions")


class BaseToken(Base):
    __tablename__ = "base_tokens"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    address = Column(String, nullable=True)
    name = Column(String, nullable=True)
    symbol = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    post = relationship("Post")
