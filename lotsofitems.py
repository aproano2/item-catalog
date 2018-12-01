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

item1 = Item(user_id=1, name="Surf Camp", 
             description="It's the most fun and cost efficient way to spend a holiday surfing and meeting people with the same desires to learn a sport that will hook you from the get go.", category=category1)

session.add(item1)
session.commit()


category2 = Category(name="Winter Activities")

session.add(category2)
session.commit()

category3 = Category(name="Fall Activities")

session.add(category3)
session.commit()

category4 = Category(name="Spring Activities")

session.add(category4)
session.commit()

print "added items!"
