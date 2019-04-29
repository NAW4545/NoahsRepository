create_slo_db = []
create_slo_db.append("DROP TABLE IF EXISTS plo_assessments;")
create_slo_db.append("DROP TABLE IF EXISTS discussions;")
create_slo_db.append("DROP TABLE IF EXISTS poutcomes;")
create_slo_db.append("DROP TABLE IF EXISTS programs;")
create_slo_db.append("DROP TABLE IF EXISTS degrees;")
create_slo_db.append("DROP TABLE IF EXISTS super_programs;")
create_slo_db.append("DROP TABLE IF EXISTS departments;")

create_slo_db.append("""
	CREATE TABLE degrees(
	deg_id INT AUTO_INCREMENT NOT NULL,
	deg_type VARCHAR(25) NOT NULL,
	PRIMARY KEY (deg_id),
	UNIQUE KEY (deg_type)
);""")

create_slo_db.append("""
	CREATE TABLE departments(
	dep_id INT AUTO_INCREMENT NOT NULL,
	dep_name VARCHAR(250) NOT NULL,
	dep_chair VARCHAR(100) NOT NULL,
	PRIMARY KEY (dep_id),
	UNIQUE KEY (dep_name)
);""")

create_slo_db.append("""
	CREATE TABLE super_programs(
	sp_id INT AUTO_INCREMENT NOT NULL,
	sp_name VARCHAR(255) NOT NULL,
	dep_id INT NOT NULL,
	PRIMARY KEY (sp_id),
	FOREIGN KEY (dep_id) REFERENCES departments (dep_id)
);""")

create_slo_db.append("""
	CREATE TABLE programs(
	prog_id INT AUTO_INCREMENT NOT NULL,
	prog_name VARCHAR(255) NOT NULL,
	prog_desc TEXT,
	deg_id INT NOT NULL,
	sp_id INT NOT NULL,
	PRIMARY KEY (prog_id),
	FOREIGN KEY (deg_id) REFERENCES degrees (deg_id),
	FOREIGN KEY (sp_id) REFERENCES super_programs (sp_id)
);""")
create_slo_db.append("""
	CREATE UNIQUE INDEX unique_program_degree
ON programs(prog_name(255), deg_id);""")

create_slo_db.append("""
	CREATE TABLE poutcomes(
	pout_id INT AUTO_INCREMENT NOT NULL,
	pout_desc TEXT NOT NULL,
	prog_id INT NOT NULL,
	PRIMARY KEY (pout_id),
	FOREIGN KEY (prog_id) REFERENCES programs (prog_id)
);""")
create_slo_db.append("""
	CREATE UNIQUE INDEX unique_poutcome
ON poutcomes(pout_desc(255), prog_id);""")

create_slo_db.append("""
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
);""")

create_slo_db.append("""
	CREATE TABLE plo_assessments(
	pout_id INT NOT NULL,
	discussion_id INT NOT NULL,
	plo_assess_date DATE NOT NULL,
	PRIMARY KEY (pout_id, discussion_id),
	FOREIGN KEY (pout_id) REFERENCES poutcomes (pout_id),
	FOREIGN KEY (discussion_id) REFERENCES discussions (discussion_id)
);""")

if __name__ == '__main__':
	with open('slo_db.sql', 'w', encoding="utf-8") as f:
		for statement in create_slo_db:
			f.write(statement+"\n")
		f.close()
