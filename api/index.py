import sys
import os

# Get absolute path of the directory containing this file (api/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get root directory (parent of api/)
root_dir = os.path.dirname(current_dir)
# Get backend directory
backend_dir = os.path.join(root_dir, 'backend')

# Add backend directory to sys.path so 'app' module can be found
sys.path.append(backend_dir)

from app.main import app
from mangum import Mangum

handler = Mangum(app)
