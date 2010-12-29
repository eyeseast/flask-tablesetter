#!/usr/bin/env python

import os
import shutil
import unittest
import urllib2
import yaml

from table_setter import commands
from table_setter.table import Table, TableDoesNotExist
from table_fu import TableFu

class TableTest(unittest.TestCase):
    
    def setUp(self):
        self.yml = open('table_setter/template/tables/example.yml')
        self.parsed = yaml.load(self.yml)
        self.yml.seek(0)
    
    def tearDown(self):
        self.yml.close()


class OptionsTest(TableTest):
    
    def testProse(self):
        table = Table(self.yml)
        self.assertEqual(table.deck, self.parsed['table']['deck'])
        self.assertEqual(table.footer, self.parsed['table']['footer'])
        self.assertEqual(table.title, self.parsed['table']['title'])
        
    def testStatus(self):
        table = Table(self.yml)
        self.assertTrue(table.live)


class TableFuTest(TableTest):

    def testColumns(self):
        table = Table(self.yml)
        columns = self.parsed['table']['column_options']['columns']
        self.assertEqual(table.data.columns, columns)

class FacetTest(unittest.TestCase):
    
    def setUp(self):
        self.yml = open('table_setter/template/tables/example_faceted.yml')
        self.parsed = yaml.load(self.yml)
        self.yml.seek(0)
    
    def tearDown(self):
        self.yml.close()

    def testFacets(self):
        table = Table(self.yml)
        options = self.parsed['table']['column_options']
        url = "http://spreadsheets.google.com/pub?key=tcSL0eqrj3yb5d6ljak4Dcw&output=csv"
        response = urllib2.urlopen(url)
        tf = TableFu(response, **options)
        tables = tf.facet_by('State')
        for i, t in enumerate(tables):
            self.assertEqual(t.table, table.data[i].table)
        
    def testSortable(self):
        table = Table(self.yml)
        self.assertFalse(table.sortable)

class RemoteTest(TableTest):
    
    def testNameCSV(self):
        table = Table(self.yml)
        self.assertEqual(table.url, 'http://spreadsheets.google.com/pub?key=thJa_BvqQuNdaFfFJMMII0Q&output=csv')

    def testDeferLoading(self):
        table = Table(self.yml)
        self.assertEqual(table._data, None)


class CommandTest(unittest.TestCase):
    
    def setUp(self):
        self.start_dir = os.getcwd()
        os.mkdir('testbed')
        os.chdir('testbed')
    
    def tearDown(self):
        os.chdir(self.start_dir)
        shutil.rmtree('testbed')
    
    def testInstall(self):
        self.assertFalse('test_set' in os.listdir('.'))
        # commands.install('test_set')
        args = commands.parser.parse_args('install test_set'.split())
        args.func(args)
        self.assertTrue('test_set' in os.listdir('.'))
        shutil.rmtree('test_set')


class AppTest(unittest.TestCase):
    
    def setUp(self):
        self.table_path = os.path.abspath('table_setter/template/tables')
    
    def testGetTable(self):
        t = Table.get(self.table_path, 'example')
        self.assertEqual(t.title, 'Failed Banks List')
    
    def testTableIndex(self):
        all = Table.all(self.table_path)
        results = {
            'example': 'Failed Banks List',
            'example_faceted': 'Appropriations by District', 
            'example_formatted': 'Stimulus Progress',
            'example_local': 'Browse All Approved Stimulus Highway Projects'
        }
        
        self.assertEqual(type(all), dict)
        
        for slug, title in results.items():
            self.assertEqual(title, all[slug].title)


class ErrorTest(AppTest):
    
    def testNoTable(self):
        self.assertRaises(
            TableDoesNotExist,
            Table.get,
            self.table_path, 'notatable',
        )


if __name__ == '__main__':
    unittest.main()
