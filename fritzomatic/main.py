#!/usr/bin/env python

import argparse
import json
import sys

from generic_ic import generate_schematic

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Generates a Fritzing component from simple JSON definition file.')
  parser.add_argument('input', metavar='INPUT', help='Input JSON file')
  args = parser.parse_args()

  with open(args.input) as f:
    component = json.load(f)
    svg, warnings = generate_schematic(component)
    for warning in warnings:
      print >> sys.stderr, 'WARNING:', warning
    print svg
