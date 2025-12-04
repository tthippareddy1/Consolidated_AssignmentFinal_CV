#!/usr/bin/env python3
"""
Production Backend for Task 1: Stereo Measurement
For deployment to Render or similar cloud services
"""

import os
from task1_backend import app

if __name__ == '__main__':
    # Use PORT from environment variable (for Render/Heroku)
    port = int(os.environ.get('PORT', 5001))
    # Run in production mode
    app.run(host='0.0.0.0', port=port, debug=False)

