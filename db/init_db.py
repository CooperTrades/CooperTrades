
m sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://postgres:dbpassword@localhost:5434/postgres', echo=True)
# After dropping and recreating tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# # Obtain a connection from the engine
# with engine.connect() as conn:
#     # Reset the sequence for class_id in the classes table
#     conn.execute(text("ALTER SEQUENCE classes_class_id_seq RESTART WITH 1;"))
#     # Commit the changes if needed (not required for ALTER SEQUENCE)
#     conn.commit()

class Class(Base):
    __tablename__ = 'classes'
    
    class_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(255), nullable=False)
    section = Column(String(255), nullable=False)
    instructor = Column(String(255), nullable=False)
    day_time = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    units = Column(Integer, nullable=False)
    max_capacity = Column(Integer, nullable=False)
    num_students = Column(Integer, nullable=False)
    waitlist_status = Column(Boolean, nullable=False)  # tinyint(1) is often used as a boolean

    def __repr__(self):
        return f"<Class(class_id={self.class_id}, course_name='{self.course_name}', section='{self.section}', instructor='{self.instructor}', day_time='{self.day_time}', location='{self.location}', units={self.units}, max_capacity={self.max_capacity}, num_students={self.num_students}, waitlist_status={self.waitlist_status})>"

class Event(Base):
    __tablename__ = 'events'
    
    events_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Assuming there is a users table with user_id
    class_id = Column(Integer, ForeignKey('classes.class_id'), nullable=False)  # Assuming a relation with the classes table
    type = Column(Integer, nullable=False)  # This column name 'type' is typically reserved in Python, consider renaming

    def __repr__(self):
        return f"<Event(events_id={self.events_id}, user_id={self.user_id}, class_id={self.class_id}, type={self.type})>"

class Trade(Base):
    __tablename__ = 'trades'
    
    trade_id = Column(Integer, primary_key=True, autoincrement=True)
    requester = Column(Integer, nullable=False)  # Assuming this refers to a user_id in another table
    accepter = Column(Integer, nullable=True)  # This might also refer to a user_id and can be null
    get1 = Column(Integer, nullable=True)  # Details for this and subsequent 'get' columns would depend on their purpose
    get2 = Column(Integer, nullable=True)
    get3 = Column(Integer, nullable=True)
    get_chosen = Column(Integer, nullable=True)
    give = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)  # tinyint(1) is often used as a boolean
    post_time = Column(DateTime, default=func.now(), nullable=False)
    accept_time = Column(DateTime, nullable=True)

    def __repr__(self):
        return (f"<Trade(trade_id={self.trade_id}, requester={self.requester}, "
                f"accepter={self.accepter}, get1={self.get1}, get2={self.get2}, "
                f"get3={self.get3}, get_chosen={self.get_chosen}, give={self.give}, "
                f"status={self.status}, post_time={self.post_time}, accept_time={self.accept_time})>")

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(254), nullable=False)
    username = Column(String(30), nullable=True)  # The username can be NULL as per your table definition
    password = Column(String(60), nullable=False)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, email='{self.email}', username='{self.username}', password='***')>"

class UserClass(Base):
    __tablename__ = 'user_class'
    
    user_class_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Assuming there is a users table
    class_id = Column(Integer, ForeignKey('classes.class_id'), nullable=False)  # Assuming a relationship with the classes table

    def __repr__(self):
        return f"<UserClass(user_class_id={self.user_class_id}, user_id={self.user_id}, class_id={self.class_id})>"

Session = sessionmaker(bind=engine)
session = Session()

# Insert dummy data into users
users = [
    {'email': 'alice@example.com', 'username': 'alice', 'password': 'alicepass'},
    {'email': 'bob@example.com', 'username': 'bob', 'password': 'bobpass'},
]

# Insert dummy data into classes
classes = [
    {'course_name': 'Calculus', 'section': 'A', 'instructor': 'Prof. Newton', 'day_time': 'MWF 9-10', 'location': 'Bldg 5', 'units': 3, 'max_capacity': 30, 'num_students': 25, 'waitlist_status': False},
]

# Insert dummy data into events
events = [
    {'user_id': 1, 'class_id': 1, 'type': 1},
]

# Insert dummy data into trades
trades = [
    {'requester': 1, 'give': 1, 'status': True},
]

# Insert dummy data into user_class
user_classes = [
    {'user_id': 1, 'class_id': 1},
]

# Add users to session
for user_data in users:
    user = User(**user_data)
    session.add(user)
# session.commit()  # Commit users

# Add classes to the session and commit
for class_data in classes:
    class_ = Class(**class_data)
    session.add(class_)
# session.commit()  # Commit classes **This step must occur before adding events**

# Now that classes are committed, add events to the session and commit
for event_data in events:
    event = Event(**event_data)
    session.add(event)
# session.commit()  # Commit events

# Add trades to the session and commit
for trade_data in trades:
    trade = Trade(**trade_data)
    session.add(trade)
# session.commit()  # Commit trades

# Finally, add user_classes to the session and commit
for user_class_data in user_classes:
    user_class = UserClass(**user_class_data)
    session.add(user_class)

session.commit()
session.close()

conn = engine.connect()
print(conn.execute(text("SELECT * from classes")).fetchall())
