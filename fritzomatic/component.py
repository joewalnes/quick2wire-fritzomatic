import json

class Component(object):

  def label(self):
    return self.data['label']

  def json(self):
    return json.dumps(self.data, indent=2)
