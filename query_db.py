import sys
sys.path.append('app')

from app.database import engine
from app.models import Base, User, Post, Category, Topic, Interaction
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
db = Session()

print("DB Counts:")
print(f"Users: {db.query(User).count()}")
print(f"Posts: {db.query(Post).count()}")
print(f"Categories: {db.query(Category).count()}")
print(f"Topics: {db.query(Topic).count()}")
print(f"Interactions: {db.query(Interaction).count()}")

# Print sample posts
posts = db.query(Post).all()
for p in posts:
    print(f"Post ID: {p.id}, Title: {p.title}, Views: {p.view_count}")

db.close()
