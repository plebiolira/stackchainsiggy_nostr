import json
import datetime
# from python_nostr_package.nostr import PrivateKey, PublicKey
# from post_note import *

def append_json(event_msg: json):
  print('running append_json')
  # print(event_msg)
  with open('events.json','r+') as f:
    append_event = True
    events = json.load(f)
    for event in events:
      if event[2]['id'] == event_msg[2]['id']:
        print('found id on json, switching append event to false')
        append_event = False
    if append_event == True:
      print('didnt find event on json, appending')
      datetime_event_was_queried = {"datetime_event_was_queried":datetime.datetime.now().isoformat()}
      event_msg.append(datetime_event_was_queried)
      # print(f"event msg event json: {event_msg.event.json}")
      # event_msg.event.json.append(datetime_event_was_queried)
      # event_msg = json.load(event_msg)
      # events.append(event_msg.event.json)
      events.append(event_msg)
      f.seek(0)
      f.write(json.dumps(events, indent=4))