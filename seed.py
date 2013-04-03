import model
import csv
import os
from datetime import datetime

def load_users(session):
    # use u.user
    # change directory
    os.chdir("/home/user/src/ratings/seed_data")
    with open('u.user', 'rb') as csvfile:
        #reading document
        reader = csv.reader(csvfile)
        for row in reader:
            #parsing line
            split_row = row[0].split("|")
            # assigning variables to each part of the row
            id, age, gender, occupation, zipcode = split_row
            # create new user object
            new_user = model.User(id = id, age = age,
                gender = gender, occupation = occupation, zipcode = zipcode)
            #add new user object to session
            session.add(new_user)
        session.commit()      

def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = "|")
        # def new_date():
        for row in reader:
            title = row[1]
            title = title.decode("latin-1")
            if row[2] != "":
                new_time = row[2]
                format_time = datetime.strptime(new_time, "%d-%b-%Y") 
                new_user = model.Movies(id = row[0], name = title, released_at = format_time, imdb_url = row[4])
                session.add(new_user)
        session.commit()

            # new_row_at_index1 = split_row[1].rstrip('(1234567890)')
            # split_row.insert(1,new_row_at_index1)
            # split_row.pop(1)
            # print split_row


def load_ratings(session):
    # use u.data
    os.chdir("/home/user/src/ratings/seed_data")
    with open('u.data', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            split_row = row[0].split()
            user_id, movie_id, rating, timestamp = split_row
            new_rating = model.Ratings(id = None, user_id = user_id, movie_id = movie_id, rating = rating)
            session.add(new_rating)
        session.commit()

def main(session):
    #load_users(session)
    load_ratings(session)
    # You'll call each of the load_* functions with the session as an argument
    #load_movies(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
