import os
import webapp2
import jinja2

from google.appengine.api import memcache

from utils import *
        
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def logged_in():
    session = memcache.get(SESSION_KEY)
    if session:
        return session

jinja_env.globals['logged_in'] = logged_in

class Handler(webapp2.RequestHandler):
	def write(self,*args,**kwargs):
		self.response.out.write(*args,**kwargs)
	
	def render_str(self,template,**kwargs):
		t = jinja_env.get_template(template)
		return t.render(kwargs)
		
	def render(self,template,**kwargs):
		self.write(self.render_str(template,**kwargs))
		
class WelcomeHandler(Handler):
    def get(self):
        session = memcache.get(SESSION_KEY)
        if session is None:
            self.redirect('/')
        else:
            self.render('message.html', message = session)
		
class FrontHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/blog')

app = webapp2.WSGIApplication([
    (r'/', FrontHandler),
    (r'/welcome/?', WelcomeHandler),
], debug=True)