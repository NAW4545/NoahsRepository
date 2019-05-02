#! /usr/bin/env python3
import pymysql
# installed mysql python connector from https://dev.mysql.com/downloads/connector/python/
# pip install pymysql

# csci36@zippymail.info
# Username: WlH9s7G8vy
# Password: uH0YWN3msY
# Database Name: WlH9s7G8vy
# Server: remotemysql.com
# Port: 3306

# To set the foreign keys when inserting data, the order should be
# degree type&department > super_program > program > poutcomes & courses

class PLODB():
    def __init__(self, connection=None):
        "Create a connection to the database."

        if connection is not None:
            self.connection = connection
            self.close_on_del = False
        else:
            self.close_on_del = True
            self.connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='',
                                             db='slo_db_test',
                                             cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def __del__(self):
        "Close the database connection on destruction."
        if self.close_on_del is True:
            self.connection.close()

    def insert(self, plo_data):
        """ Insert a program, it's PLOs and associated data into the database.
            @plo_data: A dictionary containing the plo data. The format should be
                the same as that returned by PLOScraper.getPLOs()
                {
                    'pid': pid,
                    'super_program': listed under 'Program Details' (Multimedia Studies Program, Computer Science),
                    'program': program (ex. Wallpaper Design),
                    'plos': a list of PLOs (['plo 1', 'plo 2']),
                    'department': department name (Business Education, Digital Arts and Design),
                    'description': program description,
                    'chair': department chair,
                    'deg_type': degree code (AA, AS-T, CERT),
                    'courses': a list of dictionaries containting course names and codes within the degree program
                               [{'cour_code': 'CSCI 20',
                                 'cour_name': 'Programming and Aphorisms I'
                                 }]
                }
        """

        # This is a workaround. Having a list of dictionaries causes
        # TypeError: sequence item 0: expected str instance, dict found
        # for any query
        course_list = plo_data['courses']
        plo_data = {key:value for key, value in plo_data.items() if key is not 'courses'}

        # attempt to insert all fields from the plo dictionary
        # duplicate entries are ignored

        # attempt to insert degree type
        self.cursor.execute(""" INSERT INTO degrees VALUES(0, %(deg_type)s)
                                ON DUPLICATE KEY UPDATE deg_id = deg_id;""", plo_data)

        # attempt to insert department
        self.cursor.execute(""" INSERT INTO departments VALUES(0, %(department)s, %(chair)s)
                                ON DUPLICATE KEY UPDATE dep_id = dep_id;""", plo_data)

        # attempt to insert the super program
        self.cursor.execute(
            """INSERT INTO super_programs
               VALUES(%(pid)s,
                      %(super_program)s,
                      (SELECT dep_id FROM departments WHERE dep_name=%(department)s)
                )
                ON DUPLICATE KEY UPDATE sp_id = sp_id;
            """, plo_data)

        # insert the program and description, setting the keys for degreetype and super program
        self.cursor.execute(
            """INSERT INTO programs
                VALUES(0,
                    %(program)s,
                    %(description)s,
                    (SELECT deg_id FROM degrees WHERE deg_type=%(deg_type)s),
                    (SELECT sp_id FROM super_programs WHERE sp_id=%(pid)s)
                )
                ON DUPLICATE KEY UPDATE prog_id = prog_id;""",
            plo_data)

        # insert each plo, setting the foreign key as the id of the program
        for plo in plo_data['plos']:
            self.cursor.execute(
                """INSERT INTO poutcomes
                   VALUES( 0,
                           %s,
                           (SELECT prog_id FROM programs
                            WHERE prog_name=%s
                            AND deg_id=(SELECT deg_id FROM degrees WHERE deg_type=%s))
                    )
                    ON DUPLICATE KEY UPDATE pout_id = pout_id;""",
                (plo, plo_data['program'], plo_data['deg_type'])
            )

        for c_dict in course_list:
            self.cursor.execute(
                """INSERT INTO courses
                   VALUES( 0,
                           %(cour_code)s,
                           %(cour_name)s,
                           NULL
                    )
                    ON DUPLICATE KEY UPDATE cour_id = cour_id;
                """,
                (c_dict)
            )
            # create an entry in the join table
            self.cursor.execute(
                """INSERT INTO programs_courses
                   VALUES(
                        (SELECT prog_id FROM programs
                         JOIN degrees on programs.deg_id=degrees.deg_id
                         WHERE prog_name=%s AND deg_type=%s),
                        (SELECT cour_id FROM courses WHERE cour_code=%s)
                   )
                   ON DUPLICATE KEY UPDATE cour_id = cour_id;
                 """,
                 (plo_data['program'], plo_data['deg_type'], c_dict['cour_code'])
            )
        self.connection.commit()

def main():
    db = PLODB()

    ms_serv_cert = {
        'deg_type': 'CERT',
        'pid': '714',
        'super_program': 'Computer Science',
        'program': 'Microsoft Server Administration',
        'plos': ['Implement a core Windows Server 2012 infrastructure in an existing enterprise environment.',
                 'Implement, manage, maintain and provision services and infrastructure in a Windows Server 2012 environment.',
                 'Identify labor market needs and properly prepare for the most relevant industry certification exams.',
                 ],
        'department': "Sustainable Technologies Computer Science & Design",
        'description': '',
        'chair': 'Luke Sathrum, Chair (530) 895-2219',
        'courses': [{'cour_code': 'CSCI 70', 'cour_name': 'Installing and Configuring Windows Server 2012'},
                    {'cour_code': 'CSCI 71', 'cour_name': 'Administering Windows Server 2012'},
                    {'cour_code': 'CSCI 72', 'cour_name': 'Configuring Advanced Windows 2012 Server Services'}]
    }
    print(ms_serv_cert['deg_type'])
    db.insert(ms_serv_cert)

if __name__ == '__main__':
    main()
