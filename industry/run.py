import sys
import os

# Ensure backend package is in python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
