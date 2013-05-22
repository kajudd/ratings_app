from flask import Flask, render_template, redirect, request, session
import model
import math

app = Flask(__name__)


@app.route("/")
def signup():
    return render_template("new_user.html")
    
@app.route("/signup_done", methods = ["POST"])
def new_user():
    email = request.form['email']
    password = request.form['password']
    # inserts the user's email and pswrd into the database
    new_user = model.User(id = None, age = None, gender = None, occupation = None, zipcode = None, email = email, password = password)
    model.session.add(new_user)
    model.session.commit()
    user = model.session.query(model.User).get(new_user.id)
    return redirect("/reviews")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/authenticate", methods = ["POST"])
def authenticate():
    user_email = request.form['email']
    user_password = request.form['password']
    user = model.session.query(model.User).filter_by(email = user_email).first()
    if user_password == user.password:
        session['user'] = user.id
        return redirect("/reviews")
    else:
        return redirect("/login")

@app.route("/reviews", methods = ["GET", "POST"])
def user_ratings():
    user = session.get("user")

    user_info = model.session.query(model.User).get(user)
    user_rating = user_info.ratings

    movie_names = []
    for rating in user_rating:
        movie = model.session.query(model.Movies).get(rating.movie_id)
        movie_name = movie.name
        movie_names.append(movie_name)

    ratings = []
    for rating in user_rating:
        ratings.append(rating.rating)
    # takes the ratings and movie_names lists and makes them into tuples
    tuples_of_ratings = zip(ratings, movie_names)
    return render_template("reviews.html", tuples_of_ratings = tuples_of_ratings)

@app.route("/add_reviews", methods = ["POST"])
def add_reviews():
    add = request.form["add_review"]
    return redirect("/movies_list")

@app.route("/movies_list", methods = ["GET"])
def movies_list():
    movies = model.session.query(model.Movies).all()
    return render_template("all_the_movies.html", movies = movies)


@app.route("/movie/<int:id>", methods = ["GET", "POST"])
def new_rating(id):
    movie = model.session.query(model.Movies).get(id)
    session['movie'] = movie.id 
    imdb = movie.imdb_url
    user_id = session.get("user")
    user = model.session.query(model.User).get(user_id)
    prediction = model.User.predict_rating(user, movie)
    predition = math.round(prediction)
    return render_template("movie_form.html", imdb=imdb, prediction=prediction)


@app.route("/commit_review", methods = ["POST"])
def commit_review():
    user_id = session.get("user")
    movie_id = session.get("movie")
    users_info = model.session.query(model.User).get(user_id)
    new_rating = request.form["rating"]
    # if there's a rating already for that movie then update instead of add new one into database under the user
    all_ratings = []
    ratings = users_info.ratings
    for rating in ratings:
        users_movies = rating.movie_id
        all_ratings.append(users_movies)
    if movie_id in all_ratings:
        rating = model.session.query(model.Ratings).filter_by(user_id=user_id, movie_id=movie_id).first()
        rating.rating = new_rating
        model.session.commit()
    else:
        add_rating = model.Ratings(id=None, user_id=user_id, movie_id=movie_id, rating=new_rating)
        model.session.add(add_rating)
        model.session.commit()
    return redirect("/reviews")

@app.route("/users")
def view_users():
    users = model.session.query(model.User).all()
    return render_template("users.html", users = users)

@app.route("/user/<int:id>", methods = ["GET"])
def list_movies(id):
    user = model.session.query(model.User).get(id)
    user_rating = user.ratings
    movie_names = []
    for rating in user_rating:
        movie = model.session.query(model.Movies).get(rating.movie_id)
        movie_name = movie.name
        movie_names.append(movie_name)
    ratings = []
    for rating in user_rating:
        ratings.append(rating.rating)
    tuples_of_ratings = zip(ratings, movie_names)
    return render_template("other_reviews.html", tuples_of_ratings=tuples_of_ratings)

@app.route('/logout')
def logout():
    return redirect('/')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == "__main__":
    app.run(debug = True)

