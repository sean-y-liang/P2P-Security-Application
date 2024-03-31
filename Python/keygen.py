from cryptography.hazmat.primitives.asymmetric import rsa, dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives import hashes
import os

class keygen:
    def __init__(self):
        self.pub_key = None
        self.priv_key = None

    def generate_and_save_keys(self):
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = private_key.public_key()

            # Save the private key
            with open(os.path.join(os.path.dirname(__file__), 'privateKey.pem'), 'wb') as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            # Save the public key
            with open(os.path.join(os.path.dirname(__file__), 'publicKey.pem'), 'wb') as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

            print('RSA key pair generated and saved successfully.')
        except Exception as error:
            print(f'Failed to generate or save RSA key pair: {error}')

    def load_public_key(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'publicKey.pem'), 'rb') as f:
                return load_pem_public_key(f.read(), backend=default_backend())
        except Exception as error:
            print(f'Failed to load public key: {error}')
            return None

    def load_private_key(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'privateKey.pem'), 'rb') as f:
                return load_pem_private_key(f.read(), None, backend=default_backend())
        except Exception as error:
            print(f'Failed to load private key: {error}')
            return None

    def generate_aes_key(self):
        return os.urandom(32)

    def generate_dh_keys(self):
        try:
            parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
            private_key = parameters.generate_private_key()
            public_key = private_key.public_key()
            return {'public_key': public_key, 'private_key': private_key}
        except Exception as error:
            print(f'Failed to generate DH keys: {error}')
            return None

    def get_public_key_fingerprint(self, public_key):
        try:
            # Assuming public_key is already loaded and is of type RSAPublicKey
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            digest.update(pem)
            return digest.finalize().hex()
        except Exception as error:
            print(f'Failed to generate public key fingerprint: {error}')
            return None

    def regenerate_and_save_keys(self):
        try:
            self.generate_and_save_keys()
            print('Keys have been regenerated and saved.')
        except Exception as error:
            print(f'Failed to regenerate keys: {error}')
