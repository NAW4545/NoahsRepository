import csv
import pymysql

def import_course_csv(csv_path):
    """ Import a csv containing course codes and outcomes, with each line formatted

        CRSCOD 15, Course outcome text

        @csv_path: The path to the csv.
    """
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)
        # for row in reader:
        #     print(row)
        #     c_code = row[0]
        #     c_lo = row[1]
        #     print(c_code, c_lo)

if __name__ == '__main__':
    c_outcome_list = import_course_csv('course_outcomes.csv')

    connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='slo_db_test',
                                     cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    for course in c_outcome_list:
        c_code = course[0]
        c_outcome = course[1]
        print(f"'{c_outcome}', '{c_code}'")

        cursor.execute("""
            INSERT INTO coutcomes
            VALUES(0,
                   %s,
                   (SELECT cour_id FROM courses WHERE cour_code=%s)
            )
        """, (c_outcome, c_code))
    connection.commit()
