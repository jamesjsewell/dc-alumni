import os
import json
import tornado.ioloop
import tornado.web
import tornado.log
import tornado.auth
import requests
from dotenv import load_dotenv
load_dotenv('SECRETS.env')

PORT = int(os.environ.get('PORT', '8080'))

STUDENTSARRAY = [
    {'name': 'Eric Schow', 'tag': 'Full-stack Engineer', 'github': 'http://www.github.com/ericmschow', 'linkedin': 'http://www.linkedin.com/in/ericmschow', 'portfolio': 'http://www.ericmschow.com', 'resume': 'http://www.ericmschow.com/resume.pdf',
    'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'},
    {'name': 'Frank Frankenstein',
    'tag': 'Backend Engineer',
    'description': 'Two exquisite objection delighted deficient yet its contained. Cordial because are account evident its subject but eat. Can properly followed learning prepared you doubtful yet him. Over many our good lady feet ask that. Expenses own moderate day fat trifling stronger sir domestic feelings. Itself at be answer always exeter up do. Though or my plenty uneasy do. Friendship so considered remarkably be to sentiments. Offered mention greater fifteen one promise because nor. Why denoting speaking fat indulged saw dwelling raillery. '},
    {'name': 'John Stevens',
    'tag': 'Front-end Engineer',
    'description': 'Village did removed enjoyed explain nor ham saw calling talking. Securing as informed declared or margaret. Joy horrible moreover man feelings own shy. Request norland neither mistake for yet. Between the for morning assured country believe. On even feet time have an no at. Relation so in confined smallest children unpacked delicate. Why sir end believe uncivil respect. Always get adieus nature day course for common. My little garret repair to desire he esteem. '},
    {'name': 'Steven Wilson',
    'tag': 'Web Developer',
    'description': 'To sorry world an at do spoil along. Incommode he depending do frankness remainder to. Edward day almost active him friend thirty piqued. People as period twenty my extent as. Set was better abroad ham plenty secure had horses. Admiration has sir decisively excellence say everything inhabiting acceptance. Sooner settle add put you sudden him. '}
]

# with open('static/index.html', 'r') as fh:
    # INDEX = fh.read()

class FrontendHandler(tornado.web.RequestHandler):
    def get(self, uri):
        #self.set_header("Content-Type", 'text/plain')
        with open('static/index.html', 'r') as fh:
            self.write(fh.read())
            # self.write(INDEX)

class AlumniHandler(tornado.web.RequestHandler):
    def get(self):
        # call database
        # write JSON to server
        self.set_header("Access-Control-Allow-Origin", f"http://local.ericmschow.com:{PORT}")
        self.write(json.dumps(STUDENTSARRAY))

class AlumHandler:
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
        (r"/api/", AlumniHandler),
        (r"/api/student", AlumHandler), # for updates
        (r"/auth", AuthHandler),
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),
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
