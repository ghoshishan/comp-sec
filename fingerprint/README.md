# Secure fingerprint system prototype

- Server side and client side operations are seperated into modules namely server and client
- Enrollment process is done by `client.py enroll()`. It takes inputs from `enroll-input-list.json`
- Verification process is done by `client.py verify()`. It takes inputs from `verify-input-list.json`
- Both enrollment process and verification process makes use of server and client modules.

## Changes to design

While sending transformed vector to server for verification, we encrypt it using servers key.
This step is avoided in prototype as there is no transfer over network.

Shuffling is not done for simplicity

There is no seperate storage for verification code, it will be encryted with users public key before storing alongside other
user credentials encrypted with users pin. Due to this, there is no need of vid.
