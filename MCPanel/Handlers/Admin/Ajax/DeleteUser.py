__author__ = 'brayden'

from tornado.web import asynchronous
from tornado.web import authenticated
from Base import BaseAdminAjaxHandler


class DeleteUserHandler(BaseAdminAjaxHandler):
    @asynchronous
    @authenticated
    def post(self):
        self.if_admin()
        self.set_header('Content-Type', 'text/json')
        if 'user' in self.request.arguments:
            try:
                self.application.db.deleteUser(str(self.get_argument('user')))
                self.finish({'result': {'success': True, 'message': 'User was successfully removed.'}})
            except Exception as e:
                self.finish({'result': {'success': False, 'message': e.message}})
        else:
            self.finish({'result': {'success': False, 'message': 'Required arguments not specified.'}})