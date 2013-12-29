import json


def parse(line):
    d = json.loads(line)
    return Message(d['action'], d.get('payload'))


class Message(object):

    def __init__(self, action, payload=None):
        self.action = action
        self.payload = payload

    def __str__(self):
        d = {'action': self.action, 'payload': self.payload}
        return json.dumps(d)

