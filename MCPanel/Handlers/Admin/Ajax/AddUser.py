__author__ = 'brayden'

from tornado.web import asynchronous
from tornado.web import authenticated
from Base import BaseAdminAjaxHandler


class AddUserHandler(BaseAdminAjaxHandler):
    @asynchronous
    @authenticated
    def post(self):
        self.if_admin()
        self.set_header('Content-Type', 'text/json')
        if all(k in self.request.arguments for k in ("username", "password", "is_admin")):
            try:
                if self.get_argument('is_admin') == 'true':
                    is_admin = True
                else:
                    is_admin = False
                self.application.db.addUser(self.get_argument('username'), self.get_argument('password'),
                                            is_admin=is_admin)
                self.finish({'result': {'success': True, 'message': 'User was successfully created.'}})
            except Exception as e:
                self.finish({'result': {'success': False, 'message': str(e)}})
        else:
            self.finish({'result': {'success': False, 'message': 'Required arguments not specified.'}})