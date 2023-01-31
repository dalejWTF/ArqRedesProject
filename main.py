from http.server import HTTPServer, BaseHTTPRequestHandler
import hashlib
import rsa

# Generate the RSA keys
(public_key, private_key) = rsa.newkeys(2048)

# Save the private key
with open("private.pem", "wb") as f:
    f.write(private_key.save_pkcs1())

# Save the public key
with open("public.pem", "wb") as f:
    f.write(public_key.save_pkcs1())

# The secret password
password = "test"

# The user identifier
user_id = "test"

# Create the plaintext string
plaintext = user_id + password
#######
#UNO SIN ENCRIPTAR PARA VER EN WIRESHARK Y OTRO ENCRIPTADO
######
# Create the hash object
hash_object = hashlib.sha256()

# Update the hash object with the plaintext string
hash_object.update(plaintext.encode())

# Get the hexadecimal representation of the hash
secret_key = hash_object.hexdigest()
class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Autenticación
        noencrypt=user_id+password
        if self.headers.get("Authorization") != noencrypt:
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Secure Area"')
            data = b'Autenticacion no coincidente! '
            self.wfile.write(data)
            self.end_headers()
            return

        # Desencriptar el cuerpo de la petición utilizando RSA
        private_key = rsa.PrivateKey.load_pkcs1(open("private.pem", "rb").read())
        ciphertext = self.headers.get("X-Encrypted-Data")
        try:
            plaintext = rsa.decrypt(bytes.fromhex(ciphertext), private_key)
            print(plaintext)
            # Verificar la suma de verificación
            checksum = self.headers.get("X-Checksum")
            if hashlib.sha256(plaintext).hexdigest() != checksum:
                #MANDAR MENSAJE DE QUE NO COINCIDE
                self.send_response(400)
                data = b'Checksum no coincidente! '
                self.wfile.write(data)
                self.end_headers()
                return

            # Enviar respuesta
            self.send_response(200)
            #MANDAR MENSAJE DE QUE SI COINCIDE
            self.send_header("Content-type", "text/html")
            self.end_headers()
            data =  b'Peticion recibida exitosamente!'
            self.wfile.write(data)
        except rsa.pkcs1.DecryptionError:
            self.send_response(400)
            data = b'RSA no coincidente! '

            self.wfile.write(data)
            self.end_headers()
            return


if __name__ == "__main__":   
    httpd = HTTPServer(("172.17.163.57", 8000), RequestHandler)
    try:
        print("Running server...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")

