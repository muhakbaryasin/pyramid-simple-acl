from pyramid.response import Response
from pyramid.view import view_config

from pyramid.security import remember, forget, authenticated_userid

from sqlalchemy.exc import DBAPIError

from ..models import TblUser, TblReservation, TblRoom
from pyramid.httpexceptions import (
    HTTPFound,
    )

import logging
log = logging.getLogger(__name__)

@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    return {'one': 'one', 'project': 'pyramid-simple-acl'}    

@view_config(route_name='logout', renderer='../templates/logout.jinja2')
def logout(request):
        headers = forget(request)
        request.response.headerlist.extend(headers)
        next_url = request.route_url('login')
            
        return HTTPFound(location=next_url)

@view_config(route_name='login', renderer='../templates/login.jinja2')
def login(request):
    try:
        if not ('user_name' in request.params and 'password' in request.params):
            raise Exception('Missing params')
        
        if request.params['user_name'] == '' or request.params['password'] == '':
            raise Exception('Ada inputan yang kosong dari form')

        match_ = request.dbsession.query(TblUser).filter_by(user_name=request.params['user_name'], user_password=request.params['password']).one()
        username = request.params['user_name']
        
        if match_ is not None:
            headers = remember(request, username)
            request.response.headerlist.extend(headers)
            next_url = request.route_url('search-room')
            
            return HTTPFound(location=next_url)
        
    except Exception as e:
        log.exception(str(e))
        return {'code' : 'error', 'message' : str(e) }
    
@view_config(route_name='search-room', renderer='../templates/search-room.jinja2', permission='edit')
def search_room(request):
    try:
        if not ('floor' in request.params):
            raise Exception('Missing params')
        
        if request.params['floor'] == '':
            raise Exception('Ada inputan yang kosong dari form')
        
        query = request.dbsession.query(TblReservation)
        result = query.join(TblRoom, aliased=True).filter_by(room_floor=request.params['floor']).all()
        
        if result is None or len(result) < 1:
            raise Exception("No row found")
        
        return {'code' : 'ok', 'message' : '', 'content' : result }
        
    except Exception as e:
        log.exception(str(e))
        return {'code' : 'error', 'message' : str(e), 'content' : ''}