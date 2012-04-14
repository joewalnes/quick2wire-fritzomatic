from fritzomatic.format import to_json, to_urltoken

class Component(object):

  def label(self):
    return self.data['label']

  def json(self):
    return to_json(self.data)

  def urltoken(self):
    return to_urltoken(self.data)
