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

# Tables that should comprise the database
tables = [
	"PROGRAMS_COURSES",
	"COURSES",
	"COUTCOMES",
	"PROGRAMS",
	"POUTCOMES",
	"PLO_ASSESSMENTS",
	"DISCUSSIONS",
	"DEGREES",
	"SUPER_PROGRAMS",
	"DEPARTMENTS"
]

tableDescriptions = {
	"PROGRAMS_COURSES": "`PROGRAMS_COURSES` ( `COUR_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Course ID' , `PROG_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Program ID' , PRIMARY KEY (`COUR_ID`, `PROG_ID`)) ENGINE = InnoDB COMMENT = 'Programs and Courses (Composite entity)'",
	"COURSES": "`COURSES` ( `COUR_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Course ID' , `COUR_NAME` VARCHAR(250) NOT NULL COMMENT 'Course name' , `COUR_DESC` LONGTEXT NOT NULL COMMENT 'Course description' , PRIMARY KEY (`COUR_ID`)) ENGINE = InnoDB COMMENT = 'Courses'",
	"COUTCOMES": "`COUTCOMES` ( `COUT_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Course outcome ID' , `COUT_DESC` TEXT NOT NULL COMMENT 'Course outcome description' , `COUR_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Course ID' , PRIMARY KEY (`COUT_ID`)) ENGINE = InnoDB COMMENT = 'Course outcomes'",
	"PROGRAMS": "`PROGRAMS` ( `PROG_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Program ID' , `PROG_NAME` VARCHAR(250) NOT NULL COMMENT 'Program name' , `PROG_DESC` TEXT NOT NULL COMMENT 'Program description' , `DEG_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Degree ID' , `SP_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Super program ID' , PRIMARY KEY (`PROG_ID`), UNIQUE (`PROG_NAME`)) ENGINE = InnoDB COMMENT = 'Programs'",
	"POUTCOMES": "`POUTCOMES` ( `POUT_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Program outcome ID' , `POUT_DESC` TEXT NOT NULL COMMENT 'Program outcome description' , `PROG_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Program ID' , PRIMARY KEY (`POUT_ID`)) ENGINE = InnoDB COMMENT = 'Program outcomes'",
	"PLO_ASSESSMENTS": "`PLO_ASSESSMENTS` ( `POUT_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Program outcome ID' , `DISCUSSION_ID` BIGINT UNSIGNED NOT NULL COMMENT 'Discussion ID' , `PLO_ASSESS_DATE` DATE NOT NULL COMMENT 'PLO assessment date' , PRIMARY KEY (`POUT_ID`, `DISCUSSION_ID`)) ENGINE = InnoDB COMMENT = 'Program learning outcome assessments'"
}

tableAlterations = {
	"ALTER TABLE `COUTCOMES` ADD CONSTRAINT `Course ID` FOREIGN KEY (`COUR_ID`) REFERENCES `COURSES`(`COUR_ID`) ON DELETE RESTRICT ON UPDATE RESTRICT;"
}

# To set the foreign keys when inserting data, the order should be
# degree type&department > super_program > program > poutcomes

class PLODB():
	def __init__(self, connection=None):
		"Create a connection to the database."

		if connection is not None:
			self.connection = connection
			self.close_on_del = False
		else:
			self.close_on_del = True
			self.connection = pymysql.connect(host='remotemysql.com',
											 user='WlH9s7G8vy',
											 password='uH0YWN3msY',
											 db='WlH9s7G8vy',
											 cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.connection.cursor()

		# Clear out database and rebuild table structure
		cursor = self.cursor
		for table in tables:
			cursor.execute('DROP TABLE IF EXISTS %s CASCADE' % table)
			if tableDescriptions.__contains__(table):
				cursor.execute('CREATE TABLE %s' % tableDescriptions[table])

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
					'deg_type': degree code (AA, AS-T, CERT)
				}
		"""

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

		self.connection.commit()

def main():
	# test plo data represents a single program and its PLOs
	#db = PLODB()
	#db.insert(test_plo_data)
	return

if __name__ == "__main__":
	main()
