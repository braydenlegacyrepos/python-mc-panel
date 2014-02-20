__author__ = 'brayden'

from tornado.web import asynchronous
from tornado.web import authenticated
from Handlers.Admin.Ajax.Base import BaseAdminAjaxHandler


class DeleteUserHandler(BaseAdminAjaxHandler):
    @asynchronous
    @authenticated
    def post(self):
        if 'user' in self.request.arguments:
            try:
                self.application.db.delete_user(self.get_argument('user'))
                self.application.generate_username_cache()
                self.finish({'result': {'success': True, 'message': 'User was successfully removed.'}})
            except Exception as e:
                self.finish({'result': {'success': False, 'message': e.message}})
        else:
            self.finish({'result': {'success': False, 'message': 'Required arguments not specified.'}})