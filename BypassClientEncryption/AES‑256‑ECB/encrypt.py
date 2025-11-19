import json
import argparse
import re
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# CONFIGURATION
AES_KEY_HEX = "3ebcf624336c443e8a3afc8f9d1c8deb"
BODY_MARKER = "\n--BODY_END--\n"

def encrypt_logic(plaintext, key_bytes):
    try:
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        padded_data = pad(plaintext.encode('utf-8'), 16)
        encrypted_bytes = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", required=True, help="Path to file")
    args = parser.parse_args()
    file_path = args.data

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        byte_array_str = content
        headers_raw = ""
        
        if BODY_MARKER in content:
            parts = content.split(BODY_MARKER, 1)
            byte_array_str = parts[0]
            if len(parts) > 1:
                headers_raw = parts[1]

        try:
            byte_list = json.loads(byte_array_str.strip())
            working_string = bytes(byte_list).decode('utf-8')
        except Exception:
            working_string = byte_array_str

        # Regex Strategy: Find "password":"<ANYTHING>"
        # Note: In Burp, you will see "password":"myNewPassword". 
        # This script grabs "myNewPassword" and encrypts it.
        password_regex = r'"password"\s*:\s*"([^"]+)"'
        match = re.search(password_regex, working_string)

        if match:
            full_match_str = match.group(0)
            plaintext_val = match.group(1)
            
            key_bytes = AES_KEY_HEX.encode('utf-8')
            ciphertext = encrypt_logic(plaintext_val, key_bytes)
            
            if ciphertext:
                replacement = f'"password":"{ciphertext}"'
                working_string = working_string.replace(full_match_str, replacement)

        # Re-Encode to Byte Array Format
        new_byte_list = list(working_string.encode('utf-8'))
        output_byte_array_str = json.dumps(new_byte_list)

        final_output = output_byte_array_str
        if BODY_MARKER in content:
            final_output = output_byte_array_str + BODY_MARKER + headers_raw

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_output)

    except Exception as e:
        with open("/tmp/pycript_py_encrypt_error.log", "w") as f:
            f.write(str(e))

if __name__ == "__main__":
    main()