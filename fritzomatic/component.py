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

  def module_id(self):
    return 'fedcf3d723271139dab3cc83d369dc6d' # TODO

  def icon_filename(self):
    return '%s_icon.svg' % self.module_id()

  def breadboard_filename(self):
    return '%s_breadboard.svg' % self.module_id()

  def schematic_filename(self):
    return '%s_schematic.svg' % self.module_id()

  def pcb_filename(self):
    return '%s_pcb.svg' % self.module_id()
