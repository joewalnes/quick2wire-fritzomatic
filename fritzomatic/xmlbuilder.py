"""
Easy XML document builder.

-Joe Walnes
"""

import re

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
      cleaned_name = re.compile('^_').sub('', name)
      el.setAttribute(cleaned_name, str(kwargs[name]))
    self.last = el
    self.parent.appendChild(el)
    return self

  def __enter__(self):
    self.parent = self.last

  def __exit__(self, type, value, traceback):
    self.parent = self.parent.parentNode

  def __str__(self):
    return self.document.toprettyxml(indent='  ')
