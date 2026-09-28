import os
import json
import shutil
import logging
from datetime import datetime
from flask import (
    Flask, render_template, request, jsonify,
    send_file, send_from_directory, make_response
)
from werkzeug.utils import secure_filename

from config import config
from hybrid_signature import HybridSignature

def create_app(config_name=None):
    """Application Factory Pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    selected_config = config.get(config_name, config['default'])
    
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )
    app.config.from_object(selected_config)

    # Konfigurasi Logging
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    app.logger.setLevel(log_level)

    # Buat direktori penyimpanan jika belum ada
    os.makedirs(app.config['SIGNED_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    # Route kompatibilitas untuk folder gambar (mendukung path /images/<filename> lama)
    @app.route('/images/<path:filename>')
    def legacy_images(filename):
        # Cari di static/images terlebih dahulu, lalu fallback ke images/ jika ada
        static_img_dir = os.path.join(app.static_folder, 'images')
        if os.path.exists(os.path.join(static_img_dir, filename)):
            return send_from_directory(static_img_dir, filename)
        return send_from_directory('images', filename)

    @app.route('/')
    def index():
        app.logger.debug("Rendering index.html template")
        return render_template('index.html')

    @app.route('/hybrid-encription', methods=['GET', 'POST'])
    def hybrid_signature():
        app.logger.debug("Rendering hybrid-encription.html template")
        if request.method == 'POST':
            if not request.is_json:
                action = request.form.get('action')
                
                # --- ENKRIPSI FILE HYBRID ---
                if action == 'hybrid_sign_file':
                    if 'file' not in request.files:
                        return jsonify({'error': 'No file part'})
                    
                    file = request.files['file']
                    rsa_private_key = request.form.get('rsaPrivateKey', '').strip()
                    ecc_private_key = request.form.get('eccPrivateKey', '').strip()
                    
                    if file.filename == '':
                        return jsonify({'error': 'No selected file'})
                    
                    if not rsa_private_key or not ecc_private_key:
                        return jsonify({'error': 'Both RSA and ECC private keys are required'})
                    
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        
                        try:
                            hybrid_signer = HybridSignature()
                            result = hybrid_signer.sign_document(file_path, rsa_private_key, ecc_private_key)
                            
                            # Salin file terenkripsi ke signed_folder
                            encrypted_filename = os.path.basename(result['encrypted_path'])
                            encrypted_dest_path = os.path.join(app.config['SIGNED_FOLDER'], encrypted_filename)
                            shutil.copy2(result['encrypted_path'], encrypted_dest_path)
                            
                            # Salin file metadata ke signed_folder
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
                            app.logger.error(f"Error signing file: {str(e)}")
                            return jsonify({'error': str(e)})
                        finally:
                            if os.path.exists(file_path):
                                os.remove(file_path)
                    
                    return jsonify({'error': 'Invalid file type'})
                
                # --- VERIFIKASI FILE HYBRID ---
                elif action == 'hybrid_verify_file_simple':
                    if 'file' not in request.files or 'keys_metadata' not in request.files:
                        return jsonify({'error': 'Both encrypted file and metadata file are required'})
                    
                    file = request.files['file']
                    keys_metadata_file = request.files['keys_metadata']
                    
                    if file.filename == '' or keys_metadata_file.filename == '':
                        return jsonify({'error': 'Both encrypted file and metadata file must be selected'})
                    
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                    keys_metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(keys_metadata_file.filename))
                    file.save(file_path)
                    keys_metadata_file.save(keys_metadata_path)
                    
                    try:
                        hybrid_signer = HybridSignature()
                        with open(keys_metadata_path, 'r', encoding='utf-8') as f:
                            keys_metadata = json.load(f)
                        
                        result = hybrid_signer.verify_document_with_metadata(file_path, keys_metadata)
                        
                        if result.get('valid'):
                            return jsonify({
                                'success': True,
                                'isValid': True,
                                'message': 'File signature is valid. Document is authentic and unaltered.',
                                'metadata': result.get('metadata')
                            })
                        else:
                            return jsonify({
                                'success': True,
                                'isValid': False,
                                'message': result.get('error', 'Verification failed')
                            })
                    except Exception as e:
                        app.logger.error(f"Error verifying file: {str(e)}")
                        return jsonify({'error': str(e)})
                    finally:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        if os.path.exists(keys_metadata_path):
                            os.remove(keys_metadata_path)
        
        return render_template('hybrid-encription.html')

    # --- DEKRIPSI FILE HYBRID ---
    @app.route('/hybrid-encription/decrypt', methods=['POST'])
    def decrypt_hybrid_document():
        if 'file' not in request.files or 'keys_metadata' not in request.files:
            return jsonify({'error': 'Both encrypted file and metadata file are required'})
        
        file = request.files['file']
        keys_metadata_file = request.files['keys_metadata']
        rsa_private_key = request.form.get('rsaPrivateKey', '').strip()
        
        if file.filename == '' or keys_metadata_file.filename == '':
            return jsonify({'error': 'Both encrypted file and metadata file must be selected'})
        
        if not rsa_private_key:
            return jsonify({'error': 'RSA private key is required'})
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        keys_metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(keys_metadata_file.filename))
        file.save(file_path)
        keys_metadata_file.save(keys_metadata_path)
        
        try:
            hybrid_signer = HybridSignature()
            with open(keys_metadata_path, 'r', encoding='utf-8') as f:
                keys_metadata = json.load(f)
            
            result = hybrid_signer.decrypt_document(file_path, keys_metadata, rsa_private_key)
            
            if not result.get('success'):
                return jsonify({'error': result.get('error', 'Failed to decrypt document')})
            
            decrypted_data = result['decrypted_data']
            original_filename = keys_metadata.get('filename', 'decrypted_file')
            
            # Deteksi tipe file
            file_type = 'application/octet-stream'
            ext = original_filename.lower()
            if ext.endswith(('.jpg', '.jpeg')):
                file_type = 'image/jpeg'
            elif ext.endswith('.png'):
                file_type = 'image/png'
            elif ext.endswith('.gif'):
                file_type = 'image/gif'
            elif ext.endswith('.pdf'):
                file_type = 'application/pdf'
            elif ext.endswith('.txt'):
                file_type = 'text/plain; charset=utf-8'
            elif ext.endswith(('.doc', '.docx')):
                file_type = 'application/msword'
            elif ext.endswith('.json'):
                file_type = 'application/json'
            
            response = make_response(decrypted_data)
            response.headers['Content-Type'] = file_type
            response.headers['Content-Disposition'] = f'inline; filename="{original_filename}"'
            response.headers['X-Filename'] = original_filename
            response.headers['X-File-Type'] = file_type
            
            return response
            
        except Exception as e:
            app.logger.error(f"Error in decrypt_hybrid_document: {str(e)}")
            return jsonify({'error': str(e)})
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(keys_metadata_path):
                os.remove(keys_metadata_path)

    # --- GENERATE ECC KEYS ---
    @app.route('/hybrid-encription/generate-ecc', methods=['POST'])
    def generate_ecc_keys():
        hybrid_signer = HybridSignature()
        private_key, public_key = hybrid_signer.generate_ecc_keys()
        return jsonify({'privateKey': private_key, 'publicKey': public_key})

    # --- GENERATE RSA KEYS ---
    @app.route('/asymmetric', methods=['POST'])
    def asymmetric():
        if request.is_json:
            data = request.get_json()
            action = data.get('action')
            
            if action == 'generate':
                hybrid_signer = HybridSignature()
                private_key, public_key = hybrid_signer.generate_rsa_keys()
                return jsonify({
                    'privateKey': private_key,
                    'publicKey': public_key
                })
        
        return jsonify({'error': 'Invalid request'})

    # --- DOWNLOAD FILE ---
    @app.route('/download/<filename>')
    def download_file(filename):
        safe_name = secure_filename(filename)
        file_path = os.path.join(app.config['SIGNED_FOLDER'], safe_name)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        return send_file(file_path, as_attachment=True)

    # --- ERROR HANDLERS ---
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'error': 'File terlalu besar. Maksimal ukuran upload adalah 16 MB.'}), 413

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'error': 'Halaman atau endpoint tidak ditemukan.'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': 'Terjadi kesalahan pada server.'}), 500

    return app

# Instance aplikasi default untuk kompatibilitas langsung
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    debug_mode = app.config.get('DEBUG', True)
    app.run(host=host, port=port, debug=debug_mode)