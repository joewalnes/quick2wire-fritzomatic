import base64
import collections
import json
import zlib

def to_json(obj):
  return json.dumps(obj, indent=2)

def from_json(text):
  return json.loads(text, object_pairs_hook=collections.OrderedDict) # maintain key order

def to_urltoken(obj):
  return add_prefix('Z', 
      base64.urlsafe_b64encode(
        zlib.compress(
          json.dumps(obj), 9)))

def from_urltoken(text):
  return from_json(
      zlib.decompress(
        base64.urlsafe_b64decode(
          strip_prefix('Z', str(text)))))

# We use prefix in strings so we can easily identify the encoding types.

def add_prefix(prefix, text):
  return '%s%s' % (prefix, text)

def strip_prefix(prefix, text):
  return text[len(prefix):]

