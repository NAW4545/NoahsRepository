import sys
sys.path.append("../scraper/programs")
sys.path.append("../database")

import slo_db
import checkData
import unittest
import slo_queries
from unittest.mock import patch
import pymysql
from PLODB import PLODB
from PLOScraper import PLOScraper

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        "Scrape all programs and insert them into the test database once per run."

        print('scraping pages: ')
        self.scraper = PLOScraper()
        allPgmList = self.scraper.getAllPLOs()

        self.connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='',
                                         db='slo_db',
                                         cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        # scrape all programs and insert them into the database
        db = PLODB(self.connection)
        # recreate tables
        for statement in slo_db.create_slo_db:
            print('Running: ', statement)
            self.cursor.execute(statement)

        for pgmDict in allPgmList:
            print("Inserting: ", f"{pgmDict['program']}")
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
    def test_noncred_esl(self):
        "Noncredit Certificate in life skills should have correct data."
        self.cursor.execute(slo_queries.queries['program_data'], checkData.noncred_esl['program'])
        row = self.cursor.fetchone()
        # the row should contain the expected data
        self.assertEqual(row['prog_name'], checkData.noncred_esl['program'])
        self.assertEqual(row['sp_name'], checkData.noncred_esl['super_program'])
        self.assertEqual(row['dep_name'], checkData.noncred_esl['department'])
        self.assertEqual(row['deg_type'], checkData.noncred_esl['deg_type'])
        self.assertEqual("".join(row['prog_desc'].split()), "".join(checkData.noncred_esl['description'].split()))

    def test_noncred_esl_plos(self):
        "Noncredit Certificate in life skills should have correct plos."
        for plo in checkData.noncred_esl['plos']:
            # check that each plo appears in the database with the foreign key set
            self.cursor.execute("""
                SELECT COUNT(pout_desc) PLOCount
                FROM poutcomes
                JOIN programs ON poutcomes.prog_id=programs.prog_id
                WHERE pout_desc=%s""",
                plo)
            row = self.cursor.fetchone()
            self.assertGreater(row['PLOCount'], 0)

    def test_noncred_esl_courses(self):
        "Noncredit Certificate in life skills should have correct courses."
        for c_dict in checkData.noncred_esl['courses']:
            # check that each course appears in the database with the foreign key set
            self.cursor.execute("""
                SELECT COUNT(cour_code)
                FROM programs
                JOIN programs_courses ON programs_courses.prog_id=programs.prog_id
                JOIN degrees on degrees.deg_id=programs.deg_id
                JOIN courses ON programs_courses.cour_id=courses.cour_id
                WHERE cour_code=%s AND prog_name=%s""",
                (c_dict['cour_code'], checkData.noncred_esl['program']))
            row = self.cursor.fetchone()
            self.assertGreater(row['COUNT(cour_code)'], 0)


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
