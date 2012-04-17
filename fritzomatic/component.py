from fritzomatic.format import to_json, to_urltoken
from StringIO import StringIO
from zipfile import ZipFile, ZIP_DEFLATED

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
    return 'svg.icon.%s.svg' % self.module_id()

  def breadboard_filename(self):
    return 'svg.breadboard.%s.svg' % self.module_id()

  def schematic_filename(self):
    return 'svg.schematic.%s.svg' % self.module_id()

  def pcb_filename(self):
    return 'svg.pcb.%s.svg' % self.module_id()

  def metadata_filename(self):
    return 'part.%s.fzp' % self.module_id()

  def fzpz_filename(self):
    return '%s.fzpz' % self.module_id()

  def fzpz(self):
    """Convert component to complete Fritzing .fzpz archive,
    which is basically a zip file containing the metadata
    and SVGs. Returns string of bytes"""
    data = StringIO()
    with ZipFile(data, compression=ZIP_DEFLATED, mode='w') as zf:
      zf.writestr(self.metadata_filename()  , str(self.metadata()))
      zf.writestr(self.icon_filename()      , str(self.icon()))
      zf.writestr(self.breadboard_filename(), str(self.breadboard()))
      zf.writestr(self.schematic_filename() , str(self.schematic()))
      zf.writestr(self.pcb_filename()       , str(self.pcb()))
    data.seek(0)
    return data.getvalue()
