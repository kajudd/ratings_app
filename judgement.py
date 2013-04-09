from flask import Flask, render_template, redirect, request, session
import model


app = Flask(__name__)

@app.route("/")
def index():
	user_list = model.session.query(model.User).limit(5).all()
	return render_template("user_list.html", users = user_list)

@app.route("/signup")
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
	return "Your login id is %r" % user.id

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/authenticate", methods = ["POST"])
def authenticate():
	user_id = request.form['id']
	user_password = request.form['password']
	session['user'] = user_id
	return redirect("/reviews")

@app.route("/reviews", methods = ["GET", "POST"])
def user_ratings():
	user = session.get("user")
	# if user_password == user.password:
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
	print imdb 
	return render_template("movie_form.html", imdb = imdb)


@app.route("/commit_review", methods = ["POST"])
def commit_review():
	user_id = session.get("user")
	movie_id = session.get("movie")
	rating = request.form["rating"]
	# if there's a rating already for that movie then update instead of add new one into database under the user
	all_ratings = []
	ratings = model.session.query(model.User).get(user.ratings)
	for rating in ratings:
		users_info = model.session.query(model.User).get(user_id)
		users_movies = users
		all_ratings.append(users_movies)
	if movie_id in all_ratings:
		rating = model.session.query(model.Ratings).get(ratings.movie_id)
		rating_id = rating.id
		new_rating = model.Ratings(id = rating_id, user_id = user_id, movie_id = movie_id, rating = rating)
		model.session.add(new_rating)
		model.session.commit()
	else:
		new_rating = model.Ratings(id = None, user_id = user_id, movie_id = movie_id, rating = rating)
		model.session.add(new_rating)
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
	print tuples_of_ratings
	# have movie_names and ratings, have to create tuples and print them??? 
	return render_template("reviews.html", tuples_of_ratings = tuples_of_ratings)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# user inputs age, gender, occupation zipcode into template
# commit to database
# user is assigned id
# id is printed


if __name__ == "__main__":
	app.run(debug = True)

