import json
import ssl
import time
from python_nostr_package.nostr import RelayManager
from python_nostr_package.nostr import PublicKey, PrivateKey
# from python_nostr import RelayManager
# from python_nostr import PublicKey, PrivateKey
# from nostr.relay_manager import RelayManager
# from nostr.key import PublicKey
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from post_note import *
from set_query_filters import *
import os
import time

def timer(func):
    def wrapper():
        before = time.time()
        func()
        print("check_json function took: ", time.time() - before, "seconds")
    
    return wrapper

def main(public_key, since=0, to_post_note=True):
  #adding the row below temporarily
  # since = int(datetime.datetime.fromisoformat("2023-01-01").timestamp())

  request, filters, subscription_id = set_query_filters(public_key, since)

  print(request, filters)
  relay_manager = RelayManager()
  # relay_manager.add_relay("wss://nostr-pub.wellorder.net")
  relay_manager.add_relay("wss://relay.damus.io")
  # relay_manager.add_relay("wss://relay.snort.social")
  # relay_manager.add_relay("wss://nostr1.current.fyi")
  # relay_manager.add_relay("wss://relay.current.fyi")
  # relay_manager.add_relay("wss://relay.nostr.bg")
  relay_manager.add_subscription(subscription_id, filters)
  relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
  time.sleep(1.25) # allow the connections to open
  message = json.dumps(request)
  relay_manager.publish_message(message)
  time.sleep(1) # allow the messages to send

  while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    print("\n\n___________NEW_EVENT__________")
    print(f"{event_msg}\n")
    print(event_msg.event.content)
    print(f"created_at: {event_msg.event.created_at}")
    print(f"created at ISO: {datetime.datetime.fromtimestamp(event_msg.event.created_at)}")
    print(f"event.tags: {event_msg.event.tags}")
    print(f"event.kind: {event_msg.event.kind}")
    # print(event_msg.event.public_key)
    # print(event_msg.event.signature)
    print(f"event.id: {event_msg.event.id}")
    print(f"event.json: {event_msg.event.json}")
    print(f"event.json[2]['id']: {event_msg.event.json[2]['id']}")

    #keeping connection to relay open to see if it sustains
    # with open('events.json','r+') as f:
    #   append_event = True
    #   events = json.load(f)
    #   for event in events:
    #     if event[2]['id'] == event_msg.event.id:
    #       print('found id on json, switching append event to false')
    #       append_event = False
    #   if append_event == True:
    #     print('didnt find event on json, appending')
    #     datetime_event_was_queried = {"datetime_event_was_queried":datetime.datetime.now().isoformat()}
    #     # print(f"event msg event json: {event_msg.event.json}")
    #     event_msg.event.json.append(datetime_event_was_queried)
    #     events.append(event_msg.event.json)
    #     f.seek(0)
    #     f.write(json.dumps(events, indent=4))

        # private_key = PrivateKey()
        # if to_post_note == True:
        #   post_note(private_key.from_nsec("nsec1zajhm4ejm9sf50dc88eyex4myqf9wt8ru2d46wjs72am9w0t89yqmamg3e"), "content todo", [["e",event_msg.event.id],["p",public_key]])
        #   pass
  
 
  # relay_manager.close_connections()

@timer
def check_json_for_new_notes():
  
  if os.stat('last_time_checked.json').st_size == 0 or os.stat('last_time_checked.json').st_size == 2:
    with open('last_time_checked.json','w') as f:
      f.write("[]")
      times_checked = []
      times_checked.append(datetime.datetime.now().timestamp())
      f.seek(0)
      f.write(json.dumps(times_checked, indent=4))

  with open('last_time_checked.json', 'r') as f:
    times_checked = json.load(f)
    last_time_checked = times_checked[len(times_checked)-1]
 
  with open('events.json', 'r') as f:
    events = json.load(f)
    for event in events:
      if datetime.datetime.fromisoformat(event[3]['datetime_event_was_queried']).timestamp() > last_time_checked:
        print("new event found on json")
        # post_note(PrivateKey.from_nsec("nsec1zajhm4ejm9sf50dc88eyex4myqf9wt8ru2d46wjs72am9w0t89yqmamg3e"), "content todo", [["e",event[2]['id']]])
        post_note(PrivateKey.from_nsec("nsec1zajhm4ejm9sf50dc88eyex4myqf9wt8ru2d46wjs72am9w0t89yqmamg3e"), "content todo", [["e",event[2]['id']],["p",event[2]['pubkey']]])
  
  with open('last_time_checked.json', 'r+') as f:
    times_checked = json.load(f)
    times_checked.append(datetime.datetime.now().timestamp())
    f.seek(0)
    f.write(json.dumps(times_checked, indent=4))

  last_time_checked = datetime.datetime.now().timestamp()
  return last_time_checked

if __name__ == "__main__":
  try:
    os.remove('events.json')
  except: 
    pass
  time.sleep(0.5)
  with open('events.json','w') as f:
    pass
  time.sleep(0.5)
  if os.stat('events.json').st_size == 0:
    with open('events.json','w') as f:
      f.write("[]")
  with open('events.json','r') as f:
    events = json.load(f)
    if events == []:
      # since = int(datetime.datetime.fromisoformat(input("Won't reply to events queried on the initial run. What date would you like to start querying at? (yyyy-mm-dd) ")).timestamp())
      since = int(datetime.datetime.fromisoformat("2023-01-01").timestamp())
    else:
      since = int(datetime.datetime.fromisoformat(events[-1+len(events):][0][3]['datetime_event_was_queried']).timestamp())

  public_key = PublicKey.from_npub("npub1x2v0vnn059dv3ep9h45lwfgdnynl9nseqsg7safkrrqdc6va3c2qs0kkjg").hex()

  main(public_key, since=since, to_post_note=False)

  # scheduler = BlockingScheduler()
  # print('\nstarting scheduler')
  # scheduler.add_job(main, 'interval', seconds=10, args=[public_key])
  # scheduler.start()

  with open('last_time_checked.json', 'w') as f:
    pass

  # scheduler = BackgroundScheduler()
  scheduler = BlockingScheduler()
  # scheduler.add_job(check_json_for_new_notes, 'interval', seconds=5)
  scheduler.add_job(check_json_for_new_notes, 'interval', seconds=5)
  print('\nstarting scheduler')
  scheduler.start()  