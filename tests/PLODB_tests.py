import sys
sys.path.append("../scraper/programs")
sys.path.append("../database")

import slo_db
import checkData
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


    def test_db_insertion(self):
        "An inserted program should appear in the database."
        db = PLODB(self.connection)
        db.insert(checkData.noncred_esl)
        self.cursor.execute("""SELECT * FROM programs WHERE prog_name=%s""", self.test_plo_data['program'])
        row = self.cursor.fetchone()
        self.assertEqual(row['prog_name'], self.test_plo_data['program'])

    




if __name__ == '__main__':
    unittest.main()
