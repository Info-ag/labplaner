"""Configuration

This package contains all configuration files:
    - `dev.cfg` for your base configuration, that is shared across `dev`, `test`
    and `prod`
    - `dev.cfg` for your development specific configuration
    - `test.cfg` for your test specific configuration
    - `prod.cfg` for your production specific configuration
    - `secret.cfg` *(optional)* for secrets **NEVER INCLUDE THIS IN YOU COMMIT**
"""

import os


###########
# Content #
###########
CONFIG_DIR = 'config'
BASE_CONFIG = os.path.join(CONFIG_DIR, 'base.cfg')
DEV_CONFIG = os.path.join(CONFIG_DIR, 'dev.cfg')
TEST_CONFIG = os.path.join(CONFIG_DIR, 'test.cfg')
PROD_CONFIG = os.path.join(CONFIG_DIR, 'prod.cfg')
SECRET_CONFIG = os.path.join(CONFIG_DIR, 'secret.cfg')