from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
import datetime

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Alphabetical
pupper_names = session.query(Puppy.name).order_by(Puppy.name).all()
# print pupper_names

# Less than 6 months
pupper_age = session.query(Puppy.dateOfBirth).filter(Puppy.dateOfBirth > datetime.datetime.now() - datetime.timedelta(days = 180)).all()
# print pupper_age

# By weight
pupper_weight = session.query(Puppy.weight).order_by(Puppy.weight).all()
# print pupper_weight

# By shelter
pupper_shelter = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
for item in pupper_shelter:
	print item[0].name, item[1]