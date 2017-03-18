import falcon
import sqlite3

from jinja2 import Environment, PackageLoader
import datetime


# Jinja enviorment Create
env = Environment(loader=PackageLoader('app', 'templates'))


# Confs Dictonary
confs = {
    "event": "Pydelhi Conf 2017 Feedback",
    "database": "sqlite3db/feedback.db",
    "token_list": ["done0-query", "dont-mess-upthis"] # update the token_list for live deployment.
}


class Home:
    """Home page for project.
    Shows Talks that are currently going on with an offset of 10mins to the
    schedule. browse to give feedback for a talk, openspace, workshop,
    lightning talk etc. Also a basic form for General Feedback for [Event]
    """
    def on_get(self, req, resp):
        resp_status = None
        master_response = {}
        if req.get_param('time', None):
            print req.get_param('time')
            nows = req.get_param('time')
        else:
            nows = str(datetime.datetime.now() - datetime.timedelta(minutes=5))
        con = sqlite3.connect(confs['database'], detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        Query = """SELECT id, title, talk_link, speaker, speaker_link, speaker_image, room FROM talk WHERE start_time <= Datetime(?) AND end_time >= Datetime(?)"""
        Querydata = (nows, nows)
        try:
            with con:
                cur = con.execute(Query, Querydata)
                master_response['current_talks'] = cur.fetchall()
                resp_status = falcon.HTTP_200
        except Exception as e:
            master_response['error'] = "Error %s. Kindly Inform about this to any volunteer @ %s." % str(e), confs['event']
            resp_status = falcon.HTTP_502
        master_response['event'] = confs['event']
        template = env.get_template('index.html')
        resp.status = resp_status
        resp.body = template.render(master_response=master_response)
        resp.content_type = "text/html"


class Talk:
    """Listing page for talks
    """
    def on_get(self, req, resp, talk_type=None):
        resp_status = None
        master_response = {}
        # Request parameter time added for testing.
        if req.get_param('time', None):
            nows = req.get_param('time')
        else:
            nows = str(datetime.datetime.now() - datetime.timedelta(minutes=5))
        con = sqlite3.connect(confs['database'], detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        Query = """SELECT id, title, speaker, speaker_link, speaker_image, room FROM talk WHERE start_time <= Datetime(?) AND end_time >= Datetime(?) AND type == ?"""
        Querydata = (nows, nows, talk_type)
        Query1 = """SELECT id, title, speaker, speaker_link, speaker_image, room FROM talk WHERE type == ?"""
        Query1data = (talk_type)
        try:
            with con:
                cur = con.execute(Query, Querydata)
                master_response['current_talks'] = cur.fetchall()
                cur = con.execute(Query1, Query1data)
                master_response['all_talks'] = cur.fetchall()
                resp_status = falcon.HTTP_200
        except Exception as e:
            error = "Error %s. Kindly Inform about this to any volunteer @ %s." % (str(e), confs['event'])
            master_response['error'] = error
            resp_status = falcon.HTTP_502
        master_response['event'] = confs['event']
        template = env.get_template('schedule.html')
        resp.status = resp_status
        resp.body = template.render(master_response=master_response)
        resp.content_type = "text/html"


class Feedback:
    """
    Shows a form for a talk specific feedback
    """
    def on_get(self, req, resp, talk_id=None):
        resp_status = None
        master_response = {}
        Query1 = """SELECT title, speaker, room FROM talk WHERE id = %d""" % int(talk_id)
        con = sqlite3.connect(confs['database'], detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        try:
            with con:
                cur = con.execute(Query1)
                master_response['item'] = cur.fetchone()
                master_response['talk_id'] = talk_id
                resp_status = falcon.HTTP_200
        except Exception as e:
            error = "Error %s. Kindly Inform about this to any volunteer @ %s." % (str(e), confs['event'])
            master_response['error'] = error
            resp_status = falcon.HTTP_502
        template = env.get_template('feedback.html')
        master_response['event'] = confs['event']
        resp.status = resp_status
        resp.body = template.render(master_response=master_response)
        resp.content_type = "text/html"

    def on_post(self, req, resp, talk_id=None):
        resp_status = None
        master_response = {}
        Query1data = (req.get_param('name'), req.get_param('email'), req.get_param_as_int('rating'), str(datetime.datetime.now()), int(talk_id), req.get_param('comment'))
        Query1 = """INSERT INTO feedback(name, email, rating, created_on, talk_id, comment) values(?, ?, ?, ?, ?, ?)"""
        con = sqlite3.connect(confs['database'], detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        try:
            with con:
                con.execute(Query1, Query1data)
                con.commit()
                resp_status = falcon.HTTP_200
        except Exception as e:
            error = "Error %s. Kindly Inform about this to any volunteer @ %s." % (str(e), confs['event'])
            master_response['error'] = error
            resp_status = falcon.HTTP_502
        template = env.get_template('feedbackpost.html')
        master_response['event'] = confs['event']
        resp.status = resp_status
        resp.body = template.render(master_response=master_response)
        resp.content_type = "text/html"


class AdminTalk:
    """Admin form for managing talks schedule.
    # to-do
    """
    def on_get(self, req, resp, talk_id=None):
        resp_status = None
        master_response = {}
        if talk_id:
            Query1 = """SELECT * FROM talk WHERE id=?"""
            Query1data = (talk_id)
            con = sqlite3.connect(confs['database'], detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            try:
                with con:
                    cur = con.execute(Query1, Query1data)
                    master_response['item'] = cur.fetchone()
                    master_response['talk_id'] = talk_id
                    resp_status = falcon.HTTP_200
            except Exception as e:
                error = "Error %s. Kindly Inform about this to any volunteer @ %s." % (str(e), confs['event'])
                master_response['error'] = error
                resp_status = falcon.HTTP_502
        else:
            template = env.get_template('admin.html')
            resp_status = falcon.HTTP_200
            master_response['talk_id'] = talk_id
        master_response['event'] = confs['event']
        template = env.get_template('admin.html')
        resp.status = resp_status
        resp.body = template.render(master_response=master_response)
        resp.content_type = "text/html"

    def on_post(self, req, resp, talk_id=None):
        token = req.get_param('token')
        if token in confs['token_list']:
            Query1data = (req.get_param('room'),
                          req.get_param_as_int('type'),
                          req.get_param('start_time'),
                          req.get_param('end_time'),
                          req.get_param('title'),
                          req.get_param('speaker'),
                          req.get_param('speaker_image'),
                          req.get_param('speaker_link'),
                          req.get_param('talk_link')
                          )
            resp_status = None
            master_response = {}
            Query1 = """INSERT INTO talk(room, type, start_time, end_time, title, speaker, speaker_image, speaker_link, talk_link) values(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            con = sqlite3.connect(confs['database'], detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            try:
                with con:
                    con.execute(Query1, Query1data)
                    con.commit()
                    resp_status = falcon.HTTP_200
                master_response['thankyou'] = True
            except Exception as e:
                error = "Error %s. Kindly Inform about this to any volunteer @ %s." % (str(e), confs['event'])
                master_response['error'] = error
                resp_status = falcon.HTTP_502
        else:
            error = "Error: you are not authorised. Kindly Inform about this to any volunteer @ %s." % (confs['event'])
            master_response['error'] = error
            resp_status = falcon.HTTP_403
        master_response['event'] = confs['event']
        template = env.get_template('admin.html')
        resp.status = resp_status
        resp.body = template.render(master_response=master_response)
        resp.content_type = "text/html"


app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True

# Routing
home = Home()
talk = Talk()
feedback = Feedback()
admin_talk = AdminTalk()

app.add_route('/', home)
app.add_route('/talk/{talk_type}/', talk)

app.add_route('/admin/talk/', admin_talk)
app.add_route('/admin/talk/{talk_id}/', admin_talk)

app.add_route('/feedback/{talk_id}/', feedback)
