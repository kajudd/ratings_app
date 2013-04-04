from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
	user_list = model.session.query(model.User).limit(5).all()
	return render_template("user_list.html", users = user_list)

@app.route("/signup", methods = ["GET"])
def signup():
	return render_template("new_user.html")
	# request.form
	new_user = model.User(id = id, age = "age", gender = "gender", occupation = "occupation", zipcode = "zipcode")
	session.add(new_user)
	session.commit()
#user inputs age, gender, occupation zipcode into template
#commit to database
#user is assigned id
#id is printed


if __name__ == "__main__":
	app.run(debug = True)

