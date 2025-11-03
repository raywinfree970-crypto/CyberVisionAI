#!/usr/bin/env python3
"""Provision a USB drive with an encrypted unlock token.

Writes a single file named `cybervision_unlock.bin` to the root of the specified drive.
The file is a JSON blob (utf-8) containing base64-encoded salt, nonce and ciphertext.

Usage:
  python scripts/provision_usb.py --drive D: --password "hunter2"

WARNING: This is a convenience developer tool for local use. Keep your password safe.
"""
import argparse
import os
import json
import base64
import secrets
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


def provision(drive: str, password: str, ai_key: str | None = None):
    # Normalize drive path
    if len(drive) == 2 and drive[1] == ':':
        root = drive + '\\'
    else:
        root = drive

    if not os.path.isdir(root):
        raise SystemExit(f"Drive root not found: {root}")

    outfile = os.path.join(root, 'cybervision_unlock.bin')

    token = secrets.token_urlsafe(32)
    salt = secrets.token_bytes(16)
    key = derive_key(password.encode('utf-8'), salt)
    aes = AESGCM(key)
    nonce = secrets.token_bytes(12)
    # Build a JSON payload that contains both the token and an optional AI key.
    data = {
        'token': token,
        'ai_key': ai_key or ''
    }
    plaintext = json.dumps(data).encode('utf-8')
    ciphertext = aes.encrypt(nonce, plaintext, None)

    payload = {
        'version': 1,
        'salt': base64.b64encode(salt).decode('ascii'),
        'nonce': base64.b64encode(nonce).decode('ascii'),
        'ciphertext': base64.b64encode(ciphertext).decode('ascii'),
    }

    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(payload, f)

    print(f'Wrote unlock file to: {outfile}')
    print('IMPORTANT: Keep the USB drive safe. If you lose the drive you will need the password to recreate it.')
    print('Token (store securely):', token)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--drive', '-d', required=True, help='Drive letter or path to USB root (e.g. D: or D:\\)')
    p.add_argument('--password', '-p', required=False, help='Password to encrypt the token (will prompt if omitted)')
    p.add_argument('--ai-key', '-k', required=False, help='Optional AI API key to store on the USB (will prompt if omitted)')
    args = p.parse_args()

    password = args.password
    if not password:
        password = getpass.getpass('Enter password to encrypt USB token: ')

    ai_key = args.ai_key
    if ai_key is None:
        # Ask interactively but allow empty
        ai_key = getpass.getpass('Enter AI key to store on USB (leave blank to skip): ')

    provision(args.drive, password, ai_key)


if __name__ == '__main__':
    main()
