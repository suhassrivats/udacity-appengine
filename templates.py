import os
import jinja2
import webapp2
import codecs
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):

    def get(self):
        items = self.request.get_all("food")
        self.render('shopping_list.html', items=items)


class FizzBuzzHandler(Handler):

    def get(self):
        n = self.request.get('n', 0)
        if n:
            n = int(n)
        # shortcut for the above statement
        # n = n and int(n)
        self.render('fizzbuzz.html', n=n)


class Rot13(Handler):

    def get(self):
        self.render('rot13.html')

    def post(self):
        text = self.request.get('text')
        if text:
            rot13 = codecs.encode(text, 'rot_13')
        self.render('rot13.html', text=rot13)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return password and PASS_RE.match(password)


def valid_email(email):
    return not email or EMAIL_RE.match(email)


class SignUp(Handler):

    def get(self):
        self.render('signup-form.html')

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username=username,
                      email=email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True

        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)

        else:
            self.redirect('/welcome?username=' + username)


class Welcome(Handler):

    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('signup-form.html')


class Blog(Handler):

    def get(self):
        self.render("blogs.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        params = dict(subject=subject, content=content)

        if subject == "" or content == "":
            params["error"] = "subject and content, please!"
            self.render('/blog/newpost.html', **params)

        else:
            self.redirect('blog.html')

app = webapp2.WSGIApplication(
    [
        ('/', MainPage),
        ('/fizzbuzz', FizzBuzzHandler),
        ('/rot13', Rot13),
        ('/signup', SignUp),
        ('/welcome', Welcome),
        ('/blog', Blog),

    ],
    debug=True,
)
