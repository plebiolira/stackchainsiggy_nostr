import ssl
import time
from python_nostr_package.nostr import Event
from python_nostr_package.nostr import RelayManager
from python_nostr_package.nostr import PrivateKey
# from python_nostr import Event
# from python_nostr import RelayManager
# from python_nostr import PrivateKey
# from nostr.event import Event
# from nostr.relay_manager import RelayManager
# from nostr.key import PrivateKey
import random

def post_note(private_key, content, tags):
    relay_manager = RelayManager()
    # relay_manager.add_relay("wss://relay.nostr.bg")
    relay_manager.add_relay("wss://relay.damus.io")
    # relay_manager.add_relay("wss://relay.snort.social")
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
    time.sleep(1.25) # allow the connections to open

    # event = Event(private_key.public_key.hex(), "Hey there " + str(random.randint(3, 9000)), tags=tags)
    event = Event(private_key.public_key.hex(), "🤖 Stackjoin Recorded to the Mempool ☑️!\n(Siggy still in alpha, bug smashing, mode). 🤖 ["+str(random.randint(3, 90000))+"]", tags=tags)
    # event = Event(private_key.public_key.hex(), "Hey there " + str(random.randint(3, 9000)))
    private_key.sign_event(event)

    relay_manager.publish_event(event)
    print("note sent")
    time.sleep(1)

    relay_manager.close_connections()