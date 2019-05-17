from flask import Flask, render_template, request, Markup, json
import pymysql
app = Flask(__name__)

@app.route('/')
def report_home():
    # get a list of programs for the form dropdown menu
    connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='slo_db',
                                     cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute("SELECT sp_id, sp_name FROM super_programs")
    super_programs = cursor.fetchall()
    # get a list of degree programs for the form dropdown menu
    cursor.execute(""" SELECT CONCAT(prog_name, ' - ', deg_type) Program
                       FROM programs
                       JOIN degrees on programs.deg_id=degrees.deg_id
                   """)
    # return an object of programs and outcomes
    # {'program name': ['outcome1', 'outcome 2']}
    programs = cursor.fetchall()
    return render_template('index.html', super_programs=super_programs, programs=programs)

@app.route('/program_data')
def get_program_data():
    "Return program outcome as JSON."
    # with no parameters, return a list of super programs
    # with super=program%20name return a list of degrees in the program
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='slo_db',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute(""" SELECT CONCAT(prog_name, ' - ', deg_type) Program, pout_id, pout_desc
                       FROM programs
                       JOIN degrees on programs.deg_id=degrees.deg_id
                       JOIN poutcomes ON poutcomes.prog_id=programs.prog_id
                   """)
    # return an object of programs and outcomes
    # {'program name - degreetype': ['outcome1', 'outcome 2']}
    programs = {}
    for row in cursor.fetchall():
        if row['Program'] not in programs.keys():
            programs[row['Program']] = [(row['pout_id'], row['pout_desc'])]
        else:
            programs[row['Program']].append((row['pout_id'], row['pout_desc']))

    return json.dumps(programs)

@app.route('/submit_report', methods=['POST'])
def report_handler():
    # validate input
    if len(request.form['name']) <= 2:
        msg = f"The name {request.form['name']} is too short"
    else:
        # create the discussion report
        create_report(request.form)
        msg = Markup("""<h1>Thank You</h1><p id="center">Your submission has been received.</p>""")

    return render_template('handler.html', form_result=msg)

def create_report(form_data):
    connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='slo_db',
                                     cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # currently there are no tables for gelos, or slos
    discussion_data = {
        'discussion_completed_by': form_data['name'],
        'discussion_also_present': form_data['present'],
        'discussion_looking_back': form_data['looking_back'],
        'discussion_findings': form_data['findings'],
        'discussion_courses_assessed': form_data['slos'],
        'discussion_gelos_assessed': form_data['gelos'],
        'discussion_strategies': form_data['strategies'],
        'discussion_resources': form_data['resources'],
    }

    # create report + assessments
    discussion_sql = """
        INSERT INTO discussions VALUES(0,
            %(discussion_completed_by)s,
            %(discussion_also_present)s,
            %(discussion_looking_back)s,
            %(discussion_findings)s,
            %(discussion_courses_assessed)s,
            NULL,
            %(discussion_gelos_assessed)s,
            %(discussion_strategies)s,
            %(discussion_resources)s,
            CURDATE()
        )
    """
    cursor.execute(discussion_sql, discussion_data)
    for pout_id in request.form.getlist('outcome'):
        cursor.execute(
        """
            INSERT INTO plo_assessments
            VALUES(%s,
                  (SELECT LAST_INSERT_ID()),
                  CURDATE()
            )
        """, pout_id)
    connection.commit()

@app.route('/discussion_reports')
def get_reports():

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='slo_db',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute(""" SELECT discussion_date,
                              discussion_id,
                              discussion_completed_by,
                              pout_desc,
                              CONCAT(prog_name, ' - ', deg_type) program
                       FROM discussions
                       JOIN plo_assessments USING (discussion_id)
                       JOIN poutcomes USING (pout_id)
                       JOIN programs USING (prog_id)
                       JOIN degrees USING (deg_id)
                       JOIN super_programs USING (sp_id)
                       JOIN departments USING (dep_id)
                   """)

    return render_template("report_years.html", discussions=cursor.fetchall())

@app.route('/view_report', methods=['GET'])
def view_report():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='slo_db',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                                  FROM discussions
                                  WHERE discussion_id=%s
                            """, request.args['id'])
    discussion = cursor.fetchone()
    cursor.execute("""
                       SELECT pout_desc,
                              CONCAT(prog_name, ' - ', deg_type) program,
                              dep_name
                       FROM discussions
                       JOIN plo_assessments USING (discussion_id)
                       JOIN poutcomes USING (pout_id)
                       JOIN programs USING (prog_id)
                       JOIN degrees USING (deg_id)
                       JOIN super_programs USING (sp_id)
                       JOIN departments USING (dep_id)
                       WHERE discussion_id=%s
                    """, request.args['id'])
    outcomes = cursor.fetchall()
    return render_template("view_report.html", discussion=discussion, outcomes=outcomes)

if __name__ == '__main__':
    app.run()
