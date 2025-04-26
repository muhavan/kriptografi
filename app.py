from flask import Flask, render_template, request, jsonify, send_file, url_for, redirect, make_response
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import base64
import hashlib
import tempfile
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from hybrid_signature import HybridSignature

# Tambahkan logging untuk membantu debugging
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Add this near the top of the file, after app initialization
print(f"Templates directory: {app.template_folder}")
print(f"Available templates: {os.listdir(app.template_folder)}")

# Buat direktori untuk menyimpan file sementara
SIGNED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'signed_files')
os.makedirs(SIGNED_FOLDER, exist_ok=True)

app.config['SIGNED_FOLDER'] = SIGNED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Untuk enkripsi simetris (Fernet)
def generate_symmetric_key():
    return Fernet.generate_key()

def symmetric_encrypt(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def symmetric_decrypt(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message.encode()).decode()

# Untuk enkripsi asimetris (RSA)
def generate_rsa_keys():
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

def rsa_encrypt(message, public_key_pem):
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode()

def rsa_decrypt(encrypted_message, private_key_pem):
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None
    )
    decrypted = private_key.decrypt(
        base64.b64decode(encrypted_message),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

# Untuk tanda tangan digital
def sign_message(message, private_key_pem):
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None
    )
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()

def verify_signature(message, signature, public_key_pem):
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    try:
        public_key.verify(
            base64.b64decode(signature),
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

# Untuk tanda tangan file
def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def sign_file(file_path, private_key_pem):
    """Sign a file using private key"""
    file_hash = calculate_file_hash(file_path)
    return sign_message(file_hash, private_key_pem)

def verify_file_signature(file_path, signature, public_key_pem):
    """Verify a file's signature using public key"""
    file_hash = calculate_file_hash(file_path)
    return verify_signature(file_hash, signature, public_key_pem)

def create_signed_package(file_path, signature, public_key_pem, output_dir):
    """Create a package containing the file, signature, and metadata"""
    # Get original filename and extension
    original_filename = os.path.basename(file_path)
    filename_without_ext, file_extension = os.path.splitext(original_filename)
    
    # Create metadata
    metadata = {
        "original_filename": original_filename,
        "signature": signature,
        "public_key": public_key_pem,
        "timestamp": datetime.now().isoformat(),
        "hash_algorithm": "SHA-256"
    }
    
    # Create a unique filename for the signed package
    signed_filename = f"{filename_without_ext}_signed_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
    signed_path = os.path.join(output_dir, signed_filename)
    
    # Create a temporary directory to store files for zipping
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy the original file
        import shutil
        temp_file_path = os.path.join(temp_dir, original_filename)
        shutil.copy2(file_path, temp_file_path)
        
        # Write metadata to JSON file
        metadata_path = os.path.join(temp_dir, "signature.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        # Create zip file
        import zipfile
        with zipfile.ZipFile(signed_path, 'w') as zipf:
            zipf.write(temp_file_path, arcname=original_filename)
            zipf.write(metadata_path, arcname="signature.json")
    
    return signed_path

def extract_and_verify_signed_package(signed_package_path, temp_dir):
    """Extract and verify a signed package"""
    # Extract the zip file
    import zipfile
    with zipfile.ZipFile(signed_package_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Read metadata
    metadata_path = os.path.join(temp_dir, "signature.json")
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Get original file path
    original_filename = metadata["original_filename"]
    original_file_path = os.path.join(temp_dir, original_filename)
    
    # Verify signature
    signature = metadata["signature"]
    public_key = metadata["public_key"]
    is_valid = verify_file_signature(original_file_path, signature, public_key)
    
    return is_valid, metadata, original_file_path

# Untuk hashing
def hash_message(message, algorithm):
    if algorithm == 'md5':
        return hashlib.md5(message.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(message.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(message.encode()).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(message.encode()).hexdigest()
    return None

# Sandi Caesar
def caesar_encrypt(message, shift):
    result = ""
    for char in message:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def caesar_decrypt(encrypted_message, shift):
    return caesar_encrypt(encrypted_message, -shift)

@app.route('/')
def index():
    logger.debug("Rendering index.html template")
    return render_template('index.html')

@app.route('/symmetric', methods=['GET', 'POST'])
def symmetric():
    logger.debug("Rendering symmetric.html template")
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        message = data.get('message', '')
        key = data.get('key', '')
        
        if action == 'generate':
            new_key = generate_symmetric_key().decode()
            return jsonify({'key': new_key})
        elif action == 'encrypt':
            try:
                encrypted = symmetric_encrypt(message, key)
                return jsonify({'result': encrypted})
            except Exception as e:
                logger.error(f"Error in symmetric encryption: {str(e)}")
                return jsonify({'error': str(e)})
        elif action == 'decrypt':
            try:
                decrypted = symmetric_decrypt(message, key)
                return jsonify({'result': decrypted})
            except Exception as e:
                logger.error(f"Error in symmetric decryption: {str(e)}")
                return jsonify({'error': str(e)})
    
    return render_template('symmetric.html')

@app.route('/asymmetric', methods=['GET', 'POST'])
def asymmetric():
    logger.debug("Rendering asymmetric.html template")
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        message = data.get('message', '')
        public_key = data.get('publicKey', '')
        private_key = data.get('privateKey', '')
        
        if action == 'generate':
            private_pem, public_pem = generate_rsa_keys()
            return jsonify({'privateKey': private_pem, 'publicKey': public_pem})
        elif action == 'encrypt':
            try:
                encrypted = rsa_encrypt(message, public_key)
                return jsonify({'result': encrypted})
            except Exception as e:
                logger.error(f"Error in asymmetric encryption: {str(e)}")
                return jsonify({'error': str(e)})
        elif action == 'decrypt':
            try:
                decrypted = rsa_decrypt(message, private_key)
                return jsonify({'result': decrypted})
            except Exception as e:
                logger.error(f"Error in asymmetric decryption: {str(e)}")
                return jsonify({'error': str(e)})
    
    return render_template('asymmetric.html')

@app.route('/hybrid-signature', methods=['GET', 'POST'])
def hybrid_signature():
    logger.debug("Rendering hybrid-signature.html template")
    if request.method == 'POST':
        # Handle form data for file signing
        if not request.is_json:
            action = request.form.get('action')
            
            if action == 'hybrid_sign_file':
                # Check if the post request has the file part
                if 'file' not in request.files:
                    return jsonify({'error': 'No file part'})
                
                file = request.files['file']
                rsa_private_key = request.form.get('rsaPrivateKey', '')
                ecc_private_key = request.form.get('eccPrivateKey', '')
                
                # If user does not select file, browser also submits an empty part without filename
                if file.filename == '':
                    return jsonify({'error': 'No selected file'})
                
                if not rsa_private_key or not ecc_private_key:
                    return jsonify({'error': 'Both RSA and ECC private keys are required'})
                
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    try:
                        # Create hybrid signature instance
                        hybrid_signer = HybridSignature()
                        
                        # Sign the file with hybrid approach
                        result = hybrid_signer.sign_document(file_path, rsa_private_key, ecc_private_key)
                        
                        # Copy encrypted file to signed folder
                        encrypted_filename = os.path.basename(result['encrypted_path'])
                        encrypted_dest_path = os.path.join(app.config['SIGNED_FOLDER'], encrypted_filename)
                        import shutil
                        shutil.copy2(result['encrypted_path'], encrypted_dest_path)
                        
                        # Copy keys metadata file to signed folder
                        keys_metadata_filename = os.path.basename(result['keys_metadata_path'])
                        keys_metadata_dest_path = os.path.join(app.config['SIGNED_FOLDER'], keys_metadata_filename)
                        shutil.copy2(result['keys_metadata_path'], keys_metadata_dest_path)
                        
                        return jsonify({
                            'success': True,
                            'message': 'File signed successfully with hybrid RSA-ECC approach',
                            'encrypted_filename': encrypted_filename,
                            'keys_metadata_filename': keys_metadata_filename,
                            'metadata': result['metadata']
                        })
                    except Exception as e:
                        return jsonify({'error': str(e)})
                    finally:
                        # Clean up the uploaded file
                        if os.path.exists(file_path):
                            os.remove(file_path)
                
                return jsonify({'error': 'Invalid file type'})
            
            elif action == 'hybrid_verify_file_simple':
                # Check if the post request has the file and metadata parts
                if 'file' not in request.files or 'keys_metadata' not in request.files:
                    return jsonify({'error': 'Both encrypted file and metadata file are required'})
                
                file = request.files['file']
                keys_metadata_file = request.files['keys_metadata']
                
                if file.filename == '' or keys_metadata_file.filename == '':
                    return jsonify({'error': 'Both encrypted file and metadata file must be selected'})
                
                # Save uploaded files
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                keys_metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(keys_metadata_file.filename))
                file.save(file_path)
                keys_metadata_file.save(keys_metadata_path)
                
                try:
                    # Create hybrid signature instance
                    hybrid_signer = HybridSignature()
                    
                    # Read metadata from file
                    with open(keys_metadata_path, 'r') as f:
                        keys_metadata = json.load(f)
                    
                    # Verify the file with hybrid approach (simplified version)
                    result = hybrid_signer.verify_document_with_metadata(file_path, keys_metadata)
                    
                    if result['valid']:
                        return jsonify({
                            'success': True,
                            'isValid': True,
                            'message': 'File signature is valid. Document is authentic and unaltered.',
                            'metadata': result['metadata']
                        })
                    else:
                        return jsonify({
                            'success': True,
                            'isValid': False,
                            'message': result['error']
                        })
                except Exception as e:
                    return jsonify({'error': str(e)})
                finally:
                    # Clean up the uploaded files
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    if os.path.exists(keys_metadata_path):
                        os.remove(keys_metadata_path)
    
    return render_template('hybrid-signature.html')

# Tambahkan route baru untuk dekripsi dokumen
@app.route('/hybrid-signature/decrypt', methods=['POST'])
def decrypt_hybrid_document():
    if 'file' not in request.files or 'keys_metadata' not in request.files:
        return jsonify({'error': 'Both encrypted file and metadata file are required'})
    
    file = request.files['file']
    keys_metadata_file = request.files['keys_metadata']
    rsa_private_key = request.form.get('rsaPrivateKey', '')
    
    if file.filename == '' or keys_metadata_file.filename == '':
        return jsonify({'error': 'Both encrypted file and metadata file must be selected'})
    
    if not rsa_private_key:
        return jsonify({'error': 'RSA private key is required'})
    
    # Save uploaded files
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    keys_metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(keys_metadata_file.filename))
    file.save(file_path)
    keys_metadata_file.save(keys_metadata_path)
    
    try:
        # Create hybrid signature instance
        hybrid_signer = HybridSignature()
        
        # Read metadata from file
        with open(keys_metadata_path, 'r') as f:
            keys_metadata = json.load(f)
        
        # Decrypt the file
        result = hybrid_signer.decrypt_document(file_path, keys_metadata, rsa_private_key)
        
        if not result.get('success'):
            return jsonify({'error': result.get('error', 'Failed to decrypt document')})
        
        # Get decrypted data and original filename
        decrypted_data = result['decrypted_data']
        original_filename = keys_metadata.get('filename', 'decrypted_file')
        
        # Determine file type
        file_type = 'application/octet-stream'  # Default binary type
        if original_filename.lower().endswith(('.jpg', '.jpeg')):
            file_type = 'image/jpeg'
        elif original_filename.lower().endswith('.png'):
            file_type = 'image/png'
        elif original_filename.lower().endswith('.gif'):
            file_type = 'image/gif'
        elif original_filename.lower().endswith('.pdf'):
            file_type = 'application/pdf'
        elif original_filename.lower().endswith('.txt'):
            file_type = 'text/plain; charset=utf-8'  # Perbaikan: Menambahkan charset=utf-8
        elif original_filename.lower().endswith(('.doc', '.docx')):
            file_type = 'application/msword'
        
        # Create response with decrypted data
        response = make_response(decrypted_data)
        response.headers['Content-Type'] = file_type
        # Perbaikan: Menggunakan inline untuk preview dan memastikan nama file dipertahankan
        response.headers['Content-Disposition'] = f'inline; filename="{original_filename}"'
        response.headers['X-Filename'] = original_filename
        response.headers['X-File-Type'] = file_type
        
        return response
        
    except Exception as e:
        logger.error(f"Error in decrypt_hybrid_document: {str(e)}")
        return jsonify({'error': str(e)})
    finally:
        # Clean up the uploaded files
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(keys_metadata_path):
            os.remove(keys_metadata_path)

@app.route('/hybrid-signature/generate-ecc', methods=['POST'])
def generate_ecc_keys():
    hybrid_signer = HybridSignature()
    private_key, public_key = hybrid_signer.generate_ecc_keys()
    return jsonify({'privateKey': private_key, 'publicKey': public_key})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['SIGNED_FOLDER'], filename), as_attachment=True)

@app.route('/hashing', methods=['GET', 'POST'])
def hashing():
    logger.debug("Rendering hashing.html template")
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message', '')
        algorithm = data.get('algorithm', 'sha256')
        
        hashed = hash_message(message, algorithm)
        return jsonify({'result': hashed})
    
    return render_template('hashing.html')

@app.route('/caesar', methods=['GET', 'POST'])
def caesar():
    logger.debug("Rendering caesar.html template")
    if request.method == 'POST':
        data = request.get_json()
        action = data.get('action')
        message = data.get('message', '')
        shift = int(data.get('shift', 3))
        
        if action == 'encrypt':
            result = caesar_encrypt(message, shift)
            return jsonify({'result': result})
        elif action == 'decrypt':
            result = caesar_decrypt(message, shift)
            return jsonify({'result': result})
    
    return render_template('caesar.html')

if __name__ == '__main__':
    app.run(debug=True)
