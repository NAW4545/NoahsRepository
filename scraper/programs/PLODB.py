#! /usr/bin/env python3
import pymysql
# installed mysql+python connector
# pip install pymysql

# csci36@zippymail.info
# Username: WlH9s7G8vy
# Password: uH0YWN3msY
# Database Name: WlH9s7G8vy
# Server: remotemysql.com
# Port: 3306

# When inserting data degree type should be inserted first
# followed by department>program>plos

class PLODB():
    def __init__(self):
        # connect to database
        self.connection = pymysql.connect(host='remotemysql.com',
                             user='WlH9s7G8vy',
                             password='uH0YWN3msY',
                             db='WlH9s7G8vy',
                             cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def insert(self, plo_data):
        # insert a program into the database

        # attempt to insert degree type
        self.cursor.execute("INSERT IGNORE INTO degrees VALUES(0, %(deg_type)s);", plo_data)

        # attempt to insert department
        self.cursor.execute("INSERT IGNORE INTO departments VALUES(0, %(department)s, %(chair)s);", plo_data)

        # insert the program and description, setting the keys for degreetype and department
        self.cursor.execute(
            """INSERT IGNORE INTO programs VALUES(0,
            %(program)s,
            %(description)s,
            (SELECT deg_id FROM degrees WHERE deg_type=%(deg_type)s),
            (SELECT dep_id FROM departments WHERE dep_name=%(department)s)
            );""",
            plo_data
        )

        # insert each plo, setting the foreign key as the id of the program
        for plo in plo_data['plos']:
            self.cursor.execute(
                """INSERT IGNORE INTO poutcomes VALUES(0,
                  %s,
                  (SELECT prog_id FROM programs WHERE prog_name=%s)
                );""",
                (plo, plo_data['program'])
            )

        self.connection.commit()

def main():
    test_plo_data = {
        'deg_type': 'AA-T',
        'department': 'Fashion',
        'chair': 'chair',
        'program': 'Certificate in Clothing Construction',
        'description':
            'The Computer System Administration program prepares students for industry standard certification exams and entry-level positions as computer support technicians and computer system administrators. The core curriculum covers Microsoft server installation, configuration, troubleshooting, and maintenance. No prerequisite skills are required for students to enroll in the program. The program offers courses that prepare students for a variety of industry certification   exams, including Microsoft MCSA, CompTIA A+, CompTIA Linux+, CompTIA Network+, and CompTIA Security+.',
        'plos': ['Implement a core Windows Server 2012 infrastructure in an existing enterprise environment.',
                'Perform legal research independently and interpret, analyze and defend appellate court decisions.',
                'Effectively interpret, integrate, synthesize and apply complex information from multiple sources.'],
    }
    db = PLODB()
    db.insert(test_plo_data)

if __name__ == '__main__':
    main()
