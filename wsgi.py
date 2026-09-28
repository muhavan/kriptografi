"""
WSGI Entry Point untuk Server Produksi (Gunicorn / uWSGI / VPS)
Contoh command:
    gunicorn --bind 0.0.0.0:5000 wsgi:app
"""
import os
from app import create_app

# Ambil environment dari FLASK_ENV atau default production
env = os.environ.get('FLASK_ENV', 'production')
app = create_app(env)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port)
