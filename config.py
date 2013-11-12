import os
import json

dirpath = os.path.dirname(os.path.realpath(__file__))
config = json.loads(open(os.path.join(dirpath,'config.json'),'r').read())