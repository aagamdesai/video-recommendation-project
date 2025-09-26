import httpx
from ..config import settings
from ..database import SessionLocal
from ..crud.crud import create_user, create_post, create_interaction
from ..models import User, Post, Category, Topic, Tag, BaseToken
from sqlalchemy.orm import Session
import asyncio


HEADERS = {"Flic-Token": settings.flic_token}


async def fetch_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()


def store_users(db: Session, users_data):
    for user_data in users_data:
        if not db.query(User).filter(User.username == user_data["username"]).first():
            create_user(db, user_data)


def store_posts(db: Session, posts_data):
    for post_data in posts_data:
        # Store owner if not exists
        owner_data = post_data["owner"]
        owner = db.query(User).filter(User.username == owner_data["username"]).first()
        if not owner:
            owner = create_user(db, owner_data)
        post_data["owner_id"] = owner.id

        # Store category
        cat_data = post_data["category"]
        category = db.query(Category).filter(Category.id == cat_data["id"]).first()
        if not category:
            category = Category(**cat_data)
            db.add(category)
            db.commit()
        post_data["category_id"] = category.id

        # Store topic
        topic_data = post_data["topic"]
        topic_owner_data = topic_data.pop("owner")
        topic_owner = db.query(User).filter(User.username == topic_owner_data["username"]).first()
        if not topic_owner:
            topic_owner = create_user(db, topic_owner_data)
        topic_data["owner_id"] = topic_owner.id
        topic = db.query(Topic).filter(Topic.id == topic_data["id"]).first()
        if not topic:
            topic = Topic(**topic_data)
            db.add(topic)
            db.commit()
        post_data["topic_id"] = topic.id

        # Handle tags
        tags = post_data.pop("tags", [])
        post = create_post(db, post_data)
        for tag_name in tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
            # Associate tag with post (assuming PostTag table)
            from ..models import PostTag
            post_tag = PostTag(post_id=post.id, tag_id=tag.id)
            db.add(post_tag)
        db.commit()

        # Store baseToken if present
        base_token_data = post_data.get("baseToken", {})
        if base_token_data.get("address"):
            base_token = BaseToken(post_id=post.id, **base_token_data)
            db.add(base_token)
        db.commit()


def store_interactions(db: Session, interactions_data, interaction_type: str):
    for post_data in interactions_data:
        post_id = post_data["id"]
        # Assuming interactions are for a specific user, but since API doesn't specify user, perhaps store as anonymous or skip
        # For now, skip interactions without user context
        pass  # TODO: Implement based on how interactions are fetched


async def collect_all_data():
    if not settings.flic_token:
        print("Skipping data collection due to missing FLIC_TOKEN.")
        return

    db = SessionLocal()
    try:
        # Fetch all users
        users_url = f"{settings.api_base_url}/users/get_all?page=1&page_size=1000"
        users_response = await fetch_data(users_url)
        if users_response.get("status") == "success":
            store_users(db, users_response.get("users", []))

        # Fetch all posts
        posts_url = f"{settings.api_base_url}/posts/summary/get?page=1&page_size=1000"
        posts_response = await fetch_data(posts_url)
        if posts_response.get("status") == "success":
            store_posts(db, posts_response.get("post", []))

        # Fetch interactions (viewed, liked, etc.)
        # Note: These APIs return posts, but to associate with users, might need different approach
        # For simplicity, fetch and store posts if not already
        interaction_urls = [
            f"{settings.api_base_url}/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
            f"{settings.api_base_url}/posts/like?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
            f"{settings.api_base_url}/posts/inspire?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
            f"{settings.api_base_url}/posts/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if"
        ]
        interaction_types = ["view", "like", "inspire", "rating"]
        for url, itype in zip(interaction_urls, interaction_types):
            try:
                response = await fetch_data(url)
                if response.get("status") == "success":
                    posts = response.get("post", [])
                    store_posts(db, posts)  # Store posts if new
                    # For interactions, since no user specified, perhaps store as general popularity
            except Exception as e:
                print(f"Error fetching {itype}: {e}")

    finally:
        db.close()


# Function to run data collection
def run_data_collection():
    asyncio.run(collect_all_data())
