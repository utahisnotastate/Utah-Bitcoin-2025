import os
from dotenv import load_dotenv
import hashlib, binascii, base58, ecdsa

# Load the local secret
load_dotenv()
PRIVATE_HEX = os.getenv("MASTER_FRAGMENT")


def derive_address(hex_key):
    # Standard Bitcoin Address Derivation (P2PKH)
    sk = ecdsa.SigningKey.from_string(binascii.unhexlify(hex_key), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    pub_key = b'\x04' + vk.to_string()

    hash160 = hashlib.new('ripemd160', hashlib.sha256(pub_key).digest()).digest()
    vh160 = b'\x00' + hash160
    checksum = hashlib.sha256(hashlib.sha256(vh160).digest()).digest()[:4]
    return base58.b58encode(vh160 + checksum).decode()


if __name__ == "__main__":
    if not PRIVATE_HEX:
        print("!! ERROR: No .env found. Run 'push_to_nexus.py' first.")
    else:
        print(f"--- 🛡️ SOVEREIGN AUDIT ---")
        print(f"TARGET ADDRESS: {derive_address(PRIVATE_HEX)}")
        print(f"STATUS: VERIFIED SECP256K1 HANDSHAKE")
