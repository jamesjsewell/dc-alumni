import os
import json
import tornado.ioloop
import tornado.web
import tornado.log
import tornado.auth
import tornado.escape
import requests

# from oauth2client import client
# from oauth2client import tools
# from oauth2client.client import AccessTokenCredentials

from peewee import *
from dotenv import load_dotenv
from playhouse.db_url import connect
from playhouse.postgres_ext import JSONField
load_dotenv('SECRETS.env')


# DB format for reference
    # CREATE TABLE alum
    #     (id SERIAL NOT NULL,
    #     isAdmin BOOLEAN DEFAULT false,
    #     isActive BOOLEAN DEFAULT true,
    #     fname VARCHAR(100),
    #     lname VARCHAR(100),
    #     email VARCHAR(100),
    #     github VARCHAR(100),
    #     linkedin VARCHAR(100),
    #     portfolio VARCHAR(100),
    #     resume VARCHAR(100),
    #     tag VARCHAR(100),
    #     description VARCHAR(500),
    #     accountId VARCHAR(100),
    #     token JSON)
DB = connect(
  os.environ.get(
    'DATABASE_URL',
    'postgres://postgres:postgres@localhost:5432/dc_alumni' # local
  )
)


PORT = int(os.environ.get('PORT', '8080'))
BASE_URL = os.environ.get('BASE_URL', 'http://local.ericmschow.com:8888/')
AUTH_URL = BASE_URL + 'auth'
SETTINGS = {
    "google_oauth": {
        "key":
            os.environ.get('GOOGLE_ID'),
        "secret":
            os.environ.get('GOOGLE_SECRET')
    },
    "autoreload": True,
    "cookie_secret": os.environ.get('SECRET'),
    "login_url": "/auth"
}

class Alum(Model):
    id = PrimaryKeyField(unique = True)
    fname = CharField()
    lname = CharField()
    github = CharField()
    email = CharField()
    linkedin = CharField()
    portfolio = CharField()
    resume = CharField()
    tag = CharField()
    description = CharField()
    isAdmin = BooleanField()
    isActive = BooleanField()
    accountId = CharField()
    token = JSONField()
    class Meta:
        database = DB

    def to_json(self):
        d = {
            'fname': self.fname,
            'lname': self.lname,
            'github': self.github,
            'email': self.email,
            'linkedin': self.linkedin,
            'portfolio': self.portfolio,
            'resume': self.resume,
            'tag': self.tag,
            'description': self.description,
            'isActive': self.isActive
            # 'date': self.date.format('%h')
        }
        return json.dumps(d)
# with open('static/index.html', 'r') as fh:
    # INDEX = fh.read()

# required for oauth2
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("accountId")

class FrontendHandler(BaseHandler):
    def get(self, uri):
        #self.set_header("Content-Type", 'text/plain')
        with open('static/index.html', 'r') as fh:
            self.write(fh.read())
            # self.write(INDEX)

# for main list
class AlumniHandler(BaseHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", BASE_URL)
        alumni = []
        # call database, selecting all active students and retrieving only information needed on front-end
        results = Alum.select(Alum.fname, Alum.lname, Alum.github, Alum.linkedin, Alum.portfolio, Alum.resume, Alum.tag, Alum.description, Alum.email).where(Alum.isActive == True).dicts()
        # below needed to convert from Peewee rows to actual objects
        # peewee rows cannot be converted to JSON
        for al in results:
            alumni.append(al)

        # TODO: implement server cache for alumni list, maybe have a user modifying their data trigger a db call, or simply store the new data serverside and only refresh it occasionally
        # maybe a better idea would be to store a lastUpdated timestamp
        # and only retrieve data where lastUpdated > most recently retrieved alum's lastUpdated

        # write JSON to browser
        self.write(json.dumps(alumni))

# for individual account
class AlumHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # call database, return one student info linking to user-id
        userString = self.current_user.decode('ascii')
        user = Alum.select().where(Alum.accountId == userString).get()
        # print('AlumHandler user ', user.to_json())
        # write JSON to browser
        self.write(user.to_json())

    @tornado.web.authenticated
    def post(self):
        userString = self.current_user.decode('ascii')
        responses = {}
        for attr in self.request.arguments.items():
            # escape user input! always!
            responses[attr[0]] = tornado.escape.xhtml_escape(self.get_body_argument(attr[0]))
        # update database with new alum info
        q = Alum.update(fname=responses['fname'],
        lname=responses['lname'],
        github=responses['github'],
        linkedin=responses['linkedin'],
        portfolio=responses['portfolio'],
        resume=responses['resume'],
        tag=responses['tag'],
        description=responses['description'],
        isActive=responses['isActive']).where(Alum.accountId == userString)
        q.execute()
        self.redirect('/profile')


class GoogleOAuth2LoginHandler(BaseHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(
                redirect_uri=AUTH_URL,
                code=self.get_argument('code'))
            # print(access)

            user = yield self.oauth2_request(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                access_token=access["access_token"])
            # print(user)

            alum, created = Alum.get_or_create(
                accountId=user['id'],
                defaults={'token': access,
                'fname': user['given_name'],
                'lname': user['family_name'],
                'github': '',
                'linkedin': '',
                'portfolio': '',
                'resume': '',
                'tag': '',
                'description': '',
                'isAdmin': False,
                'isActive': False,
                'accountId': user['id']}
            )
            if not created:
                alum.token = access
                alum.save()

            self.set_secure_cookie("accountId", user['id'])
            self.redirect('profile')

        else:
            yield self.authorize_redirect(
                redirect_uri=AUTH_URL,
                client_id=SETTINGS['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'}
            )

class ProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        with open('static/profile.html', 'r') as fh:
            self.write(fh.read())

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("accountId")
        self.redirect('/')

def make_app():
    return tornado.web.Application([
        #(r"/", MainHandler),
        (r"/api/", AlumniHandler),
        (r"/api/student/", AlumHandler), # for individual profile data requests
        (r"/auth.*", GoogleOAuth2LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/profile", ProfileHandler),
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
        (r"/static/(.*)",
          tornado.web.StaticFileHandler,
          {'path': 'static'}),
        (r"(.*)", FrontendHandler)
    ], **SETTINGS)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(PORT, print('server now running at localhost: ' + str(PORT)))
    tornado.ioloop.IOLoop.current().start()
