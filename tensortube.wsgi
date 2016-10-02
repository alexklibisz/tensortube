import sys,os
sys.path.insert(0, '/home/ubuntu/tensortube')
os.chdir("/home/ubuntu/tensortube")
from server.main import app as application
