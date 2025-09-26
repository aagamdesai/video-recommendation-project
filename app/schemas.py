from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    username: str
    picture_url: Optional[str] = None
    user_type: Optional[str] = None
    has_evm_wallet: bool = False
    has_solana_wallet: bool = False


class CategoryBase(BaseModel):
    id: int
    name: str
    count: int
    description: Optional[str] = None
    image_url: Optional[str] = None


class TopicOwner(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    username: str
    profile_url: Optional[str] = None
    user_type: Optional[str] = None
    has_evm_wallet: bool = False
    has_solana_wallet: bool = False


class TopicBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    slug: str
    is_public: bool
    project_code: str
    posts_count: int
    language: Optional[str] = None
    created_at: str
    owner: TopicOwner


class BaseTokenBase(BaseModel):
    address: str = ""
    name: str = ""
    symbol: str = ""
    image_url: str = ""


class PostBase(BaseModel):
    id: int
    owner: UserBase
    category: CategoryBase
    topic: TopicBase
    title: str
    is_available_in_public_feed: bool
    is_locked: bool
    slug: str
    upvoted: bool = False  # Assuming not implemented yet
    bookmarked: bool = False
    following: bool = False
    identifier: str
    comment_count: int
    upvote_count: int
    view_count: int
    exit_count: int
    rating_count: int
    average_rating: int
    share_count: int
    bookmark_count: int
    video_link: str
    thumbnail_url: Optional[str] = None
    gif_thumbnail_url: Optional[str] = None
    contract_address: str = ""
    chain_id: str = ""
    chart_url: str = ""
    baseToken: BaseTokenBase
    created_at: int  # timestamp in ms
    tags: List[str]


class FeedResponse(BaseModel):
    status: str = "success"
    post: List[PostBase]
