from fritzomatic.xmlbuilder import XMLBuilder

def validate(component):
  warnings = []
  errors = []

  pins = component['pins']
  if pins % 2 != 0:
    errors.append('Pins must be an even number')
  if pins < 2:
    errors.append('Expected at least 2 pins')
  if pins > 100:
    errors.append('Too many pins (max 100)') # Sanity check

  return warnings, errors

def generate_schematic(component):
  svg = XMLBuilder()
  warnings, errors = validate(component)

  pins = component['pins']

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

  with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2', width=300, height=300, viewBox='0 0 1515 ' + str(300 * pins / 2 + 670)):
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
          svg('text', connector.get('label', connector_id), x=390, y=300 * level + 50, _class='pin-label', style='text-anchor: start')
          svg('text', n, x=234, y=300 * level - 30, _class='pin-label', style='text-anchor: end')
          svg('line', x1=15, x2=300, y1=300 * level + 15, y2=300 * level + 15, _class='connector')
        elif n <= pins:
          # Right
          level = pins + 1 - n
          svg('text', connector.get('label', connector_id), x=1440, y=300 * level + 50, _class='pin-label', style='text-anchor: end')
          svg('text', n, x=1595, y=300 * level - 30, _class='pin-label', style='text-anchor: start')
          svg('line', x1=1515, x2=1800, y1=300 * level + 15, y2=300 * level + 15, _class='connector')
        else:
          warnings.append('Ignored connector "%s" because component only has %d pins.' % (connector_id, pins))

  return svg, warnings, errors

def generate_pcb(component):
  svg = XMLBuilder()
  warnings, errors = validate(component)

  pins = component['pins']

  css = """
    .copper-hole {
      stroke: rgb(255, 191, 0);
      stroke-width: 20px;
      fill: none;
    }
    .silkscreen-line {
      stroke: #ffffff;
      stroke-width: 10px;
    }
  """

  with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2', width=300, height=300, viewBox='0 0 420 ' + str(50 * pins + 20)):
    with svg('defs'):
      svg('style', css, type='text/css')

    # Top and bottom copper layers
    for layer_id in ['copper0', 'copper1']:
      with svg('g', id=layer_id):
        for connector_id, connector in component.get('connectors', {}).items():
          n = int(connector_id)
          if n < 1:
            warnings.append('Ignored connector "%s" - value should start at 1' % connector_id)
          elif n <= pins / 2:
            # Left
            level = n
            if n == 1:
              # First pin has square outline to make it easy to identify
              svg('rect', x=32.5, y=(100 * level - 67.5), width=55, height=55, _class='copper-hole')
            svg('circle', cx=60, cy=(100 * level - 40), r=27.5, _class='copper-hole')
          elif n <= pins:
            # Right
            level = pins + 1 - n
            svg('circle', cx=360, cy=(100 * level - 40), r=27.5, _class='copper-hole')
          else:
            warnings.append('Ignored connector "%s" because component only has %d pins.' % (connector_id, pins))

    # Silk screen layer
    with svg('g', id='silkscreen'):
      bottom_edge = pins * 50 + 10
      svg('line', x1=10 , y1=10         , x2=160, y2=10         , _class='silkscreen-line') # Top edge (left segment)
      svg('line', x1=260, y1=10         , x2=410, y2=10         , _class='silkscreen-line') # Top edge (right segment)
      svg('line', x1=10 , y1=10         , x2=10 , y2=bottom_edge, _class='silkscreen-line') # Left edge
      svg('line', x1=410, y1=bottom_edge, x2=410, y2=10         , _class='silkscreen-line') # Right edge
      svg('line', x1=10 , y1=bottom_edge, x2=410, y2=bottom_edge, _class='silkscreen-line') # Bottom edge

  return svg, warnings, errors

