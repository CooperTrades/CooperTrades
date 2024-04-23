import enum
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPForbidden
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.events import NewResponse

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://postgres:dbpassword@localhost:5435/postgres', echo=True)
DBSession = scoped_session(sessionmaker(bind=engine))


class TradeStatus(enum.Enum):
    AVAILABLE = "Available"
    PENDING = "Pending"
    NOT_AVAILABLE = "Not Available"


class Item(Base):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    description = Column(String(255), nullable=True)
    category = Column(String(255), nullable=False)
    condition = Column(String(255), nullable=False)
    trade_status = Column(Enum(TradeStatus), default=TradeStatus.AVAILABLE)

    # Creating an index on user_id
    # idx_user_id = Index('idx_user_id', 'user_id')


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

    # Index for commonly queried columns
    # idx_trade_status = Index('idx_trade_status', 'requester_id', 'status')


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
def add_item(request):
    try:
        data = request.json_body
        trade_status = TradeStatus[data.get('trade_status', 'AVAILABLE')]
        new_item = Item(
            user_id=data['user_id'],
            description=data['description'],
            category=data['category'],
            condition=data['condition'],
            trade_status = trade_status
        )
        DBSession.add(new_item)
        DBSession.commit()
        return {'message': 'Item added successfully', 'id': new_item.item_id}
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=400)


@view_config(route_name='add_user', request_method='POST', renderer='json')
def add_user(request):
    try:
        data = request.json_body
        new_user = User(email=data['email'], username=data.get('username'), password=data['password'])
        DBSession.add(new_user)
        DBSession.commit()
        return {'message': 'User created successfully', 'id': new_user.user_id}
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)


@view_config(route_name='get_users', renderer='json')
def get_users(request):
    users = DBSession.query(User).all()
    return [{'user_id': user.user_id, 'email': user.email, 'username': user.username} for user in users]

@view_config(route_name='user_details', renderer='json')
def user_details(request):
    user_id = request.matchdict['id']
    user = DBSession.query(User).filter(User.user_id == user_id).first()
    items = DBSession.query(Item).filter(Item.user_id == user_id).all()
    if user:
        user_info = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'items': [{
                'item_id': item.item_id,
                'description': item.description,
                'category': item.category,
                'condition': item.condition,
                'trade_status': item.trade_status.name  # Ensure trade_status is shown as a string
            } for item in items]
        }
        return user_info
    else:
        return Response(json_body={'error': 'User not found'}, status=404)


@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    try:
        data = request.json_body
        username = data['username']
        password = data['password']
        user = DBSession.query(User).filter_by(username=username).first()
        if user and user.password == password:
            return {'message': 'Login successful', 'user_id': user.user_id}
        else:
            return HTTPForbidden('Incorrect username or password')
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)


@view_config(route_name='execute_trade', request_method='POST', renderer='json')
def execute_trade(request):
    try:
        data = request.json_body
        requester_item_id = data['requester_item_id']
        accepter_item_id = data['accepter_item_id']

        # Fetch the items from the database
        requester_item = DBSession.query(Item).filter_by(item_id=requester_item_id).one()
        accepter_item = DBSession.query(Item).filter_by(item_id=accepter_item_id).one()

        # Check if items exist and belong to different users
        if requester_item and accepter_item and requester_item.user_id != accepter_item.user_id:
            # Swap the user_ids
            temp = requester_item.user_id
            requester_item.user_id = accepter_item.user_id
            accepter_item.user_id = temp

            # Commit changes to the database
            DBSession.commit()
            return {'message': 'Trade executed successfully'}
        return {'message': 'Trade cannot be executed'}
    except Exception as e:
        return Response(json_body={'error': str(e)}, status=500)

@view_config(route_name='available_items', renderer='json')
def available_items(request):
    # Fetch items where trade_status is AVAILABLE and join with User to get user details
    items = DBSession.query(Item, User).join(User, Item.user_id == User.user_id).filter(Item.trade_status == TradeStatus.AVAILABLE).all()
    return [{
        'item_id': item[0].item_id,
        'description': item[0].description,
        'category': item[0].category,
        'condition': item[0].condition,
        'user_id': item[1].user_id,
        'username': item[1].username
    } for item in items]


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers': 'Authorization,Content-Type',
            'Access-Control-Allow-Credentials': 'true',
        })

    event.request.add_response_callback(cors_headers)


def cors_preflight_view(request):
    response = Response()
    response.headers.update({
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Methods': 'POST, GET, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization',
        'Access-Control-Allow-Credentials': 'true',
    })
    return response


if __name__ == '__main__':
    with Configurator() as config:
        config.add_subscriber(add_cors_headers_response_callback, 'pyramid.events.NewResponse')

        config.add_route('cors_preflight', '/{catch_all:.*}', request_method='OPTIONS')
        config.add_view(cors_preflight_view, route_name='cors_preflight')

        config.add_route('get_items', '/items')
        config.add_route('add_item', '/items/add')
        config.add_route('get_users', '/users')
        config.add_route('add_user', '/users/add')
        config.add_route('login', '/login')
        config.add_route('execute_trade', '/trade/execute')
        config.add_route('available_items', '/items/available')
        config.add_route('user_details', '/user/{id}')

        config.scan()
        app = config.make_wsgi_app()
        server = make_server('0.0.0.0', 6543, app)
        print("Serving on http://0.0.0.0:6543...")
        server.serve_forever()
