insert_test_data = []
insert_test_data.append("INSERT IGNORE INTO degrees VALUES(1, 'CERT');")
insert_test_data.append("INSERT IGNORE INTO degrees VALUES(2, 'AS');")
insert_test_data.append("INSERT IGNORE INTO degrees VALUES(3, 'CA');")
insert_test_data.append("INSERT IGNORE INTO degrees VALUES(4, 'AS-T');")
insert_test_data.append("INSERT IGNORE INTO degrees VALUES(5, 'AA-T');")
insert_test_data.append("INSERT IGNORE INTO degrees VALUES(6, 'AA');")

# -- insert departments

insert_test_data.append("INSERT IGNORE INTO departments VALUES(1, 'Digital Arts and Design', 'chair');")
insert_test_data.append("INSERT IGNORE INTO departments VALUES(2, 'Sustainable Technologies Computer Science & Design', 'chair');")


# -- insert super programs

insert_test_data.append("INSERT IGNORE INTO super_programs VALUES(1, 'Computer Science', (SELECT dep_id FROM departments WHERE dep_name='Digital Arts and Design'));")
insert_test_data.append("INSERT IGNORE INTO super_programs VALUES(2, 'Administration of Justice', (SELECT dep_id FROM departments WHERE dep_name='Sustainable Technologies Computer Science & Design'));")
insert_test_data.append("INSERT IGNORE INTO super_programs VALUES(3, 'Fashion', (SELECT dep_id FROM departments WHERE dep_name='Digital Arts and Design'));")

# -- insert programs

insert_test_data.append("""INSERT IGNORE INTO programs VALUES(1,
'AS Degree in Computer Animation and Game Development'
,
'This program meets the lower division major preparation for a similar major at CSU, Chico. Visit website for details www.assist.org

Students in Computer Animation and Game Development use art and technology to design and create multimedia environments that communicate, inform, and entertain. Computer Animation and Game Development provides a foundation for students who wish to pursue further studies in digital animation, video game design, 3-D modeling, texture art, concept art, special effects art, graphic art, storyboard art, and game programming. The program prepares students for transfer to the Computer Animation and Game Development program at California State University, Chico and for similar majors at other four-year colleges and universities.'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS'),
(SELECT sp_id FROM super_programs WHERE sp_name='Computer Science')
);""")

insert_test_data.append("""INSERT IGNORE INTO programs VALUES(2,
'AS Degree in Computer Information Systems'
,
'The transfer major listed here partially reflects requirements for the Bachelor of Science in Computer Information Systems at CSU, Chico. Students planning to transfer should contact a counselor for more information on program and transfer requirements.
Computer Information Systems (CIS) as a field focuses on practical applications of technology to support organizations. The program includes a range of subjects, including end-user Information Technology (IT) systems, IT systems analysis and design, software development, and mathematics. Potential careers for CIS graduates include IT consultant, programmer/analyst, application developer, Quality Assurance Specialist, IT support specialist, IT project manager, and many other roles in the IT industry.
'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS'),
(SELECT sp_id FROM super_programs WHERE sp_name='Computer Science')
);""")

insert_test_data.append("""INSERT IGNORE INTO programs VALUES(3,
'AS Degree in Computer System Administration'
,
'The Computer System Administration program prepares students for industry standard certification exams and entry-level positions as computer support technicians and computer system administrators. The core curriculum covers Microsoft server installation, configuration, troubleshooting, and maintenance. No prerequisite skills are required for students to enroll in the program.

The program offers courses that prepare students for a variety of industry certification exams, including Microsoft MCSA, CompTIA A+, CompTIA Linux+, CompTIA Network+, and CompTIA Security+.
'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS'),
(SELECT sp_id FROM super_programs WHERE sp_name='Computer Science')
);""")

insert_test_data.append("""INSERT IGNORE INTO programs VALUES(4,
'Certificate of Achievement in Fashion Merchandising'
,
'See AS Degree in Fashion Merchandising.

Gainful Employment Information
Certificate of Achievement in Fashion Merchandising:
www.butte.edu/curriculum/gainful-employment/0134800CA.html
'
,
(SELECT deg_id FROM degrees WHERE deg_type='CA'),
(SELECT sp_id FROM super_programs WHERE sp_name='Fashion')
);""")

insert_test_data.append("""INSERT IGNORE INTO programs VALUES(5,
'Certificate in Clothing Construction'
,
''
,
(SELECT deg_id FROM degrees WHERE deg_type='CERT'),
(SELECT sp_id FROM super_programs WHERE sp_name='Fashion')
);""")

