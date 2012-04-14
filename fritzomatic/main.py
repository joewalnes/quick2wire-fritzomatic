#!/usr/bin/env python

import argparse
import collections
import json
import sys

from generic_ic import generate_schematic

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Generates a Fritzing component from simple JSON definition file.')
  parser.add_argument('input', metavar='INPUT', help='Input JSON file')
  args = parser.parse_args()

  with open(args.input) as f:
    component = json.load(f, object_pairs_hook=collections.OrderedDict)
    svg, warnings, errors = generate_schematic(component)
    for errors in errors:
      print >> sys.stderr, 'WARNING:', warning
    for warning in warnings:
      print >> sys.stderr, 'WARNING:', warning
    if len(errors):
      print >> sys.stderr, 'FAILED'
      sys.exit(1)
    else:
      print svg
      sys.exit(0)
