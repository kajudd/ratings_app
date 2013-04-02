import model
import csv
import os

def load_users():
    # use u.user
    # change directory
    os.chdir("/home/user/src/ratings/seed_data")
    with open('u.user', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            split_row = row[0].split("|")
            id, age, gender, occupation, zipcode = split_row
            print split_row            
load_users()
    
def load_movies(session):
    # use u.item
    pass

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
