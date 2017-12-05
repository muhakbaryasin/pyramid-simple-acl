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

class DefaultView(object):
    def __init__(self, request):
        self.request = request
        self.login_ = False
        
        if authenticated_userid(request) is not None:
            self.login_ = True
        
    @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
    def home(self):
        return {'one': 'one', 'project': 'pyramid-simple-acl', 'login' : self.login_}    

    @view_config(route_name='logout', renderer='../templates/logout.jinja2')
    def logout(self):
        headers = forget(self.request)
        self.request.response.headerlist.extend(headers)
        next_url = self.request.route_url('login')
            
        return HTTPFound(location=next_url, headers=headers)

    @view_config(route_name='login', renderer='../templates/login.jinja2')
    def login(self):
        try:
            if not ('user_name' in self.request.params and 'password' in self.request.params):
                return {'login' : self.login_}
        
            if self.request.params['user_name'] == '' or self.request.params['password'] == '':
                raise Exception('Ada inputan yang kosong dari form')

            match_ = self.request.dbsession.query(TblUser).filter_by(user_name=self.request.params['user_name'], user_password=self.request.params['password']).one()
            username = self.request.params['user_name']
            
            if match_ is not None:
                headers = remember(self.request, username)
                self.request.response.headerlist.extend(headers)
                next_url = self.request.route_url('search-room')
                
                return HTTPFound(location=next_url, headers=headers)
                
        except Exception as e:
            log.exception(str(e))
            return {'code' : 'error', 'message' : str(e), 'login' : self.login_}
    
    @view_config(route_name='search-room', renderer='../templates/search-room.jinja2', permission='edit')
    def search_room(self):
        try:
            if not ('floor' in self.request.params):
                return {'login' : self.login_}
            
            if self.request.params['floor'] == '':
                raise Exception('Ada inputan yang kosong dari form')
            
            query = self.request.dbsession.query(TblReservation)
            result = query.join(TblRoom, aliased=True).filter_by(room_floor=self.request.params['floor']).all()
            
            if result is None or len(result) < 1:
                raise Exception("No row found")
            
            return {'code' : 'ok', 'message' : '', 'content' : result, 'login' : self.login_}
            
        except Exception as e:
            log.exception(str(e))
            return {'code' : 'error', 'message' : str(e), 'content' : '', 'login' : self.login_}