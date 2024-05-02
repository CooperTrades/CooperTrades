import enum

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, text, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# class TradeStatus(enum.Enum):
#     AVAILABLE = "Available"
#     PENDING = "Pending"
#     NOT_AVAILABLE = "Not Available"
#
# class Category(enum.Enum):
#     ART = "Art"
#     CLOTHING = "Clothing"
#     MISC = "MISC"
#
# class Condition(enum.Enum):
#     NEW = "New"
#     USED = "Used"
#     OLD = "Old"
#
#
# class Item(Base):
#     __tablename__ = 'items'
#     item_id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
#     description = Column(String(255), nullable=True)
#     category = Column(Enum(Category), default=Category.MISC)
#     condition = Column(Enum(Condition), default= Condition.NEW)
#     trade_status = Column(Enum(TradeStatus), default=TradeStatus.AVAILABLE)
#
#     def __repr__(self):
#         return f"<Item(item_id={self.item_id}, name='{self.name}', description='{self.description}', category='{self.category}', condition='{self.condition}', trade_status='{self.trade_status}')>"
#
# class Trade(Base):
#     __tablename__ = 'trades'
#
#     trade_id = Column(Integer, primary_key=True, autoincrement=True)
#     requester_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
#     accepter_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
#     requester_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)  # Item the requester is offering
#     accepter_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=True)  # Item the accepter is offering
#     status = Column(Boolean, nullable=False)  # True if accepted, False otherwise
#     post_time = Column(DateTime, default=func.now(), nullable=False)
#     accept_time = Column(DateTime, nullable=True)
#
#     # Relationship to User model
#     requester = relationship("User", foreign_keys=[requester_id])
#     accepter = relationship("User", foreign_keys=[accepter_id])
#
#     # Relationship to Item model
#     requester_item = relationship("Item", foreign_keys=[requester_item_id])
#     accepter_item = relationship("Item", foreign_keys=[accepter_item_id])
#
#     def __repr__(self):
#         return (f"<Trade(trade_id={self.trade_id}, requester_id={self.requester_id}, "
#                 f"accepter_id={self.accepter_id}, requester_item_id={self.requester_item_id}, "
#                 f"accepter_item_id={self.accepter_item_id}, status={self.status}, "
#                 f"post_time='{self.post_time}', accept_time='{self.accept_time}')>")
#
# class User(Base):
#     __tablename__ = 'users'
#
#     user_id = Column(Integer, primary_key=True, autoincrement=True)
#     email = Column(String(254), nullable=False)
#     username = Column(String(30), nullable=True)
#     password = Column(String(60), nullable=False)
#
#     def __repr__(self):
#         return f"<User(user_id={self.user_id}, email='{self.email}', username='{self.username}', password='***')>"
# Enum classes
class TradeStatus(enum.Enum):
    AVAILABLE = "Available"
    PENDING = "Pending"
    NOT_AVAILABLE = "Not Available"

class Category(enum.Enum):
    ART = "Art"
    CLOTHING = "Clothing"
    MISC = "Misc"

class Condition(enum.Enum):
    NEW = "New"
    USED = "Used"
    OLD = "Old"

# Item class with indexes and relationships
class Item(Base):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    description = Column(String(255), nullable=True)
    category = Column(Enum(Category), default=Category.MISC, nullable=False)
    condition = Column(Enum(Condition), default=Condition.NEW, nullable=False)
    trade_status = Column(Enum(TradeStatus), default=TradeStatus.AVAILABLE, nullable=False)

    # Indexes
    __table_args__ = (
        Index('idx_category', 'category'),
        Index('idx_condition', 'condition'),
    )

    user = relationship("User", back_populates="items")

    def __repr__(self):
        return (f"<Item(item_id={self.item_id}, description='{self.description}', "
                f"category='{self.category.value}', condition='{self.condition.value}', "
                f"trade_status='{self.trade_status.value}')>")

# Trade class with relationships
class Trade(Base):
    __tablename__ = 'trades'

    trade_id = Column(Integer, primary_key=True, autoincrement=True)
    requester_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    accepter_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    requester_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    accepter_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=True)
    status = Column(Boolean, nullable=False)
    post_time = Column(DateTime, default=func.now(), nullable=False)
    accept_time = Column(DateTime, nullable=True)

    requester = relationship("User", foreign_keys=[requester_id], back_populates="requested_trades")
    accepter = relationship("User", foreign_keys=[accepter_id], back_populates="accepted_trades")

    requester_item = relationship("Item", foreign_keys=[requester_item_id])
    accepter_item = relationship("Item", foreign_keys=[accepter_item_id])

    def __repr__(self):
        return (f"<Trade(trade_id={self.trade_id}, requester_id={self.requester_id}, "
                f"accepter_id={self.accepter_id}, requester_item_id={self.requester_item_id}, "
                f"accepter_item_id={self.accepter_item_id}, status={self.status}, "
                f"post_time='{self.post_time}', accept_time='{self.accept_time}')>")

# User class with relationships
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(254), nullable=False)
    username = Column(String(30), nullable=True)
    password = Column(String(60), nullable=False)

    items = relationship("Item", back_populates="user")
    requested_trades = relationship("Trade", foreign_keys=[Trade.requester_id], back_populates="requester")
    accepted_trades = relationship("Trade", foreign_keys=[Trade.accepter_id], back_populates="accepter")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, email='{self.email}', username='{self.username}', password='***')>"

engine = create_engine('postgresql+psycopg2://postgres:dbpassword@localhost:5435/postgres', echo=True)
# After dropping and recreating tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

user1 = User(email='john.doe@example.com', username='john_doe', password='securepassword123')
user2 = User(email='jane.doe@example.com', username='jane_doe', password='securepassword456')

session.add(user1)
session.add(user2)
session.commit()

# Insert dummy items, assuming the users now have their IDs
item1 = Item(user_id=user1.user_id, description='A beautiful canvas painting', category='ART', condition='NEW', trade_status="AVAILABLE")
item2 = Item(user_id=user2.user_id, description='Vintage leather-bound jacket', category='CLOTHING', condition='USED', trade_status="NOT_AVAILABLE")

session.add(item1)
session.add(item2)
session.commit()

# Insert a dummy trade
trade = Trade(requester_id=user1.user_id, accepter_id=user2.user_id, requester_item_id=item1.item_id, accepter_item_id=item2.item_id, status=True)

session.add(trade)
session.commit()
session.close()

conn = engine.connect()
print(conn.execute(text("SELECT * from items")).fetchall())
