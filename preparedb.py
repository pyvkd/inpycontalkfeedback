import sqlite3
import json


def main():
    conn = sqlite3.connection('sqlite3db/feedback.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    mastertalklist = json.load(open('fixtures.json', 'r'))
    for item in mastertalklist:
        query = """INSERT INTO talk(start_time,end_time,title,speaker,room,type,speaker_link,speaker_image) values(?, ?, ?, ?, ?, ?, ?, ?)"""
        querydata = (item['start_time'], item['end_time'], item['title'], item['speaker'], item['room'], item['type'], item['speaker_link'], item['speaker_image'])
        conn.excute(query, querydata)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
