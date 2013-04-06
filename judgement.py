from flask import Flask, render_template, redirect, request
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
	# age = request.form['age']
	# gender = request.form['gender']
	# occupation = request.form['occupation']
	# zipcode = request.form['zipcode']
	email = request.form['email']
	password = request.form['password']
	new_user = model.User(id = None, age = None, gender = None, occupation = None, zipcode = None, email = email, password = password)
	model.session.add(new_user)
	model.session.commit()
	user = model.session.query(model.User).get(new_user.id)
	return "Your login id is %r" % user.id

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/reviews", methods = ["GET", "POST"])
def user_ratings():
	# saves the user's id into a variable so we can query
	user_id = request.form["id"]
	user_password = request.form["password"]
	user = model.session.query(model.User).get(user_id)
	if user_password == user.password:
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
	else:
		return "You are not a user."
	# if button pushed return redirect...

@app.route("/add_reviews", methods = ["POST"])
def add_reviews():
	add = request.form["add_review"]
	return redirect("/movies_list")

@app.route("/movies_list", methods = ["GET"])
def movies_list():
	movies = model.session.query(model.Movies).all()
	return render_template("all_the_movies.html", movies = movies)

@app.route("/new_review", methods = ["POST"]
def new_review():

@app.route("/commit_review", methods = ["POST"])
def commit_review():
	user_id = request.form["user_id"]
	movie_name = request.form["movie_name"]
	review = request.form["review"]
	movie = model.session.query(model.Movies).filter_by(name = movie_name)
	if movie_name == movie[0].name:
		#get the id
		movie_id = movie[0].id
		#add into ratings database somehow
		new_rating = model.Ratings(id = None, user_id = user_id, movie_id = movie_id, rating = review)
		model.session.add(new_rating)
		model.session.commit()
		#return redirect to login
		return redirect("/login")

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



# user inputs age, gender, occupation zipcode into template
# commit to database
# user is assigned id
# id is printed


if __name__ == "__main__":
	app.run(debug = True)

