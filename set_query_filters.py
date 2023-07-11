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

def set_query_filters(since, type_of_query, query_term):

  if since == 0:
    with open('events.json','r') as f:
      events = json.load(f)
      since = int(datetime.datetime.fromisoformat(events[-1+len(events):][0][3]['datetime_event_was_queried']).timestamp())

  subscription_id = uuid.uuid1().hex

  if type_of_query == "hashtag":
    # query list of events since specific date - 
    # bot's default functionality - commented out temporarily to build stackjoin
    filter = Filter(kinds=[EventKind.TEXT_NOTE], since=since)
    filter.add_arbitrary_tag("#t",[query_term])
    filters = Filters([filter])
  if type_of_query == "user_tag":
    filter = Filter(kinds=[EventKind.TEXT_NOTE], since=since)
    filter.add_arbitrary_tag("#p",[[query_term]])
    filters = Filters([filter])
  elif type_of_query == "individual_event":
    # query a specific event from relays, based on event_id hex
    filters = Filters([Filter(event_ids=[query_term])])
  elif type_of_query == "npub":
    # query all events from a npub. npub is a list.
    print("npub query")
    filters = Filters([Filter(authors=[query_term], kinds=[EventKind.TEXT_NOTE])])

  # setting filters

  # query all events from a npub. npub is a list.
  # filters = Filters([Filter(authors=[public_key], kinds=[EventKind.TEXT_NOTE])])

  # query events since and until specific dates
  # filters = Filters([Filter(authors=[public_key], kinds=[EventKind.TEXT_NOTE], since=1683602000, until=1676091000)])

  request = [ClientMessageType.REQUEST, subscription_id]
  request.extend(filters.to_json_array())
  # print(filters)
  return request, filters, subscription_id