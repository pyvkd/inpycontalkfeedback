import falcon
import sqlite3

from jinja2 import Environment, PackageLoader
import datetime


# Jinja enviorment Create
env = Environment(loader=PackageLoader('app', 'templates'))


class Home:
    """Home page for project.
    Shows Talks that are currently going on with an offset of 10mins to the
    schedule. Also gives an option for selecting a talk for giving a feedback.
    Also a basic form for Open Feedback for Pycon India 2016.
    """
    def on_get(self, req, resp):
        resp_status = None
        master_response = {}
        if req.get_param('time', None):
            nows = req.get_param('time')
        else:
            nows = str(datetime.datetime.now() - datetime.timedelta(minutes=5))
        con = sqlite3.connect('pyconfeedback.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        Query1 = """SELECT id, title, speaker, room FROM Talk WHERE start_time <= Datetime(?) AND end_time >= Datetime(?)"""
        Query1data = (nows, nows)
        Query2 = """SELECT id, title, speaker, room FROM Talk"""
        try:
            with con:
                cur = con.execute(Query1, Query1data)
                master_response['current_talks'] = cur.fetchall()
                cur = con.execute(Query2)
                l = cur.fetchall()
                master_response['all_talks'] = [x for x in l if ((x[1]) and ('Breakfast' not in x[1]) and ('Lunch' not in x[1]) and ('Feedback' not in x[1]) and (x[1].strip() == '-'))]
                resp_status = falcon.HTTP_200
        except Exception as e:
            master_response['error'] = "Error %s. Kindly Inform about this to any volunteer @ Pycon India 2016." % str(e)
            resp_status = falcon.HTTP_502
        template = env.get_template('index.html')
        resp.status = resp_status
        resp.body = template.render(master_response=master_response)
        resp.content_type = "text/html"


class Feedback:
    """
    Shows a form for a talk specific feedback
    """
    def on_get(self, req, resp, talk_id):
        resp_status = None
        master_response = {}
        Query1 = """SELECT title, speaker, room FROM Talk WHERE id = %d""" % int(talk_id)
        con = sqlite3.connect('pyconfeedback.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        try:
            with con:
                cur = con.execute(Query1)
                master_response['item'] = cur.fetchone()
                master_response['talk_id'] = talk_id
                print master_response
                resp_status = falcon.HTTP_200
        except Exception as e:
            master_response['error'] = "Error %s. Kindly Inform about this to any volunteer @ Pycon India 2016." % str(e)
            resp_status = falcon.HTTP_502
        template = env.get_template('talk.html')
        resp.status = resp_status
        resp.body = template.render(master_response=master_response)
        resp.content_type = "text/html"

    def on_post(self, req, resp, talk_id):
        resp_status = None
        master_response = {}
        print req.params
        Query1data = (req.get_param('email'), req.get_param_as_int('rating'), str(datetime.datetime.now()), int(talk_id), req.get_param('comment') )
        master_response = {}
        print Query1data
        Query1 = """INSERT INTO feedback(email, rating, created_on, talk_id, comment) values(?, ?, ?, ?, ?)"""
        con = sqlite3.connect('pyconfeedback.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        try:
            with con:
                con.execute(Query1, Query1data)
                con.commit()
                resp_status = falcon.HTTP_200
        except Exception as e:
            master_response['error'] = "Error %s. Kindly Inform about this to any volunteer @ Pycon India 2016." % str(e)
            resp_status = falcon.HTTP_502
        template = env.get_template('talkpost.html')
        resp.status = resp_status
        resp.body = template.render(master_response=master_response)
        resp.content_type = "text/html"


class AdminTalk:
    def on_get():
        pass

    def on_post():
        pass


# reqwrapper = falcon.RequestOptions()
# reqwrapper.auto_parse_form_urlencoded = True
app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True
# Routing
home = Home()
feedback = Feedback()
admin_talk = AdminTalk()

app.add_route('/', home)
app.add_route('/talk/{talk_id}/', feedback)
app.add_route('/admin/talk/', admin_talk)
app.add_route('/admin/talk/{talk_id}/', admin_talk)
