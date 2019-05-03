#! /usr/bin/env python3
DEBUG = False

#install pips
from os import system, name
system('pip install -r requirements.txt')
print("************PIPS INSTALLED**********")
# Add subdirectories

import sys
sys.path.append("./courses")
sys.path.append("./programs")

#from bs4 import BeautifulSoup
#import glob, os
#import mysql.connector
#from mysql.connector import errorcode
#import slate
#import ProgramParser as P
from PLOScraper import PLOScraper
from PLODB import PLODB

programsUrl = "http://www.butte.edu/academicprograms/"

#def writeProgramsToFile(programs, file):
#    f = open(file, 'w')
#    for program in programs:
#        f.write('{},{}\n'.format(*program))
#    f.close()

def main():
	#progParser = P.ProgramParser(programsUrl)
	#programs = progParser.parseToList()
	#writeProgramsToFile(programs, "programs.csv")

	#answer = raw_input("Download course outlines (y/n)? ")
	#if answer[0] == "y" or answer[0] == "Y":
	#	subjectList = createSubjectList(getPage(allSubjectsUrl))
	#	for subject in subjectList.find_all("option"):
	#		processSubject(subject['value'])
	#courses = processCoursePDFs()
	#writeCoursesToFile(courses, 'courses.csv')
	#writeCourseOutcomesToFile(courses, 'course_outcomes.csv')

	scraper = PLOScraper(); Socket = PLODB()
	scrapedPrograms = scraper.getPrograms()
	for prog in scrapedPrograms:
		[Socket.insert(plo) for plo in scraper.getPLOs(prog)]

if __name__ == "__main__":
	main()
