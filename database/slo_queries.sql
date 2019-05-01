
select prog_name, plo_assess_date, pout_desc from plo_assessments
right join poutcomes on plo_assessments.pout_id=poutcomes.pout_id
join programs on poutcomes.prog_id=programs.prog_id
where prog_name=%s
order by plo_assess_date;


select pout_desc, prog_name from programs
left join poutcomes on poutcomes.prog_id=programs.prog_id
left join plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
where (programs.prog_id=0 or programs.prog_id=1)
group by programs.prog_id
order by plo_assessments.plo_assess_date desc;


select pout_desc, prog_name from programs
left join poutcomes on poutcomes.prog_id=programs.prog_id
left join plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
where (programs.prog_id=0 or programs.prog_id=1)
group by programs.prog_id
order by plo_assessments.plo_assess_date desc;


select programs.prog_id, prog_name, poutcomes.pout_id, dep_name from programs
left join poutcomes on poutcomes.prog_id=programs.prog_id
left join departments on departments.dep_id=programs.dep_id
left join plo_assessments on poutcomes.pout_id=plo_assessments.pout_id
group by programs.prog_id
order by plo_assessments.plo_assess_date desc;

