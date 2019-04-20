import pickle
import secrets

from flask.sessions import SessionInterface
from flask.sessions import SessionMixin
from werkzeug.datastructures import CallbackDict
from redis import Redis


class RedisSession(CallbackDict, SessionMixin):
    """Redis Session
    """

    def __init__(self, initial=None, sid=None, permanent=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        if permanent:
            self.permanent = permanent
        self.modified = False


class RedisSessionInterface(SessionInterface): 
    """Redis Session Interface

    Usage:
        app = Flask(__name__)
        app.session_interface = RedisSessionInterface(app.config)

    :param config: App configuration
    :param redis: Redis instance
    :param serializer: Default: pickle

    Config:
        - SESSION_REDIS_HOST
        - SESSION_REDIS_PORT
        - SESSION_REDIS_PASSWORD
        - SESSION_REDIS_PREFIX
        - SESSION_PERMANENT
    """

    session_class = RedisSession

    def __init__(self, config, redis=None, serializer=pickle):
        if redis is None:
            redis = Redis(
                host=config.get('SESSION_REDIS_HOST', 'localhost'),
                port=config.get('SESSION_REDIS_PORT', 6379),
                password=config.get('SESSION_REDIS_PASSWORD', ''))

        self.redis = redis
        self.config = config
        self.serializer = serializer
        self.prefix = self.config.get('SESSION_REDIS_PREFIX', '')
        self.permanent = self.config.get('SESSION_PERMANENT', True)


    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = secrets.token_hex(64)
            # Avoid same sid, make sid unique
            while self.redis.get(self.prefix + sid):
                sid = secrets.token_hex(64)
            return self.session_class(sid=sid, permanent=self.permanent)
        
        val = self.redis.get(self.prefix + sid)
        
        if not val:
            return self.session_class(sid=sid, permanent=self.permanent)
        else:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid, permanent=self.permanent)

        
    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)

        if not session:
            if session.modified:
                self.redis.delete(self.prefix + session.sid)
                response.delete_cookie(
                    app.session_cookie_name,
                    domain=domain,
                    path=path
                )

            return

        if not session.sid:
            session.sid = secrets.token_hex(64)

        self.redis.set(self.prefix + session.sid, self.serializer.dumps(session))

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        samesite = self.get_cookie_samesite(app)
        expires = self.get_expiration_time(app, session)
        response.set_cookie(
            app.session_cookie_name,
            session.sid,
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure,
            samesite=samesite
        )
