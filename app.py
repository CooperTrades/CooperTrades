# # from wsgiref.simple_server import make_server
# # from pyramid.config import Configurator
# # from sqlalchemy.orm import scoped_session
# # from pyramid.view import view_config
# # from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, text
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker, relationship
# # from sqlalchemy.sql import func
# # from pyramid.response import Response
# # from pyramid.request import Request
# # from pyramid.events import NewResponse
# #
# # Base = declarative_base()
# # engine = create_engine('postgresql+psycopg2://postgres:dbpassword@localhost:5435/postgres', echo=True)
# # DBSession = scoped_session(sessionmaker(bind=engine))
# #
# # class Item(Base):
# #     __tablename__ = 'items'
# #
# #     item_id = Column(Integer, primary_key=True, autoincrement=True)
# #     user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
# #     description = Column(String(255), nullable=True)
# #     category = Column(String(255), nullable=False)
# #     condition = Column(String(255), nullable=False)
# #
# #
# # class Trade(Base):
# #     __tablename__ = 'trades'
# #
# #     trade_id = Column(Integer, primary_key=True, autoincrement=True)
# #     requester_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
# #     accepter_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
# #     requester_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)  # Item the requester is offering
# #     accepter_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=True)  # Item the accepter is offering
# #     status = Column(Boolean, nullable=False)  # True if accepted, False otherwise
# #     post_time = Column(DateTime, default=func.now(), nullable=False)
# #     accept_time = Column(DateTime, nullable=True)
# #
# #     # Relationship to User model
# #     requester = relationship("User", foreign_keys=[requester_id])
# #     accepter = relationship("User", foreign_keys=[accepter_id])
# #
# #     # Relationship to Item model
# #     requester_item = relationship("Item", foreign_keys=[requester_item_id])
# #     accepter_item = relationship("Item", foreign_keys=[accepter_item_id])
# #
# #
# # class User(Base):
# #     __tablename__ = 'users'
# #
# #     user_id = Column(Integer, primary_key=True, autoincrement=True)
# #     email = Column(String(254), nullable=False)
# #     username = Column(String(30), nullable=True)
# #     password = Column(String(60), nullable=False)
# #
# # @view_config(route_name='get_items', renderer='json')
# # def get_items(request):
# #     items = DBSession.query(Item).all()
# #     return [{"id": item.item_id, "description": item.description, "category": item.category} for item in items]
# #
# #
# # @view_config(route_name='add_item', request_method='POST', renderer='json')
# # def add_item(request: Request):
# #     print("add_item view called")
# #     print("Received data:", request.params)
# #     description = request.params.get('description')
# #     category = request.params.get('category')
# #     condition = request.params.get('condition')
# #     user_id = request.params.get('user_id') # for now, will maybe need to just do something else but maybe not
# #
# #     if not all([description, category, condition, user_id]):
# #         return Response(json_body={'error': 'Missing fields'}, status=400)
# #
# #     new_item = Item(description=description, category=category, condition=condition, user_id=user_id)
# #     DBSession.add(new_item)
# #     DBSession.commit()
# #
# #     return Response(json_body={'message': 'Item added successfully', 'id': new_item.item_id}, status=201)
# #
# # @view_config(route_name='add_user', request_method='POST', renderer='json')
# # def add_user(request: Request):
# #     try:
# #         data = request.json_body
# #         email = data['email']
# #         username = data.get('username', None)  # Optional field
# #         password = data['password']  # In real-world applications, ensure this is hashed
# #
# #         new_user = User(email=email, username=username, password=password)
# #         DBSession.add(new_user)
# #         DBSession.flush()  # Flush to get the new user id if needed immediately after
# #         return {'message': 'User created successfully', 'id': new_user.user_id}
# #     except Exception as e:
# #         return Response(json_body={'error': str(e)}, status=500)
# #
# # @view_config(route_name='get_users', renderer='json')
# # def get_users(request):
# #     try:
# #         users = DBSession.query(User).all()
# #         return [{'user_id': user.user_id, 'email': user.email, 'username': user.username} for user in users]
# #     except Exception as e:
# #         return Response(json_body={'error': str(e)}, status=500)
# #
# #
# # def add_cors_headers_response_callback(event):
# #     def cors_headers(request, response):
# #         response.headers.update({
# #             'Access-Control-Allow-Origin': 'http://localhost:3000',
# #             'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
# #             'Access-Control-Allow-Headers': 'Authorization,Content-Type',
# #             'Access-Control-Allow-Credentials': 'true',
# #         })
# #     event.request.add_response_callback(cors_headers)
# #
# #
# # @view_config(route_name='cors_preflight', request_method='OPTIONS')
# # def cors_preflight_view(request):
# #     request.response.headers.update({
# #         'Access-Control-Allow-Origin': 'http://localhost:3000',
# #         'Access-Control-Allow-Methods': 'POST, GET, PUT, DELETE, OPTIONS',
# #         'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization',
# #         'Access-Control-Allow-Credentials': 'true',
# #     })
# #     return request.response
# #
# # if __name__ == '__main__':
# #     with Configurator() as config:
# #         config.add_subscriber(add_cors_headers_response_callback, 'pyramid.events.NewResponse')
# #         config.add_route('get_items', '/items')
# #         config.add_route('cors_preflight', '/items/add')
# #         config.add_view(add_item, route_name='add_item', request_method='POST', renderer='json')
# #         config.add_route('add_item', '/items/add')
# #         config.add_route('get_users', '/users')
# #         config.add_route('add_user', '/users/add')
# #         config.scan()
# #         app = config.make_wsgi_app()
# #     server = make_server('0.0.0.0', 6543, app)
# #     print("Serving on http://0.0.0.0:6543...")
# #     server.serve_forever()
# from wsgiref.simple_server import make_server
# from pyramid.config import Configurator
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.sql import func
# from pyramid.view import view_config
# from pyramid.response import Response
#
# Base = declarative_base()
# engine = create_engine('postgresql+psycopg2://postgres:dbpassword@localhost:5435/postgres', echo=True)
# DBSession = scoped_session(sessionmaker(bind=engine))
#
# class Item(Base):
#     __tablename__ = 'items'
#     item_id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
#     description = Column(String(255), nullable=True)
#     category = Column(String(255), nullable=False)
#     condition = Column(String(255), nullable=False)
#
# class Trade(Base):
#     __tablename__ = 'trades'
#     trade_id = Column(Integer, primary_key=True, autoincrement=True)
#     requester_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
#     accepter_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
#     requester_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
#     accepter_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=True)
#     status = Column(Boolean, nullable=False)
#     post_time = Column(DateTime, default=func.now(), nullable=False)
#     accept_time = Column(DateTime, nullable=True)
#
# class User(Base):
#     __tablename__ = 'users'
#     user_id = Column(Integer, primary_key=True, autoincrement=True)
#     email = Column(String(254), nullable=False)
#     username = Column(String(30), nullable=True)
#     password = Column(String(60), nullable=False)
#
# @view_config(route_name='get_items', renderer='json')
# def get_items(request):
#     items = DBSession.query(Item).all()
#     return [{"id": item.item_id, "description": item.description, "category": item.category} for item in items]
#
# @view_config(route_name='add_item', request_method='POST', renderer='json')
# def add_item(request):
#     try:
#         data = request.json_body
#         new_item = Item(
#             user_id=data['user_id'],
#             description=data['description'],
#             category=data['category'],
#             condition=data['condition']
#         )
#         DBSession.add(new_item)
#         DBSession.commit()
#         return {'message': 'Item added successfully', 'id': new_item.item_id}
#     except Exception as e:
#         return Response(json_body={'error': str(e)}, status=400)
#
# @view_config(route_name='add_user', request_method='POST', renderer='json')
# def add_user(request):
#     try:
#         data = request.json_body
#         new_user = User(email=data['email'], username=data.get('username'), password=data['password'])
#         DBSession.add(new_user)
#         DBSession.commit()
#         return {'message': 'User created successfully', 'id': new_user.user_id}
#     except Exception as e:
#         return Response(json_body={'error': str(e)}, status=500)
#
# @view_config(route_name='get_users', renderer='json')
# def get_users(request):
#     users = DBSession.query(User).all()
#     return [{'user_id': user.user_id, 'email': user.email, 'username': user.username} for user in users]
#
# def add_cors_headers_response_callback(event):
#     def cors_headers(request, response):
#         response.headers.update({
#             'Access-Control-Allow-Origin': 'http://localhost:3000',
#             'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
#             'Access-Control-Allow-Headers': 'Authorization,Content-Type',
#             'Access-Control-Allow-Credentials': 'true',
#         })
#     event.request.add_response_callback(cors_headers)
#
# def cors_preflight_view(request):
#     request.response.headers.update({
#         'Access-Control-Allow-Origin': 'http://localhost:3000',
#         'Access-Control-Allow-Methods': 'POST, GET, PUT, DELETE, OPTIONS',
#         'Access-Control-Allow-Headers': 'Content-Type, Accept, Authorization',
#         'Access-Control-Allow-Credentials': 'true',
#     })
#     return request.response
#
#
# if __name__ == '__main__':
#     with Configurator() as config:
#         config.add_subscriber(add_cors_headers_response_callback, 'pyramid.events.NewResponse')
#         config.add_route('cors_preflight', '/cors-preflight')
#         config.add_route('get_items', '/items')
#         config.add_route('add_item', '/items/add')
#         config.add_route('get_users', '/users')
#         config.add_route('add_user', '/users/add')
#         config.add_view(cors_preflight_view, route_name='cors_preflight', request_method='OPTIONS')
#         config.scan()
#         app = config.make_wsgi_app()
#         server = make_server('0.0.0.0', 6543, app)
#         print("Serving on http://0.0.0.0:6543...")
#         server.serve_forever()
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPForbidden
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pyramid.view import view_config
from pyramid.response import Response
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
    requester_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    accepter_item_id = Column(Integer, ForeignKey('items.item_id'), nullable=True)
    status = Column(Boolean, nullable=False)
    post_time = Column(DateTime, default=func.now(), nullable=False)
    accept_time = Column(DateTime, nullable=True)

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
        new_item = Item(
            user_id=data['user_id'],
            description=data['description'],
            category=data['category'],
            condition=data['condition']
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

        config.scan()
        app = config.make_wsgi_app()
        server = make_server('0.0.0.0', 6543, app)
        print("Serving on http://0.0.0.0:6543...")
        server.serve_forever()
