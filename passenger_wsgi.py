"""
Passenger WSGI Entry Point
Khusus untuk Hosting berbasis cPanel / hPanel Hostinger (CloudLinux / Phusion Passenger).
Hostinger "Setup Python App" memerlukan file ini sebagai Application Startup File,
dan objek WSGI harus bernama 'application'.
"""
import sys
import os

# Pastikan path direktori aplikasi berada di urutan teratas sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Set mode production secara default
os.environ.setdefault('FLASK_ENV', 'production')

# Import factory atau instance app Flask
from app import create_app

# Phusion Passenger mewajibkan nama WSGI callable adalah 'application'
application = create_app('production')
