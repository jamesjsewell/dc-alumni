import os
import tornado.ioloop
import tornado.web
import tornado.log
import tornado.auth
import requests

PORT = int(os.environ.get('PORT', '8080'))

# with open('static/index.html', 'r') as fh:
    # INDEX = fh.read()

class FrontendHandler(tornado.web.RequestHandler):
    def get(self, uri):
        #self.set_header("Content-Type", 'text/plain')
        with open('static/index.html', 'r') as fh:
            self.write(fh.read())
            # self.write(INDEX)

class StudentsHandler(tornado.web.RequestHandler):
    def get(self):
        # call database
        #
        self.write("<p>this is a test</p> <a href='/'>Back home</a>")

class StudentHandler:
    def get(self):
        # call database, return one student info
        pass

    def post(self):
        # update database with new student info
        pass

class AuthHandler:
    def get(self):
        #
        pass
    def post(self):
        # send login info proba
        pass

def make_app():
    return tornado.web.Application([
        #(r"/", MainHandler),
        (r"/api/", StudentsHandler),
        (r"/api/student", StudentHandler),
        (r"/auth", AuthHandler),
        (r"/static/(.*)",
          tornado.web.StaticFileHandler,
          {'path': 'static'}),
        (r"(.*)", FrontendHandler)
    ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(PORT, print('server now running at localhost: ' + str(PORT)))
    tornado.ioloop.IOLoop.current().start()
