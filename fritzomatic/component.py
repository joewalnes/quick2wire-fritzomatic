from fritzomatic.format import to_json, to_urltoken

class Component(object):

  def name(self):
    return self.data['name']

  def label(self):
    return self.data['label']

  def description(self):
    return self.data['description']

  def tags(self):
    return self.data['tags']

  def json(self):
    return to_json(self.data)

  def urltoken(self):
    return to_urltoken(self.data)
