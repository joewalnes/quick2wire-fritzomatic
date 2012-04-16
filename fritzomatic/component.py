from fritzomatic.format import to_json, to_urltoken

class Component(object):

  def title(self):
    return self.data.get('title', '')

  def label(self):
    return self.data.get('label', '')

  def description(self):
    return self.data.get('description', '')

  def tags(self):
    return self.data.get('tags', [])

  def connectors(self):
    return self.data.get('connectors', {})

  def json(self):
    return to_json(self.data)

  def urltoken(self):
    return to_urltoken(self.data)
