#!/usr/bin/env python

import json
import os
import urllib

from fritzomatic.generic_ic import generate_icon, generate_breadboard, generate_schematic, generate_pcb
from flask import send_from_directory, Flask, Response

app = Flask(__name__)

def parse_component(data):
  return json.loads(urllib.unquote(data))

@app.route('/')
def homepage():
  with open('examples/mcp23008.json') as f:
    component = json.load(f)
  url = 'component/%s/summary' % urllib.quote(json.dumps(component))
  return """
    <a href="%s">Example</a>
  """ % url

@app.route('/favicon.ico')
def favicon():
   return send_from_directory(os.path.join(app.root_path, 'static'),
       'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/component/<data>/summary')
def summary(data):
  component = parse_component(data)
  return """
    <style>
      img { border: 1px solid #aaaaaa; margin: 2px;}
    </style>
    <a href="icon"      ><img src="icon"       style="background-color: #cccccc;"></a><br>
    <a href="breadboard"><img src="breadboard" style="background-color: #cccccc;"></a>
    <a href="schematic" ><img src="schematic"  style="background-color: #ffffff;"></a>
    <a href="pcb"       ><img src="pcb"        style="background-color: #69947a;"></a>
    <p><a href="json">JSON</a></p>
  """

@app.route('/component/<data>/json')
def dump_json(data):
  component = parse_component(data)
  return Response(json.dumps(component, indent=2), mimetype='text/plain')

@app.route('/component/<data>/icon')
def icon(data):
  component = parse_component(data)
  result, warnings, errors = generate_icon(component)
  return Response(str(result), mimetype='image/svg+xml')

@app.route('/component/<data>/breadboard')
def breadboard(data):
  component = parse_component(data)
  result, warnings, errors = generate_breadboard(component)
  return Response(str(result), mimetype='image/svg+xml')

@app.route('/component/<data>/schematic')
def schematic(data):
  component = parse_component(data)
  result, warnings, errors = generate_schematic(component)
  return Response(str(result), mimetype='image/svg+xml')

@app.route('/component/<data>/pcb')
def pcb(data):
  component = parse_component(data)
  result, warnings, errors = generate_pcb(component)
  return Response(str(result), mimetype='image/svg+xml')

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
