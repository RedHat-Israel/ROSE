import json
from common import error

def parse(line):
    try:
        d = json.loads(line)
    except ValueError as e:
        raise error.InvalidMessage(str(e))
    if 'action' not in d:
        raise error.InvalidMessage("action required")
    return Message(d['action'], d.get('payload'))

class Message(object):

    def __init__(self, action, payload=None):
        self.action = action
        self.payload = payload

    def __str__(self):
        d = {'action': self.action, 'payload': self.payload}
        return json.dumps(d)

