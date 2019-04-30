import sys
sys.path.append("../scraper/programs")
sys.path.append("../database")

import slo_db
import unittest
from unittest.mock import patch
import pymysql
from PLODB import PLODB
from PLOScraper import PLOScraper

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        "Scrape all programs and insert them into the test database once per run."
        self.connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='',
                                         db='slo_db_test',
                                         cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

        # recreate tables
        for statement in slo_db.create_slo_db:
            self.cursor.execute(statement)

        # scrape all programs and insert them into the database
        db = PLODB(self.connection)
        self.scraper = PLOScraper()
        allPgmList = self.scraper.getAllPLOs()
        for pgmDict in allPgmList:
            db.insert(pgmDict)

    @classmethod
    def tearDownClass(self):
        self.connection.close()

    # all programs from the program list should be present in the database
    def test_all_programs_inserted(self):
        "All scraped programs should appear in the database."
        scrapedPrograms = self.scraper.getProgramNames()

        for programName in scrapedPrograms:
            self.cursor.execute("SELECT COUNT(prog_name) pCount FROM programs WHERE prog_name=%s", programName)
            self.assertTrue(self.cursor.fetchone()['pCount'] > 0)

    def test_190_programs(self):
        "The database should have 190 programs in the programs table."
        self.cursor.execute("SELECT COUNT(prog_name) pCount FROM programs")
        self.assertEqual(self.cursor.fetchone()['pCount'], 190)


    # test whether a selection of programs have the expected data associated



if __name__ == '__main__':

    unittest.main()

    # connection = pymysql.connect(host='localhost',
    #                                  user='root',
    #                                  password='',
    #                                  db='slo_db',
    #                                  cursorclass=pymysql.cursors.DictCursor)
    # cursor = connection.cursor()
    #
    # cursor.execute("SELECT COUNT(prog_name) pCount FROM programs WHERE prog_name=%s", '2D Animation and Games')
    #
    # print(cursor.fetchone()['pCount'])
