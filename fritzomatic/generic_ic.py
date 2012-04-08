from fritzomatic.xmlbuilder import XMLBuilder

def generate_schematic(component):
  svg = XMLBuilder()
  warnings = []
  pin_label_style = 'font-size:130px;text-anchor:end;fill:#000000;stroke:none;font-family:DroidSans'

  with svg('svg', xmlns='http://www.w3.org/2000/svg', version='1.2', width=164.7, height=302.70001, viewBox='0 0 1830 3363.333'):
    with svg('g', id='schematic'):
      pins = component['pins']
      for connector_id, connector in component['connectors'].items():
        n = int(connector_id)
        if n < 1:
          warnings.append('Ignored connector "%s" - value should start at 1' % connector_id)
        elif n <= pins / 2:
          # Left
          svg('text', connector.get('label', connector_id), x=390, y = 300 * n + 50)
        elif n <= pins:
          # Right
          pass
        else:
          warnings.append('Ignored connector "%s" because component only has %d pins.' % (connector_id, pins))

  return svg, warnings
