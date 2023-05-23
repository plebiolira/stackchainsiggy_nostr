from python_nostr_package.nostr import Filter, Filters
from python_nostr_package.nostr import EventKind
from python_nostr_package.nostr import ClientMessageType
from python_nostr_package.nostr import RelayManager
from python_nostr_package.nostr import PublicKey
import uuid
import json
import time
import ssl


def query_user_display_name(author_pubkey):

  subscription_id = uuid.uuid1().hex

  #query metadata from npub
  filters = Filters([Filter(authors=[author_pubkey], kinds=[EventKind.SET_METADATA])])

  request = [ClientMessageType.REQUEST, subscription_id]
  request.extend(filters.to_json_array())

  relay_manager = RelayManager()
  with open('relay_list.txt', 'r') as f:
      for line in f:
          relay_manager.add_relay(line.strip())
  relay_manager.add_subscription(subscription_id, filters)
  relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
  time.sleep(1.25) # allow the connections to open
  message = json.dumps(request)
  relay_manager.publish_message(message)
  time.sleep(1) # allow the messages to send

  display_name = "no display name"
  while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    display_name = event_msg.event.json[2]['content']
    display_name = display_name[display_name.find('"name":"')+8:]
    display_name = display_name[:display_name.find('","')-1]
    # print("|"+display_name+"|")
    # print(f"display name is {display_name}")

  relay_manager.close_connections()
  return display_name

if __name__=="__main__":
   query_user_display_name(PublicKey.from_npub("npub1h34n29f3wqvcht0jyhnd36jxcdmljyqjv4vdjfrd69nhxhrdvvnsgwr4h0").hex())