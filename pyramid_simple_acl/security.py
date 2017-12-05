GROUPS = {'admin': ['group:admin']}
USERS = {'receptionist' : 'receptionist'}

def groupfinder(userid, request):
	return ['group:admin']

from pyramid.security import Allow, Everyone

class Root(object):
	def __acl__(self):
		return [(Allow, Everyone, 'view'), (Allow, 'group:admin', 'edit')]

	def __init__(self, request):
		pass
