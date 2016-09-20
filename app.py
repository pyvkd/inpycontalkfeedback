import falcon
import sqlite3
import json

from jinja2 import Environment, PackageLoader
# import requests
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
        if req.params.get('time', None):
            nows = req.params.get('time')
        else:
            nows = str(datetime.datetime.now() - datetime.timedelta(minutes=5))
        con = sqlite3.connect('example.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        Query1 = """SELECT id, title, speaker FROM Talk WHERE start_time <= Datetime(?) AND end_time >= Datetime(?)"""
        Query1data = (nows, nows)
        Query2 = """SELECT id, titlte, speaker FROM Talk"""
        try:
            with con:
                cur = con.execute(Query1, Query1data)
                master_response['current_talks'] = cur.fetchall()
                cur = con.execute(Query2)
                master_response['all_talks'] = cur.fetchall()
                resp_status = falcon.HTTP_200
        except Exception as e:
            master_response['error'] = "Error %s. Kindly Inform about this to any volunteer @ Pycon India 2016." % str(e)
            resp_status = falcon.HTTP_502
        template = env.get_template('index.html')
        resp.status = resp_status


class Feedback:
    def on_get():
        pass

    def on_post():
        pass


class AdminTalk:
    def on_get():
        pass

    def on_post():
        pass


app = falcon.API()

# Routing
home = Home()
feedback = Feedback()
admin_talk = AdminTalk()

app.add_route('/', home)
app.add_route('/talk/<id>/', feedback)
app.add_route('/admin/talk/', admin_talk)
app.add_route('/admin/talk/<id>/', admin_talk)
