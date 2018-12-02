from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Jim Jones", email="someone@email.com",
             picture="https://svgsilh.com/svg/156584.svg")
session.add(User1)
session.commit()

# Summer Activities
category1 = Category(name="Summer Activities")

session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Surf", 
             description="It's the most fun and cost efficient way to spend a holiday surfing and meeting people with the same desires to learn a sport that will hook you from the get go.", category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Basketball",
             description="Players will learn the fundamentals while participating in skills and drills and will have the opportunity to scrimmage during a tournament at the end of the week.", category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Flag Football",
             description="Develop fundamental skills and strategies such as passing, throwing, catching, blocking, and defending/flag-pulling.", category=category1)
session.add(item3)
session.commit()


category2 = Category(name="Winter Activities")

session.add(category2)
session.commit()


item4 = Item(user_id=1, name="Ice Fishing",
             description="Topics include ice safety, how to start and run a power auger, learn to set up a portable shack, set tips ups, use a jig rod, fish with live and artificial bait, how to use electronics, view life under the ice with the underwater camera and more", category=category2)
session.add(item4)
session.commit()


item5 = Item(user_id=1, name="Figure Skating",
             description="Not only does figure skating help young children develop coordination, strength, and agility, it helps to develop their minds. Even at the lowest basic skills levels skaters learn step sequences and can even learn a complete program to be used at local competitions.", category=category2)
session.add(item5)
session.commit()

item6 = Item(user_id=1, name="Hockey",
             description="Skaters will learn the basics of skating, puck handling, passing, shooting, and many of the other skills involved in the game of ice hockey.", category=category2)
session.add(item6)
session.commit()


category3 = Category(name="Fall Activities")

session.add(category3)
session.commit()

item7 = Item(user_id=1, name="Gymnastics",
             description="Our gym program includes floor and tumbling, balance beam, vaulting horse, uneven bars, rhythmical gymnastics.", category=category3)
session.add(item7)
session.commit()

item8 = Item(user_id=1, name="Fencing",
             description="Activities include Group lessons, Competition, Footwork, Games, and Technique & Tactics", category=category3)
session.add(item8)
session.commit()

item9 = Item(user_id=1, name="Drama",
             description=" Activities include play directing, set design, improv acting, singing, and music.", category=category3)

session.add(item9)
session.commit()

category4 = Category(name="Spring Activities")

session.add(category4)
session.commit()

item10 = Item(user_id=1, name="Hicking",
             description="Hiking is a healthy low-impact way to exercise and enjoy the outdoors. Whether you are looking to challenge yourself, explore cultural landmarks, or just 'get away from it all'", category=category4)
session.add(item10)
session.commit()

item11 = Item(user_id=1, name="Backpacking",
             description="Backpacking is an adventure that blends hiking with backcountry camping. It lets you broaden your horizons beyond the car campground to enjoy a richer, more immersive outdoor experience", category=category4)
session.add(item11)
session.commit()

item12 = Item(user_id=1, name="Camping",
              description="Camping is like staying in a primitive cabin, minus the cabin itself. So, in addition to your tent, pack as though you're going to stay someplace where there's little or no furniture, no electricity, no stove or refrigerator, and the cupboards are bare.", category=category4)
session.add(item12)
session.commit()


print "added items!"
