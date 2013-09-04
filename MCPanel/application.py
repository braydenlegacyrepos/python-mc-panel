__author__ = 'brayden'

import tornado.web
import tornado
import os
import hashlib
import MCPanel.Database.database
from Config import config
from Handlers.Index import IndexHandler
from Handlers.Login import LoginHandler
from Handlers.Ajax.PerformLogin import PerformLoginHandler
from Handlers.Logout import LogoutHandler


class Application(tornado.web.Application):
    def __init__(self):
        self.config = config()
        self.db = MCPanel.Database.database.Database()
        self.sessionCache = {}
        handlers = [
            (r'/', IndexHandler),
            (r'/login', LoginHandler),
            (r'/ajax/performLogin', PerformLoginHandler),
            (r'/logout', LogoutHandler),
        ]
        settings = dict(
            debug=False,
            gzip=True,
            login_url='/login',
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
        )
        tornado.web.Application.__init__(self, handlers, **settings)

    def acl(self, required_access, current_user, server_id):
        user_perms = ['test', 'perm1']
        for access in user_perms:
            if access in required_access:
                break
        else:
            raise tornado.web.HTTPError(403)

    def makeSession(self, username):
        session = hashlib.sha256(os.urandom(32)).hexdigest()
        self.sessionCache[username] = session
        self.db.insertSession(username, session)
        return session

    def checkSession(self, username, session):
        if 'username' in self.sessionCache:
            if self.sessionCache[username] == session:
                return True
            else:
                return False
        else:  # not cached, due to daemon restart? fallback onto more expensive method
            if self.db.getSession(username) == session:
                self.sessionCache[username] = session  # push it into the cache
                return True
            else:
                return False