import os
import base64
import json
import hashlib
import tempfile
import time
import random
import zlib
from datetime import datetime
from PIL import Image, ImageDraw, ImageEnhance
from io import BytesIO
import cv2
from pyzbar.pyzbar import decode
import numpy as np

# Untuk RSA
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Untuk ECC
import ecdsa
from ecdsa import SigningKey, VerifyingKey, NIST256p

class HybridSignature:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def generate_rsa_keys(self):
        """Generate RSA key pair"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        
        return private_pem, public_pem
    
    def generate_ecc_keys(self):
        """Generate ECC key pair"""
        sk = SigningKey.generate(curve=NIST256p)
        vk = sk.verifying_key
        
        private_key = sk.to_pem().decode()
        public_key = vk.to_pem().decode()
        
        return private_key, public_key
    
    def generate_aes_key(self):
        """Generate a random AES-256 key"""
        return os.urandom(32)  # 32 bytes = 256 bits
    
    def encrypt_with_aes(self, data, key):
        """Encrypt data with AES-256 in CBC mode"""
        iv = os.urandom(16)  # Initialization vector
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # Ensure data is a multiple of 16 bytes (AES block size)
        padded_data = self._pad_data(data)
        
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv + ciphertext  # Prepend IV to ciphertext
    
    def decrypt_with_aes(self, encrypted_data, key):
        """Decrypt data with AES-256 in CBC mode"""
        iv = encrypted_data[:16]  # First 16 bytes are the IV
        ciphertext = encrypted_data[16:]  # Rest is the ciphertext
        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return self._unpad_data(padded_plaintext)
    
    def _pad_data(self, data):
        """PKCS#7 padding for AES"""
        if not isinstance(data, bytes):
            data = data.encode()
            
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length]) * padding_length
        return data + padding
    
    def _unpad_data(self, padded_data):
        """Remove PKCS#7 padding"""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
    
    def encrypt_aes_key_with_rsa(self, aes_key, rsa_public_key):
        """Encrypt the AES key with RSA public key"""
        public_key = serialization.load_pem_public_key(rsa_public_key.encode())
        encrypted_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_key
    
    def decrypt_aes_key_with_rsa(self, encrypted_key, rsa_private_key):
        """Decrypt the AES key with RSA private key"""
        private_key = serialization.load_pem_private_key(
            rsa_private_key.encode(),
            password=None
        )
        aes_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return aes_key
    
    def sign_with_rsa(self, data, rsa_private_key):
        """Sign data with RSA private key"""
        if not isinstance(data, bytes):
            data = data.encode()
            
        private_key = serialization.load_pem_private_key(
            rsa_private_key.encode(),
            password=None
        )
        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
    
    def verify_with_rsa(self, data, signature, rsa_public_key):
        """Verify signature with RSA public key"""
        if not isinstance(data, bytes):
            data = data.encode()
            
        public_key = serialization.load_pem_public_key(rsa_public_key.encode())
        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    def sign_with_ecc(self, data, ecc_private_key):
        """Sign data with ECC private key"""
        if not isinstance(data, bytes):
            data = data.encode()
            
        sk = SigningKey.from_pem(ecc_private_key)
        signature = sk.sign(data, hashfunc=hashlib.sha256)
        return signature
    
    def verify_with_ecc(self, data, signature, ecc_public_key):
        """Verify signature with ECC public key"""
        if not isinstance(data, bytes):
            data = data.encode()
            
        vk = VerifyingKey.from_pem(ecc_public_key)
        try:
            return vk.verify(signature, data, hashfunc=hashlib.sha256)
        except Exception:
            return False
    
    def calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def compress_data(self, data):
        """Compress data using zlib"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        compressed = zlib.compress(data, level=9)  # Maximum compression
        return compressed
    
    def decompress_data(self, compressed_data):
        """Decompress data using zlib"""
        decompressed = zlib.decompress(compressed_data)
        return decompressed
    
    def sign_document(self, file_path, rsa_private_key, ecc_private_key):
        """
        Sign a document using hybrid RSA-ECC approach:
        1. Calculate document hash
        2. Sign hash with RSA
        3. Encrypt document with AES-256
        4. Sign encrypted document with ECC
        5. Generate metadata with signatures, public keys, and metadata
        """
        # Read file
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        # Calculate document hash
        doc_hash = hashlib.sha256(file_data).hexdigest()
        
        # Sign hash with RSA
        rsa_signature = self.sign_with_rsa(doc_hash, rsa_private_key)
        
        # Generate AES key and encrypt document
        aes_key = self.generate_aes_key()
        encrypted_data = self.encrypt_with_aes(file_data, aes_key)
        
        # Get RSA public key from private key
        private_key_obj = serialization.load_pem_private_key(
            rsa_private_key.encode(),
            password=None
        )
        rsa_public_key = private_key_obj.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        
        # Get ECC public key from private key
        sk = SigningKey.from_pem(ecc_private_key)
        ecc_public_key = sk.verifying_key.to_pem().decode()
        
        # Encrypt AES key with RSA
        encrypted_aes_key = self.encrypt_aes_key_with_rsa(aes_key, rsa_public_key)
        
        # Sign encrypted data with ECC
        ecc_signature = self.sign_with_ecc(encrypted_data, ecc_private_key)
        
        # Create metadata
        metadata = {
            "filename": os.path.basename(file_path),
            "timestamp": datetime.now().isoformat(),
            "doc_hash": doc_hash,
            "rsa_signature": base64.b64encode(rsa_signature).decode(),
            "ecc_signature": base64.b64encode(ecc_signature).decode(),
            "encrypted_aes_key": base64.b64encode(encrypted_aes_key).decode(),
            "rsa_public_key": rsa_public_key,
            "ecc_public_key": ecc_public_key
        }
        
        # Create a separate metadata file for the keys
        keys_metadata = {
            "rsa_public_key": rsa_public_key,
            "ecc_public_key": ecc_public_key,
            "filename": os.path.basename(file_path),
            "timestamp": datetime.now().isoformat(),
            "doc_hash": doc_hash,
            "rsa_signature": base64.b64encode(rsa_signature).decode(),
            "ecc_signature": base64.b64encode(ecc_signature).decode(),
            "encrypted_aes_key": base64.b64encode(encrypted_aes_key).decode()
        }
        
        keys_metadata_path = os.path.join(self.temp_dir, f"keys_{int(time.time())}.json")
        with open(keys_metadata_path, 'w') as f:
            json.dump(keys_metadata, f)
        
        # Save encrypted document
        encrypted_path = os.path.join(self.temp_dir, f"encrypted_{os.path.basename(file_path)}")
        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)
        
        return {
            "encrypted_path": encrypted_path,
            "keys_metadata_path": keys_metadata_path,
            "metadata": metadata,
            "aes_key": aes_key  # Include AES key for decryption
        }
    
    def verify_document_with_metadata(self, encrypted_file_path, keys_metadata):
        """
        Verify a document using hybrid RSA-ECC approach with metadata:
        1. Get public keys from metadata
        2. Verify ECC signature on encrypted document
        3. Verify RSA signature on document hash
        """
        # Read encrypted file
        with open(encrypted_file_path, "rb") as f:
            encrypted_data = f.read()
        
        # Get public keys and signatures from metadata
        rsa_public_key = keys_metadata.get("rsa_public_key")
        ecc_public_key = keys_metadata.get("ecc_public_key")
        
        if not rsa_public_key or not ecc_public_key:
            return {"valid": False, "error": "Public keys not found in metadata"}
        
        # Verify ECC signature
        ecc_signature = base64.b64decode(keys_metadata["ecc_signature"])
        ecc_valid = self.verify_with_ecc(encrypted_data, ecc_signature, ecc_public_key)
        
        if not ecc_valid:
            return {
                "valid": False, 
                "error": "ECC signature verification failed. Document may have been tampered with."
            }
        
        # Verify RSA signature
        rsa_signature = base64.b64decode(keys_metadata["rsa_signature"])
        rsa_valid = self.verify_with_rsa(keys_metadata["doc_hash"], rsa_signature, rsa_public_key)
        
        if not rsa_valid:
            return {
                "valid": False, 
                "error": "RSA signature verification failed. Document hash doesn't match."
            }
        
        # If verification succeeds
        return {
            "valid": True,
            "metadata": keys_metadata,
            "message": "Document signature is valid. This is an authentic document.",
            "encrypted_data": encrypted_data
        }
    
    def verify_document(self, encrypted_file_path, qr_code_path, keys_metadata_path=None):
        """
        Verify a document using hybrid RSA-ECC approach:
        1. Read QR code to get metadata
        2. Get public keys from keys metadata file or QR code
        3. Verify ECC signature on encrypted document
        4. Verify RSA signature on document hash
        5. Decrypt document if verification succeeds
        """
        # Read QR code
        qr_data = self.read_qr_code(qr_code_path)
        if not qr_data:
            return {"valid": False, "error": "Could not read QR code"}
        
        try:
            # Try to decompress the data
            try:
                decompressed_data = self.decompress_data(base64.b64decode(qr_data))
                metadata = json.loads(decompressed_data)
            except:
                # If decompression fails, try to parse as JSON directly
                metadata = json.loads(qr_data)
        except json.JSONDecodeError:
            return {"valid": False, "error": "Invalid QR code data format"}
        
        # Get public keys
        if keys_metadata_path and os.path.exists(keys_metadata_path):
            # Read keys from metadata file
            with open(keys_metadata_path, 'r') as f:
                keys_metadata = json.load(f)
            rsa_public_key = keys_metadata.get("rsa_public_key")
            ecc_public_key = keys_metadata.get("ecc_public_key")
        else:
            # If no keys metadata file, check if keys are in the QR code
            rsa_public_key = metadata.get("rsa_public_key")
            ecc_public_key = metadata.get("ecc_public_key")
            
            if not rsa_public_key or not ecc_public_key:
                return {"valid": False, "error": "Public keys not found in QR code or keys metadata file"}

        # Read encrypted file
        with open(encrypted_file_path, "rb") as f:
            encrypted_data = f.read()
        
        # Verify ECC signature
        ecc_signature = base64.b64decode(metadata["ecc_signature"])
        ecc_valid = self.verify_with_ecc(encrypted_data, ecc_signature, ecc_public_key)
        
        if not ecc_valid:
            return {
                "valid": False, 
                "error": "ECC signature verification failed. Document may have been tampered with."
            }
        
        # Verify RSA signature
        rsa_signature = base64.b64decode(metadata["rsa_signature"])
        rsa_valid = self.verify_with_rsa(metadata["doc_hash"], rsa_signature, rsa_public_key)
        
        if not rsa_valid:
            return {
                "valid": False, 
                "error": "RSA signature verification failed. Document hash doesn't match."
            }
        
        # If verification succeeds
        return {
            "valid": True,
            "metadata": metadata,
            "message": "Document signature is valid. This is an authentic document.",
            "encrypted_data": encrypted_data
        }
    
    def read_qr_code(self, image_path):
        """Read QR code from image file"""
        if isinstance(image_path, str):
            # Read from file path
            image = cv2.imread(image_path)
        else:
            # Convert PIL Image to OpenCV format
            image = cv2.cvtColor(np.array(image_path), cv2.COLOR_RGB2BGR)
            
        decoded_objects = decode(image)
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        return None

    # Tambahkan metode baru untuk dekripsi dokumen
    def decrypt_document(self, encrypted_file_path, keys_metadata, rsa_private_key):
        """
        Decrypt a document using the hybrid RSA-ECC approach:
        1. Verify document signatures first
        2. Decrypt AES key using RSA private key
        3. Decrypt document using AES key
        """
        try:
            # First verify the document
            verify_result = self.verify_document_with_metadata(encrypted_file_path, keys_metadata)
            
            if not verify_result['valid']:
                return {
                    'success': False,
                    'error': 'Document verification failed. Cannot decrypt an invalid document.'
                }
            
            # Read encrypted file
            with open(encrypted_file_path, "rb") as f:
                encrypted_data = f.read()
            
            # Get encrypted AES key from metadata
            encrypted_aes_key = base64.b64decode(keys_metadata["encrypted_aes_key"])
            
            # Decrypt AES key with RSA private key
            try:
                aes_key = self.decrypt_aes_key_with_rsa(encrypted_aes_key, rsa_private_key)
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to decrypt AES key. Make sure you provided the correct RSA private key: {str(e)}'
                }
            
            # Decrypt document with AES key
            try:
                decrypted_data = self.decrypt_with_aes(encrypted_data, aes_key)
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to decrypt document: {str(e)}'
                }
            
            return {
                'success': True,
                'decrypted_data': decrypted_data,
                'filename': keys_metadata.get('filename', 'decrypted_file')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Decryption failed: {str(e)}'
            }
