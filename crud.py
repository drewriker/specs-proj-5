"""CRUD Operations"""

from model import db, User, Movie, Rating, connect_to_db
from sqlalchemy.sql import func



def create_user(email, password):
    """Create and return a new user"""
    
    user = User(email=email, password=password)
    
    return user

def get_users():
    """return all users"""
    return User.query.all()

def get_user_by_id(user_id):
    """return user based on user ID"""
    return User.query.get(user_id)

def get_user_by_email(user_email):
    """return user based on email"""
    return User.query.filter(User.email == user_email).first()
    
def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie"""
    
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)
    
    return movie

def get_movies():
    """Return all movies in DB"""
    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return a specific movie"""
    return Movie.query.get(movie_id)

def create_rating(user, movie, score):
    """Create and return a new rating"""
    
    rating = Rating(user=user, movie=movie, score=score)
    return rating

def get_rating_by_user_and_movie(user_id, movie_id):
    """Return a rating given by a user to a specific movie, if it exists."""
    return Rating.query.filter(Rating.user_id == user_id, Rating.movie_id == movie_id).first()

def get_movies_with_avg_rating():
    """Return all movies with their average rating"""
    return db.session.query(
        Movie,
        func.coalesce(func.avg(Rating.score), None).label('average_rating')  # Return None if no rating
    ).outerjoin(Rating).group_by(Movie.movie_id).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)