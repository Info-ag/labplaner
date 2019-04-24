#!/usr/bin/env python3

if __name__ == '__main__':
    import sys
    import os
    from app import create_app
    
    root = os.path.abspath(os.path.dirname(sys.argv[0]))
    # Get project root. This is required to load the correct config
    # file with relative paths.

    app, db = create_app(root)
    db.create_all()
    app.run(port=5000)
