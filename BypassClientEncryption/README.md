# PyCript — Quick Guide (Bypass Client-Side Encryption)

Purpose: Simple, focused instructions to intercept, decrypt, edit, and re-encrypt request bodies using PyCript.

Key protocol notes:
- The request body is passed as a JSON-style byte-array string (e.g. `[123, 34, 117...]`).
- The body is separated from headers by the marker `\n--BODY_END--\n`.

Files you need:
- `decrypt.py` — converts the byte array to plaintext and returns decrypted fields.
- `encrypt.py` — takes modified plaintext and converts it back to the exact byte-array format.
- Note  : The current codes inside the AES folder are served as template to use with PyScript. With the content of code is specifically descrypt password field only. Change is needed for custom Request
Prerequisites:
- Burp Suite with the PyCript extension.
- Python 3 and `pycryptodome` (or equivalent) installed. Point PyCript to the Python binary (for example, `/usr/bin/python3`).

Typical workflow:
1. Intercept the request in Burp Proxy.
2. In the PyCript tab, the `decrypt.py` handler unwraps the byte-array and shows plaintext fields.
3. Edit the plaintext field(s) as needed.
4. Forward the request — PyCript runs `encrypt.py`, which re-wraps the modified plaintext into the original byte-array format and sends the valid ciphertext.
