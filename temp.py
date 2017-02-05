for table in tabledict:
    for key in table:
        abc += "CREATE TABLE %s (" % key
        for k in table[key]:
            abc += "%s %s," % (k, table[key][k])
        abc += ");\n"
schedule_list = json.load(open('schedule.json', 'r'))
event_list = []
i = 1
for item in schedule_list:
    for eachtalk in item['events']:
        talk = {'speaker': eachtalk["speaker"], 'start_time': eachtalk['time'].split('-')[0] + " %s"%item['date'], 'end_time': eachtalk['time'].split('-')[1]  + " %s"%item['date'], 'room': eachtalk['location'],'title': eachtalk['title'] ,'id': i}
        i = i + 1
        event_list.append(talk)
        print item['id'], item['date'], eachtalk




import datetime

for event in event_list:
    try:
        event['start_time_bck'] = event["start_time"]
        s = str(datetime.datetime.strptime(event['start_time'].strip(), "%I:%M %p %B %d, %Y")) + '.000'
        event['start_time'] = s
    except:
        s = str(datetime.datetime.strptime(event['start_time'].strip(), "%I.%M %p %B %d, %Y")) + '.000'
        event['start_time'] = s
    try:
        event['end_time_bck'] = event["end_time"]
        s = str(datetime.datetime.strptime(event['end_time'].strip(), "%I:%M %p %B %d, %Y")) + '.000'
        event['end_time'] = s
    except:
        s = str(datetime.datetime.strptime(event['end_time'].strip(), "%I.%M %p %B %d, %Y")) + '.000'
        event['end_time'] = s


for event in event_list:
    con.execute("insert into Talk(speaker, start_time, end_time, room, title) values(?, ?, ?, ?, ?)", (event['speaker'], event['start_time'], event['end_time'], event['room'], event['title']))


tx = "select id as id, title as title, speaker as speaker from Talk WHERE start_time >= %s and end_time <= %s" %(nows, nows)

Datetime('2016-09-24 08:45:00.000')


tx = """SELECT id as id, title as title, speaker as speaker FROM Talk WHERE start_time <= Datetime(?) AND end_time >= Datetime(?)"""
other = (nows, nows)
cur = conn.execute(tx, other)