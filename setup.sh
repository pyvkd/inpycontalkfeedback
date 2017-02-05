#!/bin/bash
SCHEMA_TALK="create table talk(id integer primary key,start_time timestamp, end_time timestamp, title text, speaker text, room text, type integer, talk_link text, speaker_link text,speaker_image text);"
SCHEMA_FEEDBACK="create table feedback(id integer primary key, created_on timestamp, rating integer, comment text, email text,talk_id integer,talk_type integer,talk_title text,talk_speaker text);"
mkdir sqlite3db
echo $SCHEMA_TALK | sqlite3 sqlite3db/feedback.db
echo $SCHEMA_FEEDBACK | sqlite3 sqlite3db/feedback.db
virtualenv venv
source venv/bin/activate && pip install -r requirements.txt