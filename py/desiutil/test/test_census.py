# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""Test desiutil.census.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
# The line above will help with 2to3 support.
import unittest

has_mock = True
try:
    from unittest.mock import call, patch
except ImportError:
    has_mock = False

has_commonpath = True
try:
    from os.path import commonpath
except ImportError:
    has_commonpath = False


class MockLogger(object):
    """Foo
    """

    def error(self, message):
        print(message)


class TestCensus(unittest.TestCase):
    """Test desiutil.census.
    """

    @classmethod
    def setUpClass(cls):
        from os.path import dirname, join
        cls.data_dir = join(dirname(__file__), 't')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ScannedFile(self):
        """Test simple object storing file data.
        """
        from ..census import ScannedFile
        f = ScannedFile('foo.txt', 12345, 1973)
        self.assertEqual(f.filename, 'foo.txt')
        self.assertEqual(f.size, 12345)
        self.assertEqual(f.year, 1973)
        self.assertFalse(f.islink)
        self.assertFalse(f.isexternal)
        self.assertIsNone(f.linkname)
        self.assertIsNone(f.linksize)
        self.assertIsNone(f.linkyear)

    def test_get_options(self):
        """Test command-line argument parsing.
        """
        from ..census import get_options
        options = get_options([])
        self.assertFalse(options.verbose)
        options = get_options(['--verbose'])
        self.assertTrue(options.verbose)
        options = get_options(['-c', 'foo.yaml'])
        self.assertEqual(options.config, 'foo.yaml')

    @unittest.skipUnless(has_mock, "Skipping test that requires unittest.mock.")
    def test_walk_error(self):
        """Test error-handling function for os.walk().
        """
        from ..census import walk_error
        with patch('desiutil.log.desi_logger') as mock:
            try:
                raise OSError(2, 'File not found', 'foo.txt')
            except OSError as e:
                walk_error(e)
            calls = [call.error("[Errno 2] File not found: 'foo.txt'")]
            self.assertListEqual(mock.mock_calls, calls)
        with patch('desiutil.log.desi_logger') as mock:
            try:
                raise OSError(2, 'File not found', 'foo.txt', None, 'bar.txt')
            except OSError as e:
                walk_error(e)
            calls = [call.error("[Errno 2] File not found: 'foo.txt' -> 'bar.txt'")]
            self.assertListEqual(mock.mock_calls, calls)

    def test_year(self):
        """Test conversion of mtime to year.
        """
        from ..census import year
        from time import gmtime
        mtime = 1475692367.0
        self.assertEqual(year(mtime), 2017)
        self.assertEqual(year(mtime, fy=False), 2016)

    @unittest.skipUnless(has_commonpath, "Skipping test that requires os.path.commonpath().")
    def test_in_path(self):
        """Test directory hierarchy checker.
        """
        from ..census import in_path
        self.assertTrue(in_path('/foo/bar/baz', '/foo/bar/baz/a/b/c/foo.txt'))
        self.assertTrue(in_path('/foo/bar/baz', '/foo/bar/baz/a'))
        self.assertFalse(in_path('/foo/bar/baz', '/foo/bar/baz-x2'))
        self.assertFalse(in_path('/foo/bar/baz', '/foo/baz/bar'))

    def test_output_csv(self):
        """Test CSV writer.
        """
        from os import remove
        from os.path import join
        from collections import OrderedDict
        from ..census import output_csv
        csvfile = join(self.data_dir, 'test_output_csv.csv')
        d = OrderedDict()
        d['/foo/bar'] = {2000: {'number': 2, 'size': 20},
                         2001: {'number': 2, 'size': 20},
                         2002: {'number': 2, 'size': 20}}
        d['/foo/bar/baz'] = {2000: {'number': 1, 'size': 10},
                             2001: {'number': 1, 'size': 10},
                             2002: {'number': 1, 'size': 10}}
        dd = OrderedDict()
        dd['/a/b/c'] = {2001: {'number': 2, 'size':50},
                        2002: {'number': 4, 'size': 100},
                        2003: {'number': 2, 'size': 50}}
        dd['/a/b/c/d'] = {2002: {'number': 2, 'size': 50}}
        output_data = output_csv([d, dd], csvfile)
        datatext = """Directory,FY2000 Number,FY2000 Size,FY2001 Number,FY2001 Size,FY2002 Number,FY2002 Size,FY2003 Number,FY2003 Size
/foo/bar,2,20,4,40,6,60,6,60
/foo/bar/baz,1,10,2,20,3,30,3,30
/a/b/c,0,0,2,50,6,150,8,200
/a/b/c/d,0,0,0,0,2,50,2,50"""
        data = [row.split(',') for row in datatext.split('\n')]
        self.assertEqual(len(output_data), len(data))
        for k in range(len(data)):
            self.assertListEqual(output_data[k], data[k])
        remove(csvfile)


def test_suite():
    """Allows testing of only this module with the command::

        python setup.py test -m <modulename>
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
