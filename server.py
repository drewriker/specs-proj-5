"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""
    return render_template("homepage.html")

@app.route('/movies')
def all_movies():
    """View all movies with their average ratings"""
    movies_with_ratings = crud.get_movies_with_avg_rating()
    return render_template("all_movies.html", movies_with_ratings=movies_with_ratings)


@app.route('/movies/<int:movie_id>')
def show_movie(movie_id):
    """Show details on specific movie"""
    movie = crud.get_movie_by_id(movie_id)
    
    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def all_users():
    """View all users"""
    users = crud.get_users()
    
    return render_template("all_users.html", users=users)

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show users profile"""
    user = crud.get_user_by_id(user_id)
    
    return render_template("user_details.html", user=user)


"""POST routes"""
@app.route("/user", methods=["POST"])
def register_user():
    """Create a new user"""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again!")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please login")
    
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    """Log a user in"""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    
    if user and user.password == password:
        session['user_id'] = user.user_id
        flash("Logged in successfully", "success")
        return redirect("/movies")
    else:
        flash("Invalid email or password", "danger")
        return redirect("/")
    
@app.route("/rate_movie/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    """Let user rate movies"""
    score = int(request.form.get("score"))
    user_id = session.get("user_id")
    
    if user_id:
        user = crud.get_user_by_id(user_id)
        movie = crud.get_movie_by_id(movie_id)
        
        #check if user has rating
        existing_rating = crud.get_rating_by_user_and_movie(user_id, movie_id)
        if existing_rating:
            #if user has rating, update it and notify
            existing_rating.score = score
            flash(f"Updated your rating for {movie.title} to {score}")
        else: 
            #create new rating
            rating = crud.create_rating(user, movie, score)
            db.session.add(rating)
        #commit changes to database
        db.session.commit()
    else:
        flash("You must be logged in to rate a movie")
        return redirect("/")
    
    return redirect(f"/movies/{movie_id}")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
