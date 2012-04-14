#!/usr/bin/env python

import collections
import json
import os

from fritzomatic.components.generic_dip import GenericDIP
from fritzomatic.format import from_json, from_urltoken, to_urltoken
from flask import send_from_directory, url_for, redirect, render_template, request, Flask, Response

app = Flask(__name__)

def parse_component(data):
  # TODO: Support multiple components.
  # TODO: Validate
  return GenericDIP(from_urltoken(data))

@app.route('/')
def homepage():
  with open('examples/mcp23008.json') as f:
    data = json.load(f, object_pairs_hook=collections.OrderedDict)
  return redirect(url_for('summary', data=to_urltoken(data)))

@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'),
      'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/update', methods=['POST'])
def update():
  data = request.form.get('data')
  if data:
    return redirect(url_for('summary', data=to_urltoken(from_json(data))))
  else:
    return 'No data'

@app.route('/component/<data>/')
def summary(data):
  component = parse_component(data)
  return render_template('summary.html', component=component)

@app.route('/component/<data>/json')
def dump_json(data):
  component = parse_component(data)
  return Response(str(component.json()), mimetype='text/plain')

@app.route('/component/<data>/icon')
def icon(data):
  component = parse_component(data)
  return Response(str(component.icon()), mimetype='image/svg+xml')

@app.route('/component/<data>/breadboard')
def breadboard(data):
  component = parse_component(data)
  return Response(str(component.breadboard()), mimetype='image/svg+xml')

@app.route('/component/<data>/schematic')
def schematic(data):
  component = parse_component(data)
  return Response(str(component.schematic()), mimetype='image/svg+xml')

@app.route('/component/<data>/pcb')
def pcb(data):
  component = parse_component(data)
  return Response(str(component.pcb()), mimetype='image/svg+xml')

# Go!
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  debug = bool(int(os.environ.get('DEBUG', '0')))
  app.run(host='0.0.0.0', port=port, debug=debug)
