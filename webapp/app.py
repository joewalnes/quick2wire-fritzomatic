#!/usr/bin/env python

import json
import os

from fritzomatic.generic_ic import generate_icon, generate_breadboard, generate_schematic, generate_pcb
from flask import send_from_directory, Flask, Response

app = Flask(__name__)

def parse_component():
  # TODO: Really parse this from request
  with open('examples/mcp23008.json') as f:
    return json.load(f)

@app.route('/')
def homepage():
  return """
    <style>
      img { border: 1px solid #aaaaaa; margin: 2px;}
    </style>
    <img src="/icon"       style="background-color: #cccccc;"><br>
    <img src="/breadboard" style="background-color: #cccccc;">
    <img src="/schematic"  style="background-color: #ffffff;">
    <img src="/pcb"        style="background-color: #69947a;">
  """

@app.route('/favicon.ico')
def favicon():
   return send_from_directory(os.path.join(app.root_path, 'static'),
       'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/icon')
def icon():
  component = parse_component()
  result, warnings, errors = generate_icon(component)
  return Response(str(result), mimetype='image/svg+xml')

@app.route('/breadboard')
def breadboard():
  component = parse_component()
  result, warnings, errors = generate_breadboard(component)
  return Response(str(result), mimetype='image/svg+xml')

@app.route('/schematic')
def schematic():
  component = parse_component()
  result, warnings, errors = generate_schematic(component)
  return Response(str(result), mimetype='image/svg+xml')

@app.route('/pcb')
def pcb():
  component = parse_component()
  result, warnings, errors = generate_pcb(component)
  return Response(str(result), mimetype='image/svg+xml')

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
