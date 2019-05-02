queries = {}
# Use Case #1: Access - Public report
# 	Show most recently assessed outcomes associated with a specified program.

queries['public_access'] = """
select prog_name, deg_type, plo_assess_date, pout_desc
from plo_assessments
right join poutcomes on plo_assessments.pout_id=poutcomes.pout_id
join programs on poutcomes.prog_id=programs.prog_id
join degrees on degrees.deg_id=programs.deg_id
where prog_name=%s
order by plo_assess_date;
"""

# Use Case #2: Access - Teacher report
# 	Show all outcomes associated with one or more programs regardless of when they were assessed.
# 	Entries should be grouped by the program and ordered by the assessment date in descending order.

queries['teacher_access'] = """
select pout_desc, prog_name from programs
left join poutcomes on poutcomes.prog_id=programs.prog_id
left join plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
where (programs.prog_id=0 or programs.prog_id=1)
group by programs.prog_id
order by plo_assessments.plo_assess_date desc;
"""

# Use Case #3: Access - Chair report
# 	Show all outcomes associated with one or more programs regardless of when they were assessed.
# 	Entries should be grouped by the program and ordered by the assessment date in descending order.

queries['chair_access'] = """
select pout_desc, prog_name from programs
left join poutcomes on poutcomes.prog_id=programs.prog_id
left join plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
where (programs.prog_id=0 or programs.prog_id=1)
group by programs.prog_id
order by plo_assessments.plo_assess_date desc;
"""

# Use Case #5: Assess - Chair report
# 	Show all programs and outcomes associated with a specified department.
# 	Entries should be grouped by the program and ordered by the assessment date in descending order.

queries['chair_assess'] = """
select programs.prog_id, prog_name, poutcomes.pout_id, dep_name from programs
left join poutcomes on poutcomes.prog_id=programs.prog_id
left join departments on departments.dep_id=programs.dep_id
left join plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
group by programs.prog_id
order by plo_assessments.plo_assess_date desc;
"""

# Use Case #7: Assessment Form Submission
# 	Create an entry in the discussions table with data from the form.
# 	An assessment must be created for each outcome referenced in the form data.



# select all program information for a specified program
queries['program_data'] = """
select prog_desc,
	   prog_name,
	   deg_type,
	   sp_name,
	   dep_name
from programs
join degrees on degrees.deg_id=programs.deg_id
join super_programs on super_programs.sp_id=programs.sp_id
join departments on departments.dep_id=super_programs.dep_id
join poutcomes on poutcomes.prog_id=programs.prog_id
WHERE prog_name = %s
"""

# select all outcomes for a specified program
queries['program_outcomes'] = """
select deg_type,
	   prog_name,
	   pout_desc
from programs
join degrees on degrees.deg_id=programs.deg_id
join poutcomes on poutcomes.prog_id=programs.prog_id
WHERE prog_name = %s
"""

# select all program outcomes with no assessments
queries['unnassessed'] = """
select pout_desc,
	   prog_name,
	   deg_type,
	   plo_assess_date Assessed_On
from programs
join poutcomes on poutcomes.prog_id=programs.prog_id
JOIN degrees on degrees.deg_id=programs.deg_id
LEFT JOIN plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
WHERE plo_assess_date IS NULL;
"""

# select all courses in a program
queries['program_courses'] = """
select cour_code,
	   cour_name
from programs
JOIN programs_courses ON programs_courses.prog_id=programs.prog_id
JOIN degrees on degrees.deg_id=programs.deg_id
JOIN courses ON programs_courses.cour_id=courses.cour_id
WHERE prog_name = %s AND deg_type = %s
"""

if __name__ == '__main__':
	with open('slo_queries.sql', 'w', encoding="utf-8") as f:
		for name, statement in queries.items():
			f.write(f"--{name}\n{statement}\n")
		f.close()
