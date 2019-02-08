from bs4 import BeautifulSoup
import glob, os
import mysql.connector
from mysql.connector import errorcode
import slate
import urllib2

import ProgramParser as P

DEBUG = False

programsUrl = "http://www.butte.edu/academicprograms/"

def writeProgramsToFile(programs, file):
    f = open(file, 'w')
    for course in courses:
        f.write('{},{}\n'.format(*course))
    f.close()

def main():

    #progParser = P.ProgramParser(programsUrl)
    #programs = progParser.parseToList()
    #print(programs)
    #writeProgramsToFile(programs, "programs.csv")

	#answer = raw_input("Download course outlines (y/n)? ")
	#if answer[0] == "y" or answer[0] == "Y":
	#	subjectList = createSubjectList(getPage(allSubjectsUrl))
	#	for subject in subjectList.find_all("option"):
	#		processSubject(subject['value'])
	#courses = processCoursePDFs()
	#writeCoursesToFile(courses, 'courses.csv')
	#writeCourseOutcomesToFile(courses, 'course_outcomes.csv')

	#connectDB()
	#closeDB()

if __name__ == "__main__":
	main()
