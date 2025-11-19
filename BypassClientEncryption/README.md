# 🔑 PyCript Guide: Bypassing Client-Side Encryption (CSE)

This documentation provides the necessary configuration and specialized code modules to intercept, decrypt, modify, and re-encrypt traffic protected by symmetric cryptography used for client-side protection.

***

## 1. Overview and The Data Barrier

The fundamental challenge in bypassing Client-Side Encryption using PyCript is the **Data Format Barrier**. PyCript, being a Java extension, uses a strict file protocol for all data transfer:

1.  **Input Protocol:** The entire request body is passed as a JSON representation of a byte array (a string like `[123, 34, 117...]`).
2.  **File Structure:** The data is separated from the raw headers by a marker: `\n--BODY_END--\n`.

**The Solution:** Our custom **Processing Modules** handle this protocol by performing a **Surgical Modification**. This involves: **Unwrapping** (converting the byte array list to readable text), finding and decrypting the target field using **Regex** (to bypass malformed JSON), and then **Wrapping** (converting the modified text back into the exact byte array format) before writing back to the file.

---

## 2. Prerequisites and Custom Handlers

* **Required Tool:** Burp Suite (with PyCript extension).
* **Required Interpreter:** Python 3 (with the necessary cryptographic library, e.g., `pycryptodome`).

**Custom Code Modules:**
You must have two specialized files—a decryption handler and an encryption handler—configured with the target application's cryptographic key. These **Processing Modules** must handle the complex file I/O protocol detailed above.

---

## 3. PyCript Configuration and Workflow (Critical)

Configure the PyCript extension based on this specialized file protocol method:

### A. Core Settings

| Setting | Value | Notes |
| :--- | :--- | :--- |
| **Request Type** | **Complete Body** | **Crucial:** Must process the whole JSON body to handle the context and file structure. |
| **Language Binary** | `/usr/bin/python3` | Must point to the Python environment with your cryptographic libraries installed. |

### B. File Selection

| Setting | Value | Notes |
| :--- | :--- | :--- |
| **Encryption File** | `/path/to/your/encrypt.py` | Full path to the encryption module. |
| **Decryption File** | `/path/to/your/decrypt.py` | Full path to the decryption module. |

### C. Execution Workflow

1.  **Intercept:** Capture the target request (e.g., Login) in Burp Proxy.
2.  **View Decrypted:** Go to the **PyCript** tab. The custom handler automatically **decrypts** the body and renders the plaintext password field.
3.  **Bypass/Edit:** Modify the plaintext password in the PyCript tab (e.g., change `"password": "userpass"` to `"password": "admin"`).
4.  **Forward:** When you click "Forward" (or "Send" in Repeater), PyCript executes your **encryption module**, which re-encrypts your modified plaintext and sends the valid ciphertext to the server.# Payload