insert_test_data.append("""INSERT IGNORE INTO programs VALUES(6,
'AS-T Degree in Administration of Justice'
,
'Students completing Associate Degrees for Transfer are guaranteed admission to the CSU system. Please see the beginning of the "Academic Programs" section for details.'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS-T'),
(SELECT sp_id FROM super_programs WHERE sp_name='Administration of Justice')
);""")

insert_test_data.append("""INSERT IGNORE INTO programs VALUES(7,
'AS Degree in Criminal Justice '
,
'The Criminal Justice degree is designed for students who plan to earn a Bachelors degree in Criminal Justice or related fields at CSU, Chico. This transfer major may also serve as the basis for students who are interested in pre-law. Visit website for details www.assist.org'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS'),
(SELECT sp_id FROM super_programs WHERE sp_name='Administration of Justice')
);""")


# -- insert poutcomes

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(1,
  'Design and implement basic software solutions using the building blocks of modern computer software systems.',
  1
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(2,
  'Install, configure, maintain, and network Microsoft desktop computer workstations.',
  1
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(3,
  'Implement a core Windows Server 2012 infrastructure in an existing enterprise environment.',
  1
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(4,
  'Design, implement, test, and debug algorithms to solve a variety of problems.',
  2
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(5,
  'Apply structured and object-oriented approaches to the design and implementation of computer programs.',
  2
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(6,
  'Design, build, configure, and maintain small to medium-sized Cisco networks utilizing switches, routers, and WAN connections.',
  2
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(7,
  'Implement, manage, maintain and provision services and infrastructure in a Windows Server 2012 environment.',
  3
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(8,
  'List and describe the formal and dramatic elements that comprise a well- designed video game and conceptualize and refine an idea for a video game.',
  3
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(9,
  'Perform legal research independently and interpret, analyze and defend appellate court decisions.',
  3
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(10,
  'Identify and describe modus operandi, basic crime scene investigation, proper identification and collection of evidence.',
  4
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(11,
  'Explain the historical development and philosophy of law.',
  4
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(12,
  'Demonstrate an understanding of complex laws, court decisions, the court system and legal process and their impact on government, business and society.',
  5
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(13,
  'Identify and describe modus operandi, basic crime scene investigation, proper identification and collection of evidence.',
  5
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(14,
  'Effectively interpret, integrate, synthesize and apply complex information from multiple sources.',
  6
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(15,
  'Demonstrate an understanding of complex laws, court decisions, the court system and legal process and their impact on government, business and society.',
  6
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(16,
  'Identify and describe modus operandi, basic crime scene investigation, proper identification and collection of evidence.',
  7
);""")

insert_test_data.append("""INSERT IGNORE INTO poutcomes VALUES(17,
  'Perform legal research independently and interpret, analyze and defend appellate court decisions.',
  7
);""")

# insert courses
insert_test_data.append("""
  INSERT IGNORE INTO courses VALUES(1,
  'cls 154',
  'classes in learning something 1',
  ''
);""")

insert_test_data.append("""
  INSERT IGNORE INTO courses VALUES(2,
  'cls 254',
  'classes in learning something 2',
  ''
);""")

insert_test_data.append("""
  INSERT IGNORE INTO courses VALUES(3,
  'cls 354',
  'classes in learning something 3',
  ''
);""")

insert_test_data.append("""
  INSERT IGNORE INTO courses VALUES(4,
  'cls 4354',
  'classes in learning something 4',
  ''
);""")

insert_test_data.append("""
  INSERT IGNORE INTO courses VALUES(5,
  'cls 553',
  'classes in learning something 5',
  ''
);""")


# join with programs
insert_test_data.append("""
  INSERT IGNORE INTO programs_courses VALUES(
  1,
  1
);""")

insert_test_data.append("""
  INSERT IGNORE INTO programs_courses VALUES(
  2,
  2
);""")

insert_test_data.append("""
  INSERT IGNORE INTO programs_courses VALUES(
  3,
  3
);""")

insert_test_data.append("""
  INSERT IGNORE INTO programs_courses VALUES(
  4,
  4
);""")

insert_test_data.append("""
  INSERT IGNORE INTO programs_courses VALUES(
  5,
  5
);""")



# insert discussions


# insert assessments

if __name__ == '__main__':
	with open('slo_test_data.sql', 'w', encoding="utf-8") as f:
		for statement in insert_test_data:
			f.write(statement+"\n")
		f.close()
