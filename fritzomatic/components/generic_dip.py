import math

from fritzomatic.xmlbuilder import XMLBuilder
from fritzomatic.component import Component

class GenericDIP(Component):

  def __init__(self, data):
    self.data = data

  def validate(self):
    warnings = []
    errors = []

    pins = self.data['pins']
    if pins % 2 != 0:
      errors.append('Pins must be an even number')
    if pins < 2:
      errors.append('Expected at least 2 pins')
    if pins > 100:
      errors.append('Too many pins (max 100)') # Sanity check

    return warnings, errors

  def metadata(self):
    meta = XMLBuilder()

    with meta('module',
        fritzingVersion='0.7.1b.03.10.5908',
        moduleId=self.module_id()):
      # Core info
      meta('version', '4') # TODO
      meta('author', 'Fritzomatic') # TODO
      meta('title', self.title())
      meta('label', self.label())
      meta('date', '2012-04-16') # TODO

      # Tags
      with meta('tags'):
        for tag in self.tags():
          meta('tag', tag)

      # Additional properties
      properties = {
          'package'            : 'DIP (Dual Inline) [THT]',
          'family'             : self.label(), # TODO
          'editable pin labels': 'false',
          'chip label'         : self.label(),
          'part number'        : self.title(),
          'pins'               : self.data['pins'],
          'spacing'            : '300mil',
      }
      with meta('properties'):
        for k, v in properties.items():
          meta('property', v, _name=k)

      meta('description', self.description())

      # Other views
      with meta('views'):
        with meta('iconView'):
          with meta('layers', image='icon/%s.svg' % self.module_id()):
            meta('layer', layerId='icon')
        with meta('breadboardView'):
          with meta('layers', image='breadboard/%s.svg' % self.module_id()):
            meta('layer', layerId='breadboard')
        with meta('schematicView'):
          with meta('layers', image='schematic/%s.svg' % self.module_id()):
            meta('layer', layerId='schematic')
        with meta('pcbView'):
          with meta('layers', image='pcb/%s.svg' % self.module_id()):
            meta('layer', layerId='copper0')
            meta('layer', layerId='silkscreen')
            meta('layer', layerId='copper1')

      # Connector meta-data
      with meta('connectors'):
        for connector_id, connector in self.connectors().items():
          with meta('connector', id='connector%s' % connector_id, type='male', _name=connector.get('label', connector_id)):
            meta('description', connector.get('description', ''))
            with meta('views'):
              with meta('breadboardView'):
                meta('p', layer='breadboard', svgId='connector%spin' % connector_id, terminalId='connector%sterminal' % connector_id)
              with meta('schematicView'):
                meta('p', layer='schematic', svgId='connector%spin' % connector_id, terminalId='connector%sterminal' % connector_id)
              with meta('pcbView'):
                meta('p', layer='copper0', svgId='connector%spin' % connector_id)
                meta('p', layer='copper1', svgId='connector%spin' % connector_id)

    return meta

  def icon(self):
    pins = min(self.data['pins'], 6) # Show no more than 6 pins on icon
    icon = self.data.get('icon', None)
    if icon:
      label1 = icon.get('label1', 'IC')
      label2 = icon.get('label2', None)
    else:
      label1 = self.data.get('label', 'IC')
      label2 = None
    return self._breadboard_component('icon', pins, label1, label2)

  def breadboard(self):
    pins = self.data['pins']
    label1 = self.data.get('label', 'IC')
    label2 = None
    return self._breadboard_component('breadboard', pins, label1, label2)

  def schematic(self):
    svg = XMLBuilder()
    pins = self.data['pins']

    width = 1830
    height = 150 * pins + 670

    pin_style = 'font-size:130px; fill:#000000; stroke:none; font-family:DroidSans,sans-serif;'
    title_style = ('font-size:235px; text-align:center; line-height:125%; writing-mode:lr; '
        + 'text-anchor:middle; fill:#000000; stroke:none; font-family:DroidSans,sans-serif;')
    connector_style = 'fill:none; stroke-width:0;'
    line_style = 'fill:none; stroke:#000000; stroke-width:30; stroke-linecap:round; stroke-linejoin:round;'

    with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2',
        width='%fin' % (width / 1000.0),
        height='%fin' % (height / 1000.0),
        viewBox='0 0 %d %d' % (width, height)):
      with svg('g', id='schematic', transform='translate(0, 333)'):
        # Title
        svg('text', self.data.get('label', 'IC'), x=915, y=-100, style=title_style)
        # Outer package
        svg('rect', x=315, y=15, width=1200, height=300 * pins / 2 + 300, style=line_style)
        for connector_id, connector in self.data.get('connectors', {}).items():
          n = int(connector_id)
          if n > 0 and n <= pins / 2:
            # Left
            level = n
            svg('text', connector.get('label', connector_id), x=390, y=300 * level + 50, style='text-anchor: start; %s' % pin_style)
            svg('text', n, x=234, y=300 * level - 30, style='text-anchor: end; %s' % pin_style)
            svg('line', x1=15, x2=300, y1=300 * level + 15, y2=300 * level + 15, style='%s %s' % (connector_style, line_style))
            svg('rect', id='connector%spin'      % connector_id, x=0, y=300 * level, width=300, height=30, style=connector_style)
            svg('rect', id='connector%sterminal' % connector_id, x=0, y=300 * level, width=30 , height=30, style=connector_style)
          elif n > 0 and n <= pins:
            # Right
            level = pins + 1 - n
            svg('text', connector.get('label', connector_id), x=1440, y=300 * level + 50, style='text-anchor: end; %s' % pin_style)
            svg('text', n, x=1595, y=300 * level - 30, style='text-anchor: start; %s' % pin_style)
            svg('line', x1=1515, x2=1800, y1=300 * level + 15, y2=300 * level + 15, style='%s %s' % (connector_style, line_style))
            svg('rect', id='connector%spin'      % connector_id, x=1530, y=300 * level, width=300, height=30, style=connector_style)
            svg('rect', id='connector%sterminal' % connector_id, x=1800, y=300 * level, width=30, height=30, style=connector_style)

    return svg

  def pcb(self):
    svg = XMLBuilder()
    pins = self.data['pins']

    width = 420
    height = 50 * pins + 20
    with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2',
        width='%fin' % (width / 1000.0),
        height='%fin' % (height / 1000.0),
        viewBox='0 0 %d %d' % (width, height)):

      # Top and bottom copper layers
      for layer_id in ['copper0', 'copper1']:
        with svg('g', id=layer_id):
          for connector_id, connector in self.data.get('connectors', {}).items():
            n = int(connector_id)
            if n > 0 and n <= pins / 2:
              # Left
              level = n
              if n == 1:
                # First pin has square outline to make it easy to identify
                svg('rect', x=32.5, y=(100 * level - 67.5), width=55, height=55, stroke='rgb(255, 191, 0)', stroke__width=20, fill='none')
              svg('circle', id='connector%spin' % connector_id, cx=60, cy=(100 * level - 40), r=27.5, stroke='rgb(255, 191, 0)', stroke__width=20, fill='none')
            elif n > 0 and n <= pins:
              # Right
              level = pins + 1 - n
              svg('circle', id='connector%spin' % connector_id, cx=360, cy=(100 * level - 40), r=27.5, stroke='rgb(255, 191, 0)', stroke__width=20, fill='none')

      # Silk screen layer
      with svg('g', id='silkscreen'):
        bottom_edge = pins * 50 + 10
        svg('line', x1=10 , y1=10         , x2=160, y2=10         , stroke='white', stroke__width=10) # Top edge (left segment)
        svg('line', x1=260, y1=10         , x2=410, y2=10         , stroke='white', stroke__width=10) # Top edge (right segment)
        svg('line', x1=10 , y1=10         , x2=10 , y2=bottom_edge, stroke='white', stroke__width=10) # Left edge
        svg('line', x1=410, y1=bottom_edge, x2=410, y2=10         , stroke='white', stroke__width=10) # Right edge
        svg('line', x1=10 , y1=bottom_edge, x2=410, y2=bottom_edge, stroke='white', stroke__width=10) # Bottom edge

    return svg

  def _breadboard_component(self, layer_id, pins, label1, label2):
    svg = XMLBuilder()
    width = pins * 50
    height = 330
    with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2',
        width='%fin' % (width / 1000.0),
        height='%fin' % (height / 1000.0),
        viewBox='0 0 %d %d' % (width, height)):
      with svg('g', id=layer_id):
        # Main case
        svg('rect', x=0, y=30   , width=width, height=270,  fill='#303030', stroke__width=0) # Main component
        svg('rect', x=0, y=30   , width=width, height=24.6, fill='#3D3D3D', stroke__width=0) # Top edge
        svg('rect', x=0, y=275.4, width=width, height=24.6, fill='#000000', stroke__width=0) # Bottom edge
        svg('polygon', points='0,30,-7.5,54.6,-7.5,275.4,0,300', fill='#141414', stroke__width=0, transform='translate(' + str(width) + ', 0)') # Right edge
        svg('polygon', points='0,30,7.5,54.6,7.5,275.4,0,300'  , fill='#1F1F1F', stroke__width=0) # Left edge
        # Tab (indented semi-circle at end)
        svg('polygon', points='50,115,7.5,114.6,5.6,135.8,5.6,165,50,165'  , fill='#1C1C1C', stroke__width=0) # Top quadrant
        svg('polygon', points='7.5,215.5,50,215.5,50,165,5.6,165,5.6,194.2', fill='#383838', stroke__width=0) # Bottom quadrant
        svg('path', d='M5.6,135.8l0,58.3c14.7,-1.7,26.2,-14,26.2,-29.2C31.8,149.7,20.4,137.5,5.6,135.8z', fill='#262626', stroke__width=0) # Inner
        svg('path', d='M7.5,54.6L7.5,114.5c23.8,4.5,41.9,25.3,41.9,50.4c0,25.1,-18,46,-41.9,50.5L7.5,215.5l50,0L57.5,54.6L7.5,54.6z', fill='#303030', stroke__width=0) # Outer mask
        # Markings
        svg('circle', cx=65, cy=234.7, r=20.6, fill='#212121', stroke__width=0) # Orientation dot
        if label2:
          svg('text', label1, x=65, y=142.5, fill='#e6e6e6', stroke__width=0, font__family='OCRA', text__anchor='start', stroke='none', font__size=80)
          svg('text', label2, x=65, y=226.5, fill='#e6e6e6', stroke__width=0, font__family='OCRA', text__anchor='start', stroke='none', font__size=80)
        else:
          svg('text', label1, x=65, y=165, fill='#e6e6e6', stroke__width=0, font__family='OCRA', text__anchor='start', stroke='none', font__size=80)

        # Pins
        for pin in range(pins):
          level = math.floor(pin / 2)
          pin_label = pin + 1
          if pin % 2 == 0:
            # Top row
            svg('rect', id='connector%dpin'      % pin_label, x=(100 * level + 35), y=0, width=30, height=43.4, fill='#8c8c8c', stroke__width=0)
            svg('rect', id='connector%dterminal' % pin_label, x=(100 * level + 35), y=0, width=30, height=30  , fill='#8c8c8c', stroke__width=0)
            if level == 0: # Leftmost column
              points='85,43.4,85,32.6,65,23.4,35,23.4,35,43.4'
            elif level == pins / 2 - 1: # Rightmost column
              points='64,43.4,65,23.4,35,23.4,15,32.6,15,43.4'
            else: # All the others
              points='85,43.4,85,32.6,65,23.4,35,23.4,15,32.6,15,43.4'
            svg('polygon', points=points, transform='translate(' + str(100 * level) + ',0)', fill='#8c8c8c', stroke__width=0)
          else:
            # Bottom row
            svg('rect', id='connector%dpin'      % pin_label, x=(100 * level + 35), y=286.6, width=30, height=43.4, fill='#8c8c8c', stroke__width=0)
            svg('rect', id='connector%dterminal' % pin_label, x=(100 * level + 35), y=300,   width=30, height=30  , fill='#8c8c8c', stroke__width=0)
            if level == 0: # Leftmost column
              points='35,286.6,35,306.6,65,306.6,85,297.4,85,286.6'
            elif level == pins / 2 - 1: # Rightmost column
              points='15,286.6,15,297.4,35,306.6,65,306.6,65,286.6'
            else: # All the others
              points='15,286.6,15,297.4,35,306.6,65,306.6,85,297.4,85,286.6'
            svg('polygon', points=points, transform='translate(' + str(100 * level) + ',0)', fill='#8c8c8c', stroke__width=0)

    return svg
