#!/usr/bin/env python

import unittest

from fritzomatic.xmlbuilder import XMLBuilder

class XMLBuilderTestCase(unittest.TestCase):

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
    self.assertEqual(expected.strip(), str(node).strip())

if __name__ == '__main__':
  unittest.main()
