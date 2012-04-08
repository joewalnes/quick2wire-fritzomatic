#!/usr/bin/env python

import json
import os

from fritzomatic.generic_ic import generate_schematic
from flask import Flask, Response

app = Flask(__name__)

def parse_component():
  # TODO: Really parse this from request
  with open('examples/mcp23008.json') as f:
    return json.load(f)

@app.route('/')
def homepage():
  return '<img src="/schematic">'

@app.route('/schematic')
def schematic():
  component = parse_component()
  result, warnings, errors = generate_schematic(component)
  return Response(str(result), mimetype='image/svg+xml')

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
