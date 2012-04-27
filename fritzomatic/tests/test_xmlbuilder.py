#!/usr/bin/env python

import unittest

from fritzomatic.xmlbuilder import XMLBuilder

class XMLBuilderTestCase(unittest.TestCase):

  def assertText(self, a, b):
    #print '====\n%s\n----\n%s\n====' % (str(a).strip(), str(b).strip())
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
<people>
  <person type="real" id="123">
    <first-name>Joe</first-name>
    <last-name>Walnes</last-name>
  </person>
  <person type="fictional" id="456">
    <first-name>Father</first-name>
    <last-name>Christmas</last-name>
  </person>
</people>
 """
    self.assertText(expected, node)

  def test_allows_reserved_word_to_be_specified_with_underscore_prefix(self):
    node = XMLBuilder()
    with node('people'):
      node('person', _class='of 78')
    expected = """
<people>
  <person class="of 78"/>
</people>
 """
    self.assertText(expected, node)

  def test_allows_dash_to_be_specified_with_double_underscore(self):
    node = XMLBuilder()
    with node('people'):
      node('person', last__name='person')
    expected = """
<people>
  <person last-name="person"/>
</people>
 """
    self.assertText(expected, node)

  def test_escapes_dodgy_chars(self):
    node = XMLBuilder()
    with node('people'):
      node('person', '&<>"', xname='&<>"')
    expected = """
<people>
  <person xname="&amp;&lt;&gt;&quot;">&amp;&lt;&gt;&quot;</person>
</people>
 """
    self.assertText(expected, node)

if __name__ == '__main__':
  unittest.main()
