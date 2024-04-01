from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from sqlalchemy.orm import scoped_session
from pyramid.view import view_config
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from pyramid.response import Response
from pyramid.request import Request
from pyramid.events import NewResponse

Base = declarative_base()
engine = create_engine('postgresql+psycopg2://postgres:dbpassword@localhost:5435/postgres', echo=True)
DBSession = scoped_session(sessionmaker(bind=engine))

class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    description = Column(String(255), nullable=True)
    category = Column(String(255), nullable=False)
    condition = Column(String(255), nullable=False)


class Trade(Base):
    __tablename__ = 'trades'

    trade_id = Column(Integer, primary_key=True, autoincrement=True)
    requester_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    accepter_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    requester_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)  # Item the requester is offering
    accepter_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=True)  # Item the accepter is offering
    status = Column(Boolean, nullable=False)  # True if accepted, False otherwise
    post_time = Column(DateTime, default=func.now(), nullable=False)
    accept_time = Column(DateTime, nullable=True)

    # Relationship to User model
    requester = relationship("User", foreign_keys=[requester_id])
    accepter = relationship("User", foreign_keys=[accepter_id])

    # Relationship to Item model
    requester_item = relationship("Item", foreign_keys=[requester_item_id])
    accepter_item = relationship("Item", foreign_keys=[accepter_item_id])


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(254), nullable=False)
    username = Column(String(30), nullable=True)
    password = Column(String(60), nullable=False)

@view_config(route_name='get_items', renderer='json')
def get_items(request):
    items = DBSession.query(Item).all()
    return [{"id": item.item_id, "description": item.description, "category": item.category} for item in items]


@view_config(route_name='add_item', request_method='POST', renderer='json')
def add_item(request: Request):
    description = request.params.get('description')
    category = request.params.get('category')
    condition = request.params.get('condition')
    # Assuming a user_id is passed or determined some other way
    user_id = request.params.get('user_id')

    if not all([description, category, condition, user_id]):
        return Response(json_body={'error': 'Missing fields'}, status=400)

    new_item = Item(description=description, category=category, condition=condition, user_id=user_id)
    DBSession.add(new_item)
    DBSession.commit()

    return Response(json_body={'message': 'Item added successfully', 'id': new_item.item_id}, status=201)

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept',
        })
    event.request.add_response_callback(cors_headers)

if __name__ == '__main__':
    with Configurator() as config:
        config.add_subscriber(add_cors_headers_response_callback, NewResponse)
        config.add_route('get_items', '/items')
        config.add_route('add_item', '/items/add')
        config.scan()
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    print("Serving on http://0.0.0.0:6543...")
    server.serve_forever()
