from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

ENGINE = create_engine("sqlite:///ratings.db", echo = False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))


Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	age = Column(Integer, nullable = True)
	gender = Column(String(2), nullable = True)
	occupation = Column(String(64), nullable = True)
	zipcode = Column(String(15), nullable = True)
	email = Column(String(200), nullable = True)
	password = Column(String(64), nullable = True)

class Movies(Base):
	__tablename__ = "movies"

	id = Column(Integer, primary_key = True)
	name = Column(String(140))
	released_at = Column(String(64))
	imdb_url = Column(String(300))


class Ratings(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer(64), ForeignKey('users.id'))
	movie_id = Column(Integer(64), ForeignKey('movies.id'))
	rating = Column(Integer(64))

	user = relationship("User", backref = backref("ratings", order_by=id))

	movies = relationship("Movies", backref = backref("ratings", order_by=id))


### End class declarations


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
