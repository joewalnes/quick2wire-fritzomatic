"""
Easy XML document builder.

-Joe Walnes
"""

import re

from StringIO import StringIO
from xml.dom.minidom import Document

class XMLBuilder(object):
  """
  A mini-DSL for generating nested XML. Use the Python 'with'
  statement to created nested levels.

  Example:
    node = XMLBuilder()
    with node('people'):
      with node('person', id=123, type='real'):
        node('first-name', 'Joe')
        node('last-name', 'Walnes')
      with node('person', id=456, type='fictional'):
        node('first-name', 'Father')
        node('last-name', 'Christmas')
    print node

  Result:
    <people>
      <person id="123" type="real">
        <first-name>Joe</first-name>
        <last-name>Walnes</last-name>
      </person>
      <person id="456" type="fictional">
        <first-name>Father</first-name>
        <last-name>Christmas</last-name>
      </person>
    </people>

  To specify attributes that have reserved Python words (e.g. 'class'),
  you should give it an underscore prefix, which will be automatically
  stripped. e.g. node('foo', _class='bar') -> <foo class="bar"/>
  """
  def __init__(self):
    self.document = Document()
    self.last = self.document
    self.parent = self.document

  def __call__(self, name, text=None, **kwargs):
    el = self.document.createElement(name)
    if text:
      el.appendChild(self.document.createTextNode(str(text)))
    for name in kwargs:
      cleaned_name = re.compile('__').sub('-', name)
      cleaned_name = re.compile('^_').sub('', cleaned_name)
      el.setAttribute(cleaned_name, str(kwargs[name]))
    self.last = el
    self.parent.appendChild(el)
    return self

  def __enter__(self):
    self.parent = self.last

  def __exit__(self, type, value, traceback):
    self.parent = self.parent.parentNode

  def __str__(self):
    # Minidom has a toprettyxml() method, but it outputs additional whitespace around text
    # nodes, which confuses Fritzing. This is a cut-down XML pretty printer. It doesn't
    # deal with every possible XML document - but it will cope with anything that xmlbuilder
    # can build.

    def escape(str):
      return str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    def write(out, element, indent):
      out.write('%s<%s' % (indent, escape(element.tagName)))
      for k, v in element.attributes.items():
        out.write(' %s="%s"' % (escape(k), escape(v)))
      if len(element.childNodes) == 1 and element.childNodes[0].nodeType == Document.TEXT_NODE:
        # If the child is a single text node, write it on the same line.
        out.write('>%s</%s>\n' % (escape(element.childNodes[0].data), escape(element.tagName)))
      elif element.childNodes:
        # Otherwise, indent and recurse to children
        out.write('>\n')
        for child in element.childNodes:
          if child.nodeType == Document.ELEMENT_NODE:
            write(out, child, indent + '  ')
        out.write('%s</%s>\n' % (indent, escape(element.tagName)))
      else:
        # Empty elements
        out.write('/>\n')

    out = StringIO()
    write(out, self.document.childNodes[0], '')
    out.seek(0)
    return out.getvalue()

