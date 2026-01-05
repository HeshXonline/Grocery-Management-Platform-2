# WSGI Configuration for PythonAnywhere
# Copy this content to your WSGI configuration file on PythonAnywhere

import sys
import os

# IMPORTANT: Replace YOUR_USERNAME with your actual PythonAnywhere username
project_home = '/home/YOUR_USERNAME/Grocery-Management-Platform-2'

# Add your project directory to sys.path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as file:
        exec(file.read(), {'__file__': activate_this})

# Import FastAPI application
from main import app as application

# Optional: Add CORS if needed
# from fastapi.middleware.cors import CORSMiddleware
# application.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
