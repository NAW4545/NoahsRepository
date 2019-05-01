DROP TABLE IF EXISTS programs_courses;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS plo_assessments;
DROP TABLE IF EXISTS discussions;
DROP TABLE IF EXISTS poutcomes;
DROP TABLE IF EXISTS programs;
DROP TABLE IF EXISTS degrees;
DROP TABLE IF EXISTS super_programs;
DROP TABLE IF EXISTS departments;

	CREATE TABLE degrees(
	deg_id INT AUTO_INCREMENT NOT NULL,
	deg_type VARCHAR(25) NOT NULL,
	PRIMARY KEY (deg_id),
	UNIQUE KEY (deg_type)
);

	CREATE TABLE departments(
	dep_id INT AUTO_INCREMENT NOT NULL,
	dep_name VARCHAR(250) NOT NULL,
	dep_chair VARCHAR(100) NOT NULL,
	PRIMARY KEY (dep_id),
	UNIQUE KEY (dep_name)
);

	CREATE TABLE super_programs(
	sp_id INT AUTO_INCREMENT NOT NULL,
	sp_name VARCHAR(255) NOT NULL,
	dep_id INT NOT NULL,
	PRIMARY KEY (sp_id),
	FOREIGN KEY (dep_id) REFERENCES departments (dep_id)
);

	CREATE TABLE programs(
	prog_id INT AUTO_INCREMENT NOT NULL,
	prog_name VARCHAR(255) NOT NULL,
	prog_desc TEXT,
	deg_id INT NOT NULL,
	sp_id INT NOT NULL,
	PRIMARY KEY (prog_id),
	FOREIGN KEY (deg_id) REFERENCES degrees (deg_id),
	FOREIGN KEY (sp_id) REFERENCES super_programs (sp_id)
);

	CREATE UNIQUE INDEX unique_program_degree
ON programs(prog_name(255), deg_id);

	CREATE TABLE poutcomes(
	pout_id INT AUTO_INCREMENT NOT NULL,
	pout_desc TEXT NOT NULL,
	prog_id INT NOT NULL,
	PRIMARY KEY (pout_id),
	FOREIGN KEY (prog_id) REFERENCES programs (prog_id)
);

	CREATE UNIQUE INDEX unique_poutcome
ON poutcomes(pout_desc(255), prog_id);

	CREATE TABLE discussions(
	discussion_id INT AUTO_INCREMENT NOT NULL,
	discussion_completed_by VARCHAR(100) NOT NULL,
	discussion_also_present TEXT,
	discussion_looking_back TEXT,
	discussion_findings TEXT,
	discussion_courses_assessed TEXT,
	discussion_programs_assessed TEXT,
	discussion_gelos_assessed TEXT,
	discussion_strategies TEXT,
	discussion_resources TEXT,
	discussion_date DATE NOT NULL,
	PRIMARY KEY (discussion_id)
);

	CREATE TABLE plo_assessments(
	pout_id INT AUTO_INCREMENT NOT NULL,
	discussion_id INT NOT NULL,
	plo_assess_date DATE NOT NULL,
	PRIMARY KEY (pout_id, discussion_id),
	FOREIGN KEY (pout_id) REFERENCES poutcomes (pout_id),
	FOREIGN KEY (discussion_id) REFERENCES discussions (discussion_id)
);

	CREATE TABLE courses(
	cour_id INT AUTO_INCREMENT NOT NULL,
	cour_code VARCHAR(50),
	cour_name VARCHAR(250),
	cour_desc TEXT,
	PRIMARY KEY (cour_id),
	UNIQUE KEY (cour_code)
);

	CREATE TABLE programs_courses(
	prog_id INT NOT NULL,
	cour_id INT NOT NULL,
	PRIMARY KEY (prog_id, cour_id),
	FOREIGN KEY (prog_id) REFERENCES programs (prog_id),
	FOREIGN KEY (cour_id) REFERENCES courses (cour_id)
);
