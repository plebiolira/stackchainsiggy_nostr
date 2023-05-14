from nostr.key import PrivateKey
# import secp256k1

private_key = PrivateKey()
public_key = private_key.public_key
print(f"Private key: {private_key.bech32()}")
print(f"Public key: {public_key.bech32()}")

with open('keys.txt','r+') as f:
    f.write(f"Private key: {private_key.bech32()}\nPublic key: {public_key.bech32()}")
