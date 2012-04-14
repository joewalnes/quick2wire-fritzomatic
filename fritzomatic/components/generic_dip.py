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

  def icon(self):
    pins = min(self.data['pins'], 6) # Show no more than 6 pins on icon
    icon = self.data.get('icon', None)
    if icon:
      label1 = icon.get('label1', 'IC')
      label2 = icon.get('label2', None)
    else:
      label1 = self.data.get('label', 'IC')
      label2 = None
    return self._breadboard_component('0.3in', pins, label1, label2)

  def breadboard(self):
    pins = self.data['pins']
    label1 = self.data.get('label', 'IC')
    label2 = None
    return self._breadboard_component(300, pins, label1, label2)

  def schematic(self):
    css = """
      text {
        font-family: DroidSans;
      }
      rect.outer-package, line.connector {
        fill: none;
        stroke: #000000;
        stroke-width: 30;
        stroke-linecap: round;
        stroke-linejoin: round;
      }
      text.label {
        font-size: 235px;
        line-height: 125%;
        text-align: center;
        text-anchor: middle;
      }
      text.pin-label {
        font-size: 130px;
      }
    """
    svg = XMLBuilder()
    pins = self.data['pins']

    with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2', width=300, height=300, viewBox='0 0 1515 ' + str(300 * pins / 2 + 670)):
      with svg('defs'):
        svg('style', css, type='text/css')
      with svg('g', id='schematic', transform='translate(0, 333)'):
        # Title
        svg('text', self.data.get('label', 'IC'), x=915, y=-100, _class='label')
        # Outer package
        svg('rect', x=315, y=15, width=1200, height=300 * pins / 2 + 300, _class='outer-package')
        for connector_id, connector in self.data.get('connectors', {}).items():
          n = int(connector_id)
          if n > 0 and n <= pins / 2:
            # Left
            level = n
            svg('text', connector.get('label', connector_id), x=390, y=300 * level + 50, _class='pin-label', style='text-anchor: start')
            svg('text', n, x=234, y=300 * level - 30, _class='pin-label', style='text-anchor: end')
            svg('line', x1=15, x2=300, y1=300 * level + 15, y2=300 * level + 15, _class='connector')
          elif n > 0 and n <= pins:
            # Right
            level = pins + 1 - n
            svg('text', connector.get('label', connector_id), x=1440, y=300 * level + 50, _class='pin-label', style='text-anchor: end')
            svg('text', n, x=1595, y=300 * level - 30, _class='pin-label', style='text-anchor: start')
            svg('line', x1=1515, x2=1800, y1=300 * level + 15, y2=300 * level + 15, _class='connector')

    return svg

  def pcb(self):
    css = """
      .copper-hole {
        stroke: #F7BD13;
        stroke-width: 20px;
        fill: none;
      }
      .silkscreen-line {
        stroke: #ffffff;
        stroke-width: 10px;
      }
    """
    svg = XMLBuilder()
    pins = self.data['pins']

    with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2', width=300, height=300, viewBox='0 0 420 ' + str(50 * pins + 20)):
      with svg('defs'):
        svg('style', css, type='text/css')

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
                svg('rect', x=32.5, y=(100 * level - 67.5), width=55, height=55, _class='copper-hole')
              svg('circle', cx=60, cy=(100 * level - 40), r=27.5, _class='copper-hole')
            elif n > 0 and n <= pins:
              # Right
              level = pins + 1 - n
              svg('circle', cx=360, cy=(100 * level - 40), r=27.5, _class='copper-hole')

      # Silk screen layer
      with svg('g', id='silkscreen'):
        bottom_edge = pins * 50 + 10
        svg('line', x1=10 , y1=10         , x2=160, y2=10         , _class='silkscreen-line') # Top edge (left segment)
        svg('line', x1=260, y1=10         , x2=410, y2=10         , _class='silkscreen-line') # Top edge (right segment)
        svg('line', x1=10 , y1=10         , x2=10 , y2=bottom_edge, _class='silkscreen-line') # Left edge
        svg('line', x1=410, y1=bottom_edge, x2=410, y2=10         , _class='silkscreen-line') # Right edge
        svg('line', x1=10 , y1=bottom_edge, x2=410, y2=bottom_edge, _class='silkscreen-line') # Bottom edge

    return svg

  def _breadboard_component(self, size, pins, label1, label2):
    css = """
      rect, polygon, path, circle, text {
        stroke-width: 0;
      }
      .label {
        font-family: OCRA;
        font-size: 80px;
        text-anchor: start;
      }
    """
    svg = XMLBuilder()
    width = pins * 50
    with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2', width=size, height=size, viewBox='0 0 ' + str(width) + ' 330'):
      with svg('defs'):
        svg('style', css, type='text/css')
      with svg('g', id='breadboard'):
        # Main case
        svg('rect', x=0, y=30   , width=width, height=270,  fill='#303030') # Main component
        svg('rect', x=0, y=30   , width=width, height=24.6, fill='#3D3D3D') # Top edge
        svg('rect', x=0, y=275.4, width=width, height=24.6, fill='#000000') # Bottom edge
        svg('polygon', points='900,30,892.5,54.6,892.5,275.4,900,300'      , fill='#141414') # Right edge
        svg('polygon', points='0,30,7.5,54.6,7.5,275.4,0,300'              , fill='#1F1F1F') # Left edge
        # Tab (indented semi-circle at end)
        svg('polygon', points='50,115,7.5,114.6,5.6,135.8,5.6,165,50,165'  , fill='#1C1C1C') # Top quadrant
        svg('polygon', points='7.5,215.5,50,215.5,50,165,5.6,165,5.6,194.2', fill='#383838') # Bottom quadrant
        svg('path', d='M5.6,135.8l0,58.3c14.7,-1.7,26.2,-14,26.2,-29.2C31.8,149.7,20.4,137.5,5.6,135.8z', fill='#262626') # Inner
        svg('path', d='M7.5,54.6L7.5,114.5c23.8,4.5,41.9,25.3,41.9,50.4c0,25.1,-18,46,-41.9,50.5L7.5,215.5l50,0L57.5,54.6L7.5,54.6z', fill='#303030') # Outer mask
        # Markings
        svg('circle', cx=65, cy=234.7, r=20.6, fill='#212121') # Orientation dot
        if label2:
          svg('text', label1, x=65, y=142.5, fill='#e6e6e6', _class='label')
          svg('text', label2, x=65, y=226.5, fill='#e6e6e6', _class='label')
        else:
          svg('text', label1, x=65, y=165, fill='#e6e6e6', _class='label')

        # Pins
        for level in range(pins / 2):
          # Top row
          svg('rect', x=(100 * level + 35), y=0, width=30, height=43.4, fill='#8c8c8c')
          if level == 0: # Leftmost column
            points='85,43.4,85,32.6,65,23.4,35,23.4,35,43.4'
          elif level == pins / 2 - 1: # Rightmost column
            points='64,43.4,65,23.4,35,23.4,15,32.6,15,43.4'
          else: # All the others
            points='85,43.4,85,32.6,65,23.4,35,23.4,15,32.6,15,43.4'
          svg('polygon', points=points, transform='translate(' + str(100 * level) + ',0)', fill='#8c8c8c')
          # Bottom row
          svg('rect', x=(100 * level + 35), y=286.6, width=30, height=43.4, fill='#8c8c8c')
          if level == 0: # Leftmost column
            points='35,286.6,35,306.6,65,306.6,85,297.4,85,286.6'
          elif level == pins / 2 - 1: # Rightmost column
            points='15,286.6,15,297.4,35,306.6,65,306.6,65,286.6'
          else: # All the others
            points='15,286.6,15,297.4,35,306.6,65,306.6,85,297.4,85,286.6'
          svg('polygon', points=points, transform='translate(' + str(100 * level) + ',0)', fill='#8c8c8c')

    return svg
