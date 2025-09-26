from ..database import SessionLocal
from ..crud.crud import get_user_by_username, get_user_interactions, get_posts_by_ids, get_popular_posts, get_posts_by_topic_project_code
from ..models import Post, Interaction, Tag
from sqlalchemy.orm import Session
from typing import List
import torch
import torch.nn as nn
import networkx as nx
from collections import Counter
import numpy as np


class SimpleNCF(nn.Module):
    def __init__(self, num_users, num_items, embedding_dim=64):
        super(SimpleNCF, self).__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.item_embedding = nn.Embedding(num_items, embedding_dim)
        self.fc_layers = nn.Sequential(
            nn.Linear(embedding_dim * 2, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, user_ids, item_ids):
        user_emb = self.user_embedding(user_ids)
        item_emb = self.item_embedding(item_ids)
        concat = torch.cat([user_emb, item_emb], dim=1)
        return self.fc_layers(concat)


# Pre-compute model (simple, no training for demo)
def build_recommendation_model(db: Session):
    # Get all users and posts
    users = db.query(Interaction.user_id).distinct().all()
    posts = db.query(Post.id).all()
    num_users = max(len(users), 1)  # Avoid zero
    num_items = max(len(posts), 1)
    
    model = SimpleNCF(num_users, num_items)
    # For demo, use random weights
    # In production, train on interactions
    user_map = {u[0]: i for i, u in enumerate(users)} if users else {}
    post_map = {p[0]: i for i, p in enumerate(posts)} if posts else {}
    post_map_inv = {v: k for k, v in post_map.items()}
    return model, user_map, post_map, post_map_inv


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

        # Build graph for GNN-like analysis (user-post bipartite graph)
        G = nx.Graph()
        for inter in interactions:
            G.add_edge(user.id, inter.post_id, weight=1.0)

        # Get interacted posts as base recommendations
        interacted_posts = [inter.post_id for inter in interactions]
        similar_posts = interacted_posts[:]

        # Neural component: Simple embedding similarity
        model, user_map, post_map, post_map_inv = build_recommendation_model(db)
        user_idx = user_map.get(user.id, 0)
        all_posts = db.query(Post.id).all()
        post_ids = [p.id for p in all_posts]
        post_idxs = [post_map.get(pid, 0) for pid in post_ids]
        
        # Compute scores for all posts
        user_tensor = torch.tensor([user_idx])
        scores = []
        for i, p_idx in enumerate(post_idxs):
            item_tensor = torch.tensor([p_idx])
            score = model(user_tensor, item_tensor).item()
            scores.append((post_ids[i], score))
        
        # Sort by score, exclude already interacted
        nn_recs = [s[0] for s in sorted(scores, key=lambda x: x[1], reverse=True) if s[0] not in interacted_posts][:limit//2]
        
        # Combine NN and graph-based (interacted as similar)
        recommended = list(set(nn_recs + similar_posts))[:limit]

        # Fallback if not enough
        if len(recommended) < limit:
            popular = get_popular_posts(db, limit - len(recommended))
            recommended.extend([p.id for p in popular])

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
