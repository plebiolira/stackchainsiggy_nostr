import json
import datetime
import os
import time
# from python_nostr_package.nostr import PrivateKey, PublicKey
# from post_note import *

def timer(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        func(*args, **kwargs)
        print("append_json function took: ", time.time() - before, "seconds")    
    return wrapper

@timer
def append_json(event_msg: json):
  time.sleep(0.3)
  print('\nrunning append_json')
  with open('events.json','r+') as f:
    append_event = True
    events = json.load(f)
    if event_msg[2]['tags'] == []:
      append_event = False
    else:
      for event in events:
        if event[2]['id'] == event_msg[2]['id']:
          print('found id on json or no tags on json, switching append event to false')
          append_event = False
    if append_event == True:
      print('didnt find event on json, appending')
      datetime_event_was_queried = {"datetime_event_was_queried":datetime.datetime.now().isoformat()}
      event_msg[2]['content'] = event_msg[2]['content'].replace("\'","").replace("\"","")
      # print(f"event_msg on append_json is {event_msg}")
      event_msg.append(datetime_event_was_queried)
      # event_msg.event.json.append(datetime_event_was_queried)
      # event_msg = json.load(event_msg)
      if os.path.getsize('events.json') == 2:
        events.append(event_msg)
        f.seek(0)
        f.write(json.dumps(events, indent=4))
      else:
        f.seek(os.path.getsize('events.json')-1)
        f.write(","+str(event_msg).replace("\'","\"").replace("\"","\"")+"]")
        # f.write(","+str(event_msg).translate({39: None,91: None, 93: None, 44: None})+"]")