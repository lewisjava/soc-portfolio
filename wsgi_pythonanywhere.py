# ─────────────────────────────────────────────────────────────────────────────
# PythonAnywhere WSGI configuration
# ─────────────────────────────────────────────────────────────────────────────
# In the PythonAnywhere "Web" tab, set your WSGI configuration file to point
# here, OR copy the contents below into the WSGI file PythonAnywhere generates.
#
# IMPORTANT: change 'YOUR_USERNAME' to your actual PythonAnywhere username.
# ─────────────────────────────────────────────────────────────────────────────

import sys

# The path to your project folder on PythonAnywhere
project_home = '/home/YOUR_USERNAME/soc-portfolio'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import the Flask app object as "application" (PythonAnywhere requires this name)
from app import app as application
