# TODO List for Video Recommendation Engine

Based on the comprehensive plan, here are the logical steps to complete the project:

## Setup and Configuration
- [x] 1. Create requirements.txt with necessary dependencies (FastAPI, Uvicorn, SQLAlchemy, Alembic, httpx, python-dotenv, pydantic).
- [x] 2. Create .env file template with FLIC_TOKEN and API_BASE_URL.
- [x] 3. Set up Alembic configuration (alembic.ini and env.py).

## Core App Structure
- [x] 4. Create app/config.py for settings and environment loading.
- [x] 5. Create app/database.py for SQLAlchemy engine and session management (using SQLite).
- [x] 6. Create app/models.py with SQLAlchemy models for User, Post, Category, Topic, Interaction (views, likes, inspires, ratings).
- [x] 7. Create app/schemas.py with Pydantic schemas matching the output-data-format.md structure for Post responses.

## Data and Services
- [x] 8. Create app/crud/ directory with __init__.py and basic CRUD operations for models (e.g., create_post, get_user_interactions).
- [x] 9. Create app/services/data_collection.py to fetch data from external APIs (viewed, liked, inspired, rated posts; all posts; all users) using httpx with Flic-Token, and store in DB.
- [x] 10. Create app/services/recommendation.py with basic recommendation logic:
  - Personalized: Content-based filtering using user's interactions (similar posts by category/topic/tags).
  - Category-based: Filter by project_code.
  - Cold start: Recommend top popular posts (high view/upvote) or mood-based (category as mood proxy).
  - Limit to 10-20 items with pagination support.

## API and Main App
- [x] 11. Create app/routers/feed.py with GET /feed endpoints for personalized and category-based feeds, returning {"status": "True", "post": [posts]} format.
- [x] 12. Create app/main.py to initialize FastAPI app, include routers, CORS, and startup event to populate initial data if needed.
- [x] 13. Generate initial Alembic migration (alembic revision --autogenerate -m "initial") and update versions/ directory.

## Finalization
- [x] 14. Implement error handling (e.g., HTTPExceptions for invalid username/project_code) and basic logging in main.py.
- [x] 15. Test setup: Run migrations, start server, verify endpoints (manual via tools later).
- [x] 16. Create docs/ folder with explanation.md on how the recommendation system works.
- [x] 17. Update README.md if needed for any clarifications.
- [x] 18. Create data collection endpoints for internal use: /posts/view, /posts/like, /posts/inspire, /posts/rating, /posts/summary/get, /users/get_all.

Progress will be updated by checking off completed steps after each major file creation or tool use.
