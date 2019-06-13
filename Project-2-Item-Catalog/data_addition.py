from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///catalog_items.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="Unnati Sangani", email="a.unnati@gmail.com",
             picture='https://lh3.googleusercontent.com/a-/AAuE7mDN2RdP4DdyTb2uRAiNbTz5b3_mk279SO6AX8Is2g=s96')
session.add(User1)
session.commit()


# Category Soccer
category1 = Category(user_id=1, name="Soccer")
session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Jersey", description="T-shirt to wear in", category=category1)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Shinguard", description="Single Shinguard", category=category1)
session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Two Shinguard", description="Pair of Shinguard", category=category1)
session.add(item3)
session.commit()


# Category Basketball
category2 = Category(user_id=1, name="Basketball")
session.add(category2)
session.commit()

item1 = Item(user_id=1, name="Basketball", description="High quality ball", category=category2)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Shoes", description="Shoes for Basketball", category=category2)
session.add(item2)
session.commit()


# Category Baseball
category3 = Category(user_id=1, name="Baseball")
session.add(category3)
session.commit()

item1 = Item(user_id=1, name="Baseball", description="Baseball to play", category=category3)
session.add(item1)
session.commit()


# Category Frisbee
category4 = Category(user_id=1, name="Frisbee")
session.add(category4)
session.commit()

item1 = Item(user_id=1, name="Frisbee", description="Frisbee to play", category=category4)
session.add(item1)
session.commit()

# Category Snow boarding
category5 = Category(user_id=1, name="Snow boarding")
session.add(category5)
session.commit()

item1 = Item(user_id=1, name="Goggles", description="Goggles", category=category5)
session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Snowboard", description="Snow board", category=category5)
session.add(item2)
session.commit()

# Category Rock climbing
category6 = Category(user_id=1, name="Rock Climbing")
session.add(category6)
session.commit()

item1 = Item(user_id=1, name="Hooks", description="Hooks for climbing", category=category6)
session.add(item1)
session.commit()

# Category Foosball
category7 = Category(name="Foosball")
session.add(category7)
session.commit()

item1 = Item(name="Ball", description="Ball to play", category=category7)
session.add(item1)
session.commit()


# Category Skating
category8 = Category(name="Skating")
session.add(category8)
session.commit()

item1 = Item(name="Skates", description="Roller skates", category=category8)
session.add(item1)
session.commit()


# Category Hockey
category9 = Category(name="Hockey")
session.add(category9)
session.commit()

item1 = Item(name="Hockey Stick", description="Hockey Stick for playing", category=category9)
session.add(item1)
session.commit()


print("Items are added!")

