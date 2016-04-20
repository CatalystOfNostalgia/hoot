activate_this = '/home/ubuntu/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, "/var/www/html/hoot/")
from hoot import app as application


