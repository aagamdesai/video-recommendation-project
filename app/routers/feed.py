
from fastapi import APIRouter, HTTPException, Query
from ..services.recommendation import get_personalized_recommendations, get_category_recommendations
from ..crud.crud import get_posts_by_ids, get_user_by_username, has_user_interaction
from ..database import SessionLocal
from ..schemas import FeedResponse, PostBase
from sqlalchemy.orm import Session
from typing import Optional


router = APIRouter()


def post_to_schema(db: Session, db_post, user_id: Optional[int] = None) -> PostBase:
    # Convert SQLAlchemy model to Pydantic schema
    owner = {
        "first_name": db_post.owner.first_name,
        "last_name": db_post.owner.last_name,
        "name": db_post.owner.name,
        "username": db_post.owner.username,
        "picture_url": db_post.owner.picture_url,
        "user_type": db_post.owner.user_type,
        "has_evm_wallet": db_post.owner.has_evm_wallet,
        "has_solana_wallet": db_post.owner.has_solana_wallet,
    }
    category = {
        "id": db_post.category.id,
        "name": db_post.category.name,
        "count": db_post.category.count,
        "description": db_post.category.description,
        "image_url": db_post.category.image_url,
    }
    topic_owner = {
        "first_name": db_post.topic.owner.first_name,
        "last_name": db_post.topic.owner.last_name,
        "name": db_post.topic.owner.name,
        "username": db_post.topic.owner.username,
        "profile_url": db_post.topic.owner.picture_url,  # Assuming picture_url as profile_url
        "user_type": db_post.topic.owner.user_type,
        "has_evm_wallet": db_post.topic.owner.has_evm_wallet,
        "has_solana_wallet": db_post.topic.owner.has_solana_wallet,
    }
    topic = {
        "id": db_post.topic.id,
        "name": db_post.topic.name,
        "description": db_post.topic.description,
        "image_url": db_post.topic.image_url,
        "slug": db_post.topic.slug,
        "is_public": db_post.topic.is_public,
        "project_code": db_post.topic.project_code,
        "posts_count": db_post.topic.posts_count,
        "language": db_post.topic.language,
        "created_at": db_post.topic.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "owner": topic_owner,
    }
    base_token = {
        "address": db_post.baseToken.address or "" if db_post.baseToken else "",
        "name": db_post.baseToken.name or "" if db_post.baseToken else "",
        "symbol": db_post.baseToken.symbol or "" if db_post.baseToken else "",
        "image_url": db_post.baseToken.image_url or "" if db_post.baseToken else "",
    }
    tags = [tag.name for tag in db_post.tags]

    upvoted = has_user_interaction(db, user_id, db_post.id, 'like') if user_id else False
    bookmarked = has_user_interaction(db, user_id, db_post.id, 'inspire') if user_id else False
    following = False

    post = PostBase(
        id=db_post.id,
        owner=owner,
        category=category,
        topic=topic,
        title=db_post.title,
        is_available_in_public_feed=db_post.is_available_in_public_feed,
        is_locked=db_post.is_locked,
        slug=db_post.slug,
        upvoted=upvoted,
        bookmarked=bookmarked,
        following=following,
        identifier=db_post.identifier,
        comment_count=db_post.comment_count,
        upvote_count=db_post.upvote_count,
        view_count=db_post.view_count,
        exit_count=db_post.exit_count,
        rating_count=db_post.rating_count,
        average_rating=int(db_post.average_rating),
        share_count=db_post.share_count,
        bookmark_count=db_post.bookmark_count,
        video_link=db_post.video_link,
        thumbnail_url=db_post.thumbnail_url,
        gif_thumbnail_url=db_post.gif_thumbnail_url,
        contract_address=db_post.contract_address or "",
        chain_id=db_post.chain_id or "",
        chart_url=db_post.chart_url or "",
        baseToken=base_token,
        created_at=int(db_post.created_at.timestamp() * 1000),  # to ms
        tags=tags,
    )
    return post


@router.get("/feed", response_model=FeedResponse)
def get_feed(
    username: str = Query(..., description="Username for personalized recommendations"),
    project_code: Optional[str] = Query(None, description="Project code for category-based recommendations")
):
    db = SessionLocal()
    try:
        if project_code:
            post_ids = get_category_recommendations(username, project_code)
        else:
            post_ids = get_personalized_recommendations(username)

        user = get_user_by_username(db, username)

        posts = get_posts_by_ids(db, post_ids)
        post_schemas = [post_to_schema(db, p, user.id if user else None) for p in posts]
        return FeedResponse(post=post_schemas, status="True")
    except Exception as e:
        return FeedResponse(status="False", post=[])
    finally:
        db.close()
