#!/usr/bin/env python

import unittest

from fritzomatic.xmlbuilder import XMLBuilder

class XMLBuilderTestCase(unittest.TestCase):

  def assertText(self, a, b):
    self.assertEqual(str(a).strip(), str(b).strip())

  def test_it(self):
    node = XMLBuilder()
    with node('people'):
      with node('person', id=123, type='real'):
        node('first-name', 'Joe')
        node('last-name', 'Walnes')
      with node('person', id=456, type='fictional'):
        node('first-name', 'Father')
        node('last-name', 'Christmas')

    expected = """
<?xml version="1.0" ?>
<people>
  <person id="123" type="real">
    <first-name>
      Joe
    </first-name>
    <last-name>
      Walnes
    </last-name>
  </person>
  <person id="456" type="fictional">
    <first-name>
      Father
    </first-name>
    <last-name>
      Christmas
    </last-name>
  </person>
</people>
 """
    self.assertText(expected, node)

  def test_allows_reserved_word_to_be_specified_with_underscore_prefix(self):
    node = XMLBuilder()
    with node('people'):
      node('person', _class='of 78')
    expected = """
<?xml version="1.0" ?>
<people>
  <person class="of 78"/>
</people>
 """
    self.assertText(expected, node)

if __name__ == '__main__':
  unittest.main()
