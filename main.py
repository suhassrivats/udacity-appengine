import webapp2

form = """
    <form method="post">
        Hey!When is your Birthday?
        <br><br>
        <label>Month
            <input type="text" name="month">
        </label>
        <label>Day
            <input type="text" name="day">
        </label>
            <label>Year
            <input type="text" name="year">
        </label>
            <div style="color: red">%(error)s</div>
            <br><br>
        <input type="submit">
    </form>
"""

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

# month function


def valid_month(month):
    if month:
        cap_month = month.capitalize()
        if cap_month in months:
            return cap_month

# day function


def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day

# year function


def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year > 1900 and year < 2016:
            return year


class MainPage(webapp2.RequestHandler):

    def write_form(self, error=""):
        self.response.out.write(form % {"error": error})

    def get(self):
        self.write_form()

    def post(self):
        user_month = valid_month(self.request.get('month'))
        user_day = valid_day(self.request.get('day'))
        user_year = valid_year(self.request.get('year'))
        if not (user_month and user_day and user_year):
            self.write_form("Thats not valid data")
        else:
            # self.response.out.write("Thats a valid day")
            self.redirect("/thanks")


class ThanksHandler(webapp2.RequestHandler):

    def get(self):
        self.response.out.write("Thanks. That was a totally valid day!")

app = webapp2.WSGIApplication(
    [('/', MainPage), ('/thanks', ThanksHandler)],
    debug=True,
)
