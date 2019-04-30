queries = []
# Use Case #1: Access - Public report
# 	Show most recently assessed outcomes associated with a specified program.

queries.append("""
select prog_name, plo_assess_date, pout_desc from plo_assessments
right join poutcomes on plo_assessments.pout_id=poutcomes.pout_id
join programs on poutcomes.prog_id=programs.prog_id
where prog_name=%s
order by plo_assess_date;
""")

# Use Case #2: Access - Teacher report
# 	Show all outcomes associated with one or more programs regardless of when they were assessed.
# 	Entries should be grouped by the program and ordered by the assessment date in descending order.

queries.append("""
select pout_desc, prog_name from programs
left join poutcomes on poutcomes.prog_id=programs.prog_id
left join plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
where (programs.prog_id=0 or programs.prog_id=1)
group by programs.prog_id
order by plo_assessments.plo_assess_date desc;
""")

# Use Case #3: Access - Chair report
# 	Show all outcomes associated with one or more programs regardless of when they were assessed.
# 	Entries should be grouped by the program and ordered by the assessment date in descending order.

queries.append("""
select pout_desc, prog_name from programs
left join poutcomes on poutcomes.prog_id=programs.prog_id
left join plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
where (programs.prog_id=0 or programs.prog_id=1)
group by programs.prog_id
order by plo_assessments.plo_assess_date desc;
""")

# Use Case #5: Assess - Chair report
# 	Show all programs and outcomes associated with a specified department.
# 	Entries should be grouped by the program and ordered by the assessment date in descending order.

queries.append("""
select programs.prog_id, prog_name, poutcomes.pout_id, dep_name from programs
left join poutcomes on poutcomes.prog_id=programs.prog_id
left join departments on departments.dep_id=programs.dep_id
left join plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
group by programs.prog_id
order by plo_assessments.plo_assess_date desc;
""")

# Use Case #7: Assessment Form Submission
# 	Create an entry in the discussions table with data from the form.
# 	An assessment must be created for each outcome referenced in the form data.


if __name__ == '__main__':
	with open('slo_queries.sql', 'w', encoding="utf-8") as f:
		for statement in create_slo_db:
			f.write(statement+"\n")
		f.close()
