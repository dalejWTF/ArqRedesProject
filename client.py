import requests
import hashlib
import rsa

# Load public key
with open("public.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

# Prepare request data
data = b'Hello_World!'
checksum = hashlib.sha256(data).hexdigest()
ciphertext = rsa.encrypt(data, public_key)
print("checksum: ",checksum)
print("ciphertext: ",ciphertext)
# The secret password
password = "test"

# The user identifier
user_id = "test"

# Create the plaintext string
plaintext = user_id + password

# Create the hash object
hash_object = hashlib.sha256()

# Update the hash object with the plaintext string
hash_object.update(plaintext.encode())

# Get the hexadecimal representation of the hash
secret_key = hash_object.hexdigest()

# Prepare headers
headers = {
    "Authorization": secret_key,
    "X-Encrypted-Data": ciphertext.hex(),
    "X-Checksum": checksum
}
print(headers)

# Make request
response = requests.get(url="http://192.168.68.107:8000",headers=headers)

print(response.status_code)
print(response.text)
