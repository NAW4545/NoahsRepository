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

    def setUp(self):
        self.connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='',
                                         db='slo_db_test',
                                         cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

        # recreate tables
        for statement in slo_db.create_slo_db:
            self.cursor.execute(statement)

    # all programs from the program list should be present in the database
    def test_all_programs(self):
        """ Scrape all programs and insert them into the test database, then check
            that all programs are present.
        """
        db = PLODB(self.connection)
        s = PLOScraper()
        allPgmList = s.getAllPLOs()
        for pgmDict in allPgmList:
            db.insert(pgmDict)

        scrapedPrograms = s.getProgramNames()
        self.cursor.execute("SELECT prog_name FROM programs")

        for row in self.cursor:
            self.assertTrue(row['prog_name'] in scrapedPrograms)


    # test whether a selection of programs have the expected data associated



if __name__ == '__main__':
    unittest.main()
