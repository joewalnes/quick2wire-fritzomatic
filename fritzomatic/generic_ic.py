from fritzomatic.xmlbuilder import XMLBuilder

def generate_schematic(component):
  svg = XMLBuilder()
  warnings = []
  errors = []

  pins = component['pins']
  if pins % 2 != 0:
    errors.append('Pins must be an even number')
  if pins < 2:
    errors.append('Expected at least 2 pins')
  if pins > 100:
    errors.append('Too many pins (max 100)') # Sanity check

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
    text.pin-label.left {
      text-anchor: start;
    }
    text.pin-label.right {
      text-anchor: end;
    }
  """

  with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2', width=164.7, height=302.70001, viewBox='0 0 1830 3363.333'):
    with svg('defs'):
      svg('style', css, type='text/css')
    with svg('g', id='schematic', transform='translate(0, 333)'):
      # Title
      svg('text', component.get('label', 'IC'), x=915, y=-100, _class='label')
      # Outer package
      svg('rect', x=315, y=15, width=1200, height=300 * pins / 2 + 300, _class='outer-package')
      for connector_id, connector in component.get('connectors', {}).items():
        n = int(connector_id)
        if n < 1:
          warnings.append('Ignored connector "%s" - value should start at 1' % connector_id)
        elif n <= pins / 2:
          # Left
          level = n
          svg('text', connector.get('label', connector_id), x=390, y=300 * level + 50, _class='pin-label left')
          svg('line', x1=15, x2=300, y1=300 * level + 15, y2=300 * level + 15, _class='connector')
        elif n <= pins:
          # Right
          level = pins + 1 - n
          svg('text', connector.get('label', connector_id), x=1440, y=300 * level + 50, _class='pin-label right')
          svg('line', x1=1515, x2=1800, y1=300 * level + 15, y2=300 * level + 15, _class='connector')
        else:
          warnings.append('Ignored connector "%s" because component only has %d pins.' % (connector_id, pins))

  return svg, warnings, errors
