INSERT IGNORE INTO degrees VALUES(0, 'CERT');
INSERT IGNORE INTO degrees VALUES(0, 'AS');
INSERT IGNORE INTO degrees VALUES(0, 'CA');
INSERT IGNORE INTO degrees VALUES(0, 'AS-T');
INSERT IGNORE INTO degrees VALUES(0, 'AA-T');
INSERT IGNORE INTO degrees VALUES(0, 'AA');

-- insert departments

INSERT IGNORE INTO departments VALUES(0, 'Computer Science', 'chair');
INSERT IGNORE INTO departments VALUES(0, 'Administration of Justice', 'chair');
INSERT IGNORE INTO departments VALUES(0, 'Fashion', 'chair');

-- insert programs

INSERT IGNORE INTO programs VALUES(0,
'AS Degree in Computer Animation and Game Development'
,
'This program meets the lower division major preparation for a similar major at CSU, Chico. Visit website for details www.assist.org

Students in Computer Animation and Game Development use art and technology to design and create multimedia environments that communicate, inform, and entertain. Computer Animation and Game Development provides a foundation for students who wish to pursue further studies in digital animation, video game design, 3-D modeling, texture art, concept art, special effects art, graphic art, storyboard art, and game programming. The program prepares students for transfer to the Computer Animation and Game Development program at California State University, Chico and for similar majors at other four-year colleges and universities.'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS'),
(SELECT dep_id FROM departments WHERE dep_name='Computer Science')
);

INSERT IGNORE INTO programs VALUES(0,
'AS Degree in Computer Information Systems'
,
'The transfer major listed here partially reflects requirements for the Bachelor of Science in Computer Information Systems at CSU, Chico. Students planning to transfer should contact a counselor for more information on program and transfer requirements.
Computer Information Systems (CIS) as a field focuses on practical applications of technology to support organizations. The program includes a range of subjects, including end-user Information Technology (IT) systems, IT systems analysis and design, software development, and mathematics. Potential careers for CIS graduates include IT consultant, programmer/analyst, application developer, Quality Assurance Specialist, IT support specialist, IT project manager, and many other roles in the IT industry.
'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS'),
(SELECT dep_id FROM departments WHERE dep_name='Computer Science')
);

INSERT IGNORE INTO programs VALUES(0,
'AS Degree in Computer System Administration'
,
'The Computer System Administration program prepares students for industry standard certification exams and entry-level positions as computer support technicians and computer system administrators. The core curriculum covers Microsoft server installation, configuration, troubleshooting, and maintenance. No prerequisite skills are required for students to enroll in the program.

The program offers courses that prepare students for a variety of industry certification exams, including Microsoft MCSA, CompTIA A+, CompTIA Linux+, CompTIA Network+, and CompTIA Security+.
'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS'),
(SELECT dep_id FROM departments WHERE dep_name='Computer Science')
);

INSERT IGNORE INTO programs VALUES(0,
'Certificate of Achievement in Fashion Merchandising'
,
'See AS Degree in Fashion Merchandising.

Gainful Employment Information
Certificate of Achievement in Fashion Merchandising:
www.butte.edu/curriculum/gainful-employment/0134800CA.html
'
,
(SELECT deg_id FROM degrees WHERE deg_type='CA'),
(SELECT dep_id FROM departments WHERE dep_name='Fashion')
);

INSERT IGNORE INTO programs VALUES(0,
'Certificate in Clothing Construction'
,
''
,
(SELECT deg_id FROM degrees WHERE deg_type='CERT'),
(SELECT dep_id FROM departments WHERE dep_name='Fashion')
);

INSERT IGNORE INTO programs VALUES(0,
'AS-T Degree in Administration of Justice'
,
'Students completing Associate Degrees for Transfer are guaranteed admission to the CSU system. Please see the beginning of the "Academic Programs" section for details.'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS-T'),
(SELECT dep_id FROM departments WHERE dep_name='Administration of Justice')
);

INSERT IGNORE INTO programs VALUES(0,
'AS Degree in Criminal Justice '
,
'The Criminal Justice degree is designed for students who plan to earn a Bachelor\'s degree in Criminal Justice or related fields at CSU, Chico. This transfer major may also serve as the basis for students who are interested in pre-law. Visit website for details www.assist.org'
,
(SELECT deg_id FROM degrees WHERE deg_type='AS'),
(SELECT dep_id FROM departments WHERE dep_name='Administration of Justice')
);


-- insert poutcomes
INSERT IGNORE INTO poutcomes VALUES(0,
  'Design and implement basic software solutions using the building blocks of modern computer software systems.',
  1
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Install, configure, maintain, and network Microsoft desktop computer workstations.',
  1
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Implement a core Windows Server 2012 infrastructure in an existing enterprise environment.',
  1
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Design, implement, test, and debug algorithms to solve a variety of problems.',
  2
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Apply structured and object-oriented approaches to the design and implementation of computer programs.',
  2
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Design, build, configure, and maintain small to medium-sized Cisco networks utilizing switches, routers, and WAN connections.',
  2
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Implement, manage, maintain and provision services and infrastructure in a Windows Server 2012 environment.',
  3
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'List and describe the formal and dramatic elements that comprise a well- designed video game and conceptualize and refine an idea for a video game.',
  3
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Perform legal research independently and interpret, analyze and defend appellate court decisions.',
  3
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Identify and describe modus operandi, basic crime scene investigation, proper identification and collection of evidence.',
  4
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Explain the historical development and philosophy of law.',
  4
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Demonstrate an understanding of complex laws, court decisions, the court system and legal process and their impact on government, business and society.',
  5
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Identify and describe modus operandi, basic crime scene investigation, proper identification and collection of evidence.',
  5
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Effectively interpret, integrate, synthesize and apply complex information from multiple sources.',
  6
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Demonstrate an understanding of complex laws, court decisions, the court system and legal process and their impact on government, business and society.',
  6
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Identify and describe modus operandi, basic crime scene investigation, proper identification and collection of evidence.',
  7
);

INSERT IGNORE INTO poutcomes VALUES(0,
  'Perform legal research independently and interpret, analyze and defend appellate court decisions.',
  7
);
