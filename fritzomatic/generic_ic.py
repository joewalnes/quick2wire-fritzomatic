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
    .pin-label {
      font-size: 130px;
      fill: #000000;
      stroke: none;
      font-family: DroidSans;
    }
    .pin-label.left {
      text-anchor: end;
    }
    .pin-label.right {
      text-anchor: start;
    }
  """

  with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2', width=164.7, height=302.70001, viewBox='0 0 1830 3363.333'):
    with svg('defs'):
      svg('style', css, type='text/css')
    with svg('g', id='schematic'):
      for connector_id, connector in component['connectors'].items():
        n = int(connector_id)
        if n < 1:
          warnings.append('Ignored connector "%s" - value should start at 1' % connector_id)
        elif n <= pins / 2:
          # Left
          svg('text', connector.get('label', connector_id), x=390, y=300 * n + 50, _class='pin-label left')
        elif n <= pins:
          # Right
          svg('text', connector.get('label', connector_id), x=1440, y=300 * (pins + 1 - n) + 50, _class='pin-label right')
          pass
        else:
          warnings.append('Ignored connector "%s" because component only has %d pins.' % (connector_id, pins))

  return svg, warnings, errors
