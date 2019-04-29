import sys
sys.path.append("../scraper/programs")
sys.path.append("../database")

import slo_db
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
        self.test_plo_data = {
            'deg_type': 'AA-T',
            'department': 'Sustainable Technologies Computer Science & Design',
            'chair': 'chair name, (123) 456-4165',
            'program': 'Certificate in Clothing Construction',
            'super_program': 'Computer Science',
            'pid': '156',
            'description':
                """The Computer System Administration program prepares students for industry standard certification exams and entry-level positions as computer support technicians and computer system administrators. The core curriculum covers Microsoft server installation, configuration, troubleshooting, and maintenance. No prerequisite skills are required for students to enroll in the program. The program offers courses that prepare students for a variety of industry certification   exams, including Microsoft MCSA, CompTIA A+, CompTIA Linux+, CompTIA Network+, and CompTIA Security+.""",
            'plos': ['Implement a core Windows Server 2012 infrastructure in an existing enterprise environment.',
                    'Perform legal research independently and interpret, analyze and defend appellate court decisions.',
                    'Effectively interpret, integrate, synthesize and apply complex information from multiple sources.'],
        }

        # recreate new tables in the database
        for statement in slo_db.create_slo_db:
            self.cursor.execute(statement)


    def test_db_insertion(self):
        # check that an inserted program appears in the database
        db = PLODB(self.connection)
        db.insert(self.test_plo_data)
        self.cursor.execute("""SELECT * FROM programs WHERE prog_name=%s""", self.test_plo_data['program'])
        row = self.cursor.fetchone()
        self.assertEqual(row['prog_name'], self.test_plo_data['program'])


if __name__ == '__main__':
    unittest.main()
