from python_nostr_package.nostr import Filter, Filters
from python_nostr_package.nostr import Event, EventKind
from python_nostr_package.nostr import ClientMessageType
from python_nostr_package.nostr import PublicKey
# from python_nostr import Filter, Filters
# from python_nostr import Event, EventKind
# from python_nostr import ClientMessageType
# from nostr.filter import Filter, Filters
# from nostr.event import Event, EventKind
# from nostr.message_type import ClientMessageType
import datetime
import uuid
import json

def set_query_filters(public_key, since):

  if since == 0:
    with open('events.json','r') as f:
      events = json.load(f)
      since = int(datetime.datetime.fromisoformat(events[-1+len(events):][0][3]['datetime_event_was_queried']).timestamp())

  subscription_id = uuid.uuid1().hex

  # setting filters

  # query all events from a npub. npub is a list.
  # filters = Filters([Filter(authors=[public_key], kinds=[EventKind.TEXT_NOTE])])

  # query events since and until specific dates
  # filters = Filters([Filter(authors=[public_key], kinds=[EventKind.TEXT_NOTE], since=1683602000, until=1676091000)])

  # query list of events since specific date - 
  # bot's default functionality - commented out temporarily to build stackjoin
  filter = Filter(kinds=[EventKind.TEXT_NOTE], since=since)
  filter.add_arbitrary_tag("#t",["stackjoin"])
  filters = Filters([filter])

  # query a specific event from relays, based on event_id
  # filters = Filters([Filter(event_ids=["29053373b9267ce88dc72001ee25c3c6a657ebb46e607467493291eb1ab5201d"])])

  request = [ClientMessageType.REQUEST, subscription_id]
  request.extend(filters.to_json_array())
  # print(filters)
  return request, filters, subscription_id