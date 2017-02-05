# inpycontalkfeedback
Small falcon app for Getting feedback for talks at the conference.

# 1.Setup

Talk Type :
0: default 
1: workshops
2: talks
3: openspaces
4: lightningtalks

## 1.1 For local development

Project depends on the following:
python 2.7 
falcon (minimalistic web framework in python)
sqlite3 (database)


Schedule Format for preparing sqllite database:

[{"title": "talk title", "start_time": "datetime in isoformat", "end_time": "datetime in isoformat", "speaker": "Speaker Name", "room": "Room Name", "talk_type": [0-4] }, ... ]

*to be stored in fixtures.json

Run the following:

./setup.sh

*this shell script create sqlite3db folder, create a dbfile in that folder, create virtualenv named venv, install all the libs in requirments.txt

Run the following:

source venv/bin/activate
python preparedb.py