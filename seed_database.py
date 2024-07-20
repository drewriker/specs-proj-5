"""Script to seed database"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud, model, server

os.system("dropdb -p 5433 ratings")
os.system("createdb -p 5433 ratings")

model.connect_to_db(server.app)

with server.app.app_context():
    model.db.create_all()

    # load movie data from JSON file
    with open("data/movies.json") as f:
        movie_data = json.loads(f.read())
    
    #create movies, store them in list
    movies_in_db = []
    for movie in movie_data:
        title, overview, poster_path = (
            movie["title"],
            movie["overview"],
            movie["poster_path"]
        )
        #format the release date
        release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
        
        #create the movies from the function in CRUD.py
        db_movie = crud.create_movie(title, overview, release_date, poster_path)
        #add all movies to list
        movies_in_db.append(db_movie)

    model.db.session.add_all(movies_in_db)
    model.db.session.commit()
    
with server.app.app_context():
    for n in range(10):
        email = f'user{n}@test.com'
        password = "test"
        
        user = crud.create_user(email, password)
        model.db.session.add(user)
        
        for i in range(10):
            random_movie = choice(movies_in_db)
            score = randint(1, 5)
            
            rating = crud.create_rating(user, random_movie, score)
            model.db.session.add(rating)
    
    model.db.session.commit()