import os
import json
import tornado.ioloop
import tornado.web
import tornado.log
import tornado.auth
import requests

from oauth2client import client
from oauth2client import tools
from oauth2client.client import AccessTokenCredentials

from peewee import *
from dotenv import load_dotenv
from playhouse.db_url import connect
load_dotenv('SECRETS.env')


# DB format for reference
    # CREATE TABLE alum
    #     (id SERIAL NOT NULL,
    #     isAdmin BOOLEAN DEFAULT false,
    #     isActive BOOLEAN DEFAULT true,
    #     fname VARCHAR(100),
    #     lname VARCHAR(100),
    #     github VARCHAR(100),
    #     linkedin VARCHAR(100),
    #     portfolio VARCHAR(100),
    #     resume VARCHAR(100),
    #     tag VARCHAR(100),
    #     description VARCHAR(500))
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
    linkedin = CharField()
    portfolio = CharField()
    resume = CharField()
    tag = CharField()
    description = CharField()
    isAdmin = BooleanField()
    isActive = BooleanField()
    class Meta:
        database = DB

# with open('static/index.html', 'r') as fh:
    # INDEX = fh.read()

class FrontendHandler(tornado.web.RequestHandler):
    def get(self, uri):
        #self.set_header("Content-Type", 'text/plain')
        with open('static/index.html', 'r') as fh:
            self.write(fh.read())
            # self.write(INDEX)

# for main list
class AlumniHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", BASE_URL)
        alumni = []
        # call database, selecting all active students
        results = Alum.select().where(Alum.isActive == True).dicts()
        # below needed to convert from Peewee rows to actual objects
        # peewee rows cannot be converted to JSON
        for al in results:
            alumni.append(al)

        # TODO: implement server cache for alumni list, maybe have a user modifying their data trigger a db call, or simply store the new data serverside and only refresh it occasionally

        # write JSON to server
        self.write(json.dumps(alumni))

# for individual account
class AlumHandler(tornado.web.RequestHandler):
    def get(self):
        # check if logged in
        # @tornado.web.authenticated
            # if not logged in, redirect to login
        # call database, return one student info
        pass
        # cache

    def post(self):
        # update database with new student info
        pass

class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(
                redirect_uri=AUTH_URL,
                code=self.get_argument('code'))
            print(access)
            # Save the user with e.g. set_secure_cookie

            user = yield self.oauth2_request(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                access_token=access["access_token"])
            print(user)

            # alum, created = Alum.get_or_create(
            #     user_id=user['id'],
            #     user_email=user['email'],
            #     defaults={'name': user['name'], 'token': access}
            # )
            # if not created:
            #     alum.token = access
            #     alum.save()

            # print("here is the user info:", user)
            self.set_secure_cookie("user-id", user['id'])
            print('Cookie set!')
            self.redirect('profile', {})

        else:
            yield self.authorize_redirect(
                redirect_uri=AUTH_URL,
                client_id=SETTINGS['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'}
                )
class ProfileHandler(tornado.web.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        self.write('hello')

def make_app():
    return tornado.web.Application([
        #(r"/", MainHandler),
        (r"/api/", AlumniHandler),
        (r"/api/student", AlumHandler), # for updates
        (r"/auth.*", GoogleOAuth2LoginHandler),
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
