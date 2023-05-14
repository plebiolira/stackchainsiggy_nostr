import time
import uuid
from nostr.event import EventKind
from nostr.relay_manager import RelayManager
from nostr.key import PublicKey
from nostr.filter import Filter, Filters

pub_key = PublicKey.from_npub('npub1ljraxpufmzjnfdvsw0tq9kwnypctwxus8n9w388uhkd8h73pzzlqgmdzfy')
filters = Filters([Filter(authors=[pub_key.hex()], kinds=[EventKind.SET_METADATA])])
subscription_id = uuid.uuid1().hex

relay_manager = RelayManager()
relay_manager.add_relay("wss://relay.snort.social")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_relay("wss://nostr1.current.fyi")
relay_manager.add_relay("wss://relay.current.fyi")
relay_manager.add_relay("wss://relay.nostr.bg")
relay_manager.add_subscription_on_all_relays(subscription_id, filters)

time.sleep(1)

event_msg = relay_manager.message_pool.get_event()
print(event_msg.event.content)
  
relay_manager.close_all_relay_connections()