from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, url_for, redirect, make_response
import os
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
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploaded_files')

try:
    os.makedirs(SIGNED_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    logger.debug(f"Directories created: {SIGNED_FOLDER}, {UPLOAD_FOLDER}")
except Exception as e:
    logger.error(f"Error creating directories: {str(e)}")
    raise

app.config['SIGNED_FOLDER'] = SIGNED_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt', 'py', 'html', 'php', 'json', 'js', 'css', 'xml', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'ts', 'jsx', 'tsx', 'md', 'yml', 'yaml', 'sql', 'sh', 'bat'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

@app.route('/')
def index():
    logger.debug("Rendering index.html template")
    return render_template('index.html')

@app.route('/hybrid-encription', methods=['GET', 'POST'])
def hybrid_signature():
    logger.debug("Rendering hybrid-encription.html template")
    if request.method == 'POST':
        # Handle form data for file encryption
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
                        
                        # Encrypt the file with hybrid approach
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
                            'message': 'File encrypted successfully with hybrid RSA-ECC approach',
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
    
    return render_template('hybrid-encription.html')

# Tambahkan route baru untuk dekripsi dokumen
@app.route('/hybrid-encription/decrypt', methods=['POST'])
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

@app.route('/hybrid-encription/generate-ecc', methods=['POST'])
def generate_ecc_keys():
    hybrid_signer = HybridSignature()
    private_key, public_key = hybrid_signer.generate_ecc_keys()
    return jsonify({'privateKey': private_key, 'publicKey': public_key})

@app.route('/asymmetric', methods=['POST'])
def asymmetric():
    if request.is_json:
        data = request.get_json()
        action = data.get('action')
        
        if action == 'generate':
            # Create hybrid signature instance
            hybrid_signer = HybridSignature()
            
            # Generate RSA keys
            private_key, public_key = hybrid_signer.generate_rsa_keys()
            
            return jsonify({
                'privateKey': private_key,
                'publicKey': public_key
            })
    
    return jsonify({'error': 'Invalid request'})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['SIGNED_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)