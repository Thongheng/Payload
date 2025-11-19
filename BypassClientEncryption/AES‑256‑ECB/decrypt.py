import json
import argparse
import re
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# CONFIGURATION
AES_KEY_HEX = "3ebcf624336c443e8a3afc8f9d1c8deb"
BODY_MARKER = "\n--BODY_END--\n"

def decrypt_logic(encrypted_b64, key_bytes):
    try:
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        encrypted_bytes = base64.b64decode(encrypted_b64)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), 16)
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", required=True, help="Path to file")
    args = parser.parse_args()
    file_path = args.data

    try:
        # 1. Read the file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 2. Parse PyCript Format (Body [bytes] + Marker + Headers)
        byte_array_str = content
        headers_raw = ""
        
        if BODY_MARKER in content:
            parts = content.split(BODY_MARKER, 1) # Split only on first occurrence
            byte_array_str = parts[0]
            if len(parts) > 1:
                headers_raw = parts[1]

        # 3. Convert "Java Byte Array" string to Python String
        # Input is like "[123, 34, 117...]"
        try:
            byte_list = json.loads(byte_array_str.strip())
            # Convert list of integers back to bytes, then to string
            working_string = bytes(byte_list).decode('utf-8')
        except Exception:
            # Fallback if it's not an array (failsafe)
            working_string = byte_array_str

        # 4. Regex Strategy: Find "password":"<ANYTHING>"
        # We use regex to avoid crashing on the "Invalid JSON" user_key
        password_regex = r'"password"\s*:\s*"([^"]+)"'
        match = re.search(password_regex, working_string)

        if match:
            full_match_str = match.group(0) # "password":"..."
            encrypted_val = match.group(1)  # The content inside quotes
            
            key_bytes = AES_KEY_HEX.encode('utf-8')
            plaintext = decrypt_logic(encrypted_val, key_bytes)
            
            if plaintext:
                # Replace the encrypted part with plaintext
                # We rebuild the string: "password":"PLAINTEXT"
                replacement = f'"password":"{plaintext}"'
                working_string = working_string.replace(full_match_str, replacement)

        # 5. Re-Encode to Byte Array Format [123, 34, ...] for PyCript
        # Convert string back to bytes, then to a list of integers
        new_byte_list = list(working_string.encode('utf-8'))
        output_byte_array_str = json.dumps(new_byte_list)

        # 6. Reconstruct File Content
        final_output = output_byte_array_str
        if BODY_MARKER in content:
            final_output = output_byte_array_str + BODY_MARKER + headers_raw

        # 7. Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_output)

    except Exception as e:
        # Log errors to a tmp file for debugging
        with open("/tmp/pycript_py_decrypt_error.log", "w") as f:
            f.write(str(e))

if __name__ == "__main__":
    main()