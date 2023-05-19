# stackchainsiggy_nostr

This is the version made for Nostr for the Stackchain mascot that monitors for #stackjoin buys. 

I had to incorporate Jeff Thibault's Nostr-Python library and its dependencies into the package because of version discrepancies on pip and github, and also because I had to make a few changes to the Nostr library code to facilitate the bot's functionality.

Incorporated Monstr's hex_to_bech32 method into PublicKey class.

Credits: Jeff Thibault, Pieter Wuille, Monty888