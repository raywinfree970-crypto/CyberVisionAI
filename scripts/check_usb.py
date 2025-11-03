#!/usr/bin/env python3
"""Check a USB drive for the unlock file and decrypt it using the provided password.

Usage:
  python scripts/check_usb.py --drive D: --password "hunter2"

Outputs the unlocked token on success.
"""
import argparse
import os
import json
import base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_key(password: bytes, salt: bytes, iterations: int = 200_000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password)


def check(drive: str, password: str):
    if len(drive) == 2 and drive[1] == ':':
        root = drive + '\\'
    else:
        root = drive

    infile = os.path.join(root, 'cybervision_unlock.bin')
    if not os.path.exists(infile):
        raise SystemExit(f'Unlock file not found at: {infile}')

    with open(infile, 'r', encoding='utf-8') as f:
        payload = json.load(f)

    salt = base64.b64decode(payload['salt'])
    nonce = base64.b64decode(payload['nonce'])
    ciphertext = base64.b64decode(payload['ciphertext'])

    key = derive_key(password.encode('utf-8'), salt)
    aes = AESGCM(key)
    try:
        plaintext = aes.decrypt(nonce, ciphertext, None).decode('utf-8')
    except Exception:
        raise SystemExit('Decryption failed: incorrect password or corrupted file')

    # We store a small JSON document (token and optional ai_key)
    try:
        data = json.loads(plaintext)
        token = data.get('token', '')
        ai_key = data.get('ai_key', '')
    except Exception:
        # If payload is a plain token string (older format), fallback
        token = plaintext
        ai_key = ''

    print('SUCCESS')
    print('Token:', token)
    if ai_key:
        print('AI key present (not printed for security).')
    return token, ai_key


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--drive', '-d', required=True, help='Drive letter or path to USB root (e.g. D: or D:\\)')
    p.add_argument('--password', '-p', required=False, help='Password to decrypt the unlock file (will prompt if omitted)')
    args = p.parse_args()
    password = args.password
    if not password:
        password = getpass.getpass('Enter password to decrypt USB token: ')
    check(args.drive, password)


if __name__ == '__main__':
    main()
