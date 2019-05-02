import sys
sys.path.append("../scraper/programs")
sys.path.append("../database")

import slo_db
import checkData
import slo_queries
from PLODB import PLODB
import unittest
import pymysql
from unittest.mock import patch

class TestPLODB(unittest.TestCase):

    def setUp(self):

        self.connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='',
                                         db='slo_db_test',
                                         cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        # recreate new tables in the database
        for statement in slo_db.create_slo_db:
            self.cursor.execute(statement)

    def test_program_insertion(self):
        "An inserted program's data should appear in the database."
        db = PLODB(self.connection)
        db.insert(checkData.noncred_esl)
        self.cursor.execute(slo_queries.queries['program_data'], checkData.noncred_esl['program'])
        row = self.cursor.fetchone()
        # the row should contain the inserted data
        self.assertEqual(row['prog_name'], checkData.noncred_esl['program'])
        self.assertEqual(row['sp_name'], checkData.noncred_esl['super_program'])
        self.assertEqual(row['dep_name'], checkData.noncred_esl['department'])
        self.assertEqual(row['deg_type'], checkData.noncred_esl['deg_type'])
        self.assertEqual("".join(row['prog_desc'].split()), "".join(checkData.noncred_esl['description'].split()))
        # plos should match test data
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

    def test_duplicate_insertion(self):
        "It should not insert a duplicate program entry."
        db = PLODB(self.connection)
        db.insert(checkData.noncred_esl)
        db.insert(checkData.noncred_esl)
        self.cursor.execute("""
            SELECT COUNT(prog_id) PCount
            FROM programs
            WHERE prog_name=%s""",
            checkData.noncred_esl['program'])
        self.assertEqual(self.cursor.fetchone()['PCount'], 1)


    def test_course_insertion(self):
        "An Inserted course should be related to the program."
        db = PLODB(self.connection)
        db.insert(checkData.noncred_esl)
        self.cursor.execute("""select cour_code
                        from programs
                        JOIN programs_courses ON programs_courses.prog_id=programs.prog_id
                        JOIN degrees on degrees.deg_id=programs.deg_id
                        JOIN courses ON programs_courses.cour_id=courses.cour_id
                        WHERE prog_name = %s AND deg_type = %s""", (checkData.noncred_esl['program'], checkData.noncred_esl['deg_type']))
        # Workaround, using fetchmany causes an unknown error
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



    # check foreign key assignment manually

    # check joins/queries for data retrieval\

    # a program can have many outcomes

    # a program can have many courses

    # a course can have many programs

    # a degree type can have many programs

    #




if __name__ == '__main__':
    unittest.main()
    # connection = pymysql.connect(host='localhost',
    #                                  user='root',
    #                                  password='',
    #                                  db='slo_db_test',
    #                                  cursorclass=pymysql.cursors.DictCursor)
    # cursor = connection.cursor()
    # er = checkData.noncred_esl['courses']
    # cursor.execute("""select cour_code, cour_name
    #                      from programs
    #                      JOIN programs_courses ON programs_courses.prog_id=programs.prog_id
    #                      JOIN degrees on degrees.deg_id=programs.deg_id
    #                      JOIN courses ON programs_courses.cour_id=courses.cour_id
    #                      WHERE prog_name = %s AND deg_type = %s""", (checkData.noncred_esl['program'], checkData.noncred_esl['deg_type']))
    # cs = list(cursor.fetchall())
    # for e in er:
    #     print(e in cs)

    # t = TestPLODB()
    # t._course_insertion()
    # course_dicts = checkData.noncred_esl['courses']
    # for course_dict in course_dicts:
    #     print(course_dict)
