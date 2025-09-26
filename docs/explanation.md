# Video Recommendation Engine - How It Works

## Overview
This Video Recommendation Engine is built using FastAPI and provides personalized video content recommendations based on user preferences and engagement patterns. It integrates with external APIs to collect data and uses a basic collaborative/content-based filtering approach for recommendations.

## Architecture

### Components
- **FastAPI Backend**: Handles API requests and responses
- **SQLAlchemy ORM**: Database models and interactions
- **Alembic**: Database migrations
- **External API Integration**: Fetches data from SocialVerse API using Flic-Token authentication

### Database Models
- **User**: Stores user information (name, username, etc.)
- **Post**: Video posts with metadata (title, video_link, view_count, etc.)
- **Category**: Post categories (e.g., Flic, Social Media)
- **Topic**: Topics within categories with project codes
- **Interaction**: User interactions with posts (view, like, inspire, rating)
- **Tag**: Tags associated with posts
- **BaseToken**: Blockchain token information (if applicable)

## Recommendation Algorithm

### Personalized Recommendations
1. **User History Analysis**: Analyzes user's viewed, liked, inspired, and rated posts
2. **Similarity Matching**:
   - Finds most common categories, topics, and tags from user's interactions
   - Recommends posts with similar attributes
3. **Fallback**: If insufficient data, recommends popular posts (high view/upvote count)

### Category-Based Recommendations
1. **Personalized Base**: Starts with personalized recommendations
2. **Project Code Filtering**: Filters results to match the specified project_code
3. **Supplement**: Adds additional posts from the project_code if needed

### Cold Start Handling
- For new users with no interaction history
- Recommends top popular posts across all categories
- Uses view_count and upvote_count as popularity metrics

## Data Collection Process

### External APIs Used
1. **All Users**: Fetches user data for the system
2. **All Posts**: Retrieves complete post catalog
3. **Interaction Data**: Collects viewed, liked, inspired, and rated posts
   - Note: Current implementation stores posts but interactions are generalized due to API structure

### Data Storage
- Users, posts, categories, and topics are stored in SQLite database
- Tags are extracted and associated with posts
- Data is collected on application startup

## API Endpoints

### GET /feed
- **Personalized Feed**: `/feed?username={username}`
- **Category Feed**: `/feed?username={username}&project_code={project_code}`
- **Response Format**: Follows the detailed post object structure with status and post array

## Response Format
- **Status**: "success" for successful requests
- **Post Array**: List of post objects with full metadata including owner, category, topic, tags, etc.
- **User Interactions**: upvoted, bookmarked, following fields are set based on user's past interactions with the posts.
- **Timestamps**: In milliseconds (Unix timestamp format)

## Error Handling
- Invalid usernames or project codes return appropriate HTTP errors
- External API failures are logged but don't break the system
- Database connection issues are handled gracefully

## Future Improvements
- Implement true collaborative filtering with user-user similarities
- Add machine learning models for better recommendations
- Enhance interaction tracking with user-specific data
- Add caching layers for performance
- Implement pagination for large result sets
