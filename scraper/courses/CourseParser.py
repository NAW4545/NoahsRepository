#! /usr/bin/env python3
from bs4 import BeautifulSoup
import glob, os, sys
from subprocess import call
import slate
from urllib import request

allSubjectsUrl = "http://www.butte.edu/departments/curriculum/course_outlines/"
subjectUrl = "http://www.butte.edu/departments/curriculum/course_outlines/?area="

def getPage(url):
	"Return a BeautifulSoup parser object from the page at @url"
	page = request.urlopen(url).read()
	return BeautifulSoup(page, "html.parser")

def processSubject(subject):
	""" Get the subject url corresponding to @subject
		eg. http://www.butte.edu/departments/curriculum/course_outlines/?area=CHEM
		Then call processCourses() to save PDFs from the page.
		@subject: An abbreviated subject code eg. CHEM, ART
	"""
	print("Processing {}".format(subject))
	courseList = getPage("{}{}".format(subjectUrl, subject))
	processCourses(subject, courseList)

def createSubjectList(soup):
	""" Return the first select element from a page using BeautifulSoup
		@soup: A BeautifulSoup parser object
		@return: The select element
	"""
	# In the page at allSubjectsUrl, the courses dropdown is the first select on the page
	return soup.find("select")

def downloadCORs():
	""" Download the course PDFs for all subjects listed on allSubjectsUrl.
	"""
	subjectList = createSubjectList(getPage(allSubjectsUrl))
	# loop through all option elements in the course dropdown
	# the 'value' of each option is the abbreviated subject code eg. CHEM, ART
	for subject in subjectList.find_all("option"):
		processSubject(subject['value'])

def saveCourse(subject, url):
	""" Save a PDF file from @url to a local file.
		@subject: The subject being saved. Used in the name of the local
			pdf files.
		@url: The url where the course pdf is located.
	"""
	next = 1
	processPage = request.urlopen(url)
	CHUNK = 16 * 1024
	with open("./pdf/{}-{}.pdf".format(subject, next), 'wb') as file:
		while True:
			chunk = processPage.read(CHUNK)
			if not chunk:
				break
			file.write(chunk)

	next += 1

def processCourses(subject, courseList):
	""" Find all td elements on a subject page eg http://www.butte.edu/departments/curriculum/course_outlines/?area=CHEM,
		if the td contains an anchor, assume it is a link to the course pdf, then
		call saveCourse to save the file.
		@subject: An abbreviated subject code eg. CHEM, ART
		@courseList: A BeautifulSoup object created from the subject page
	"""
	rows = courseList.find_all("td")
	for row in rows:
		if row.find("a"):
			saveCourse(subject, row.find("a")['href'])

def splitIdTitle(text, data):
	temp = text.split('-')
	data['id'] = temp[0].strip()
	data['title'] = temp[1].strip()

def processCourseMeta(text, data):
	start = False
	for line in range(len(text)):
		if text[line] == "CATALOG DESCRIPTION":
			start = True
		elif text[line][:12] == "Prerequisite":
			break;
		elif start == True and len(text[line]) > 0:
			splitIdTitle(text[line], data)
			break

def processCoursePDF(courseFile):
	"""

	"""
    courseData = {'id': '', 'title': ''}
	# Open the file for reading in binary mode
    with open(courseFile, 'rb') as pdf:
        pdfDoc = slate.PDF(pdf)
        for page in range(len(pdfDoc)):
            lines = pdfDoc[page].split('\n')
            if page == 0:
                processCourseMeta(lines, courseData)
                print("Processed {}".format(courseData['id']))

    return courseData

def processCoursePDFs():
	""" Call processCoursePDF() for each file in the ./pdf directory.
		@return:
	"""
	allCourses = []
	os.chdir("./pdf")
	for file in glob.glob("*.pdf"):
		allCourses.append(processCoursePDF(file))
	os.chdir("../")

	return allCourses

def convertPDFToText():
	""" Use the command line utility pdftotext to convert saved PDFs into plain
		text.
	"""
	for file in glob.glob("./pdf/*.pdf"):
		outputFile = "./text/{}.txt".format(file[6:-4])
		print("Processing {} -> {}".format(file, outputFile))
		call(["pdftotext", file, outputFile])

def parseObjectives(objectives):
	result = []
	curObj = "A"
	nextObj = "B"
	objectives = objectives.replace('\n', ' ')

	parsed = False
	while not parsed:
		try:
			startIdx = objectives.index(curObj + ".")
			endIdx = objectives.index(nextObj + ".")
			result.append(objectives[startIdx+3:endIdx].strip())
			objectives = objectives[endIdx:]
			curObj = nextObj
			nextObj = chr(ord(nextObj) + 1)
		except ValueError:
			result.append(objectives[3:].strip())
			parsed = True
	return result

def parseCourseId(file):
	f = open(file, 'r')
	contents = f.read()

	idStart = contents.find("I. CATALOG DESCRIPTION")
	idEnd = contents.find("Prerequisite")
	idAndTitle = contents[idStart:idEnd]
	idAndTitle = idAndTitle.replace("I. CATALOG DESCRIPTION", "").split(" - ")
	id = idAndTitle[0]

	f.close()
	return id

def parseCourseObjectives(file):
	f = open(file, 'r')
	contents = f.read()

	objStart = contents.find("II. OBJECTIVES")
	objEnd = contents.find("III. COURSE CONTENT")
	contents = contents[objStart:objEnd]
	objStart = contents.find("A.")
	contents = contents[objStart:]
	objectives = parseObjectives(contents)

	f.close()
	return objectives

def saveObjectives():
	try:
		os.remove('objectives.tab')
	except OSError:
		pass

	for file in glob.glob("./text/*.txt"):
		objectives = parseCourseObjectives(file)
		course = parseCourseId(file).strip()
		print("File {}, id {}".format(file, course))
		writeObjectivesToFile(course, objectives, 'objectives.tab')

def writeObjectivesToFile(course, objectives, file):
	f = open(file, 'a+')
	for obj in objectives:
		f.write("{}\t{}\n".format(course, obj))
	f.close()

def writeCoursesToFile(courses, file):
    f = open(file, 'w')
    for course in courses:
        f.write('{},{}\n'.format(course['id'], course['title']))
    f.close()

def main():
	subjectList = createSubjectList(getPage(allSubjectsUrl))
	print(subjectList)

	# help = False
	# downloadFiles = False
	# convertPDFs = False
	#
	# args = sys.argv
	# for i in range(1, len(args)):
	# 	if args[i].upper()[0:1] == "H":
	# 		help = True
	# 		print("CourseParser.py [d|download] [c|convert] [o|objectives]")
	# 	elif args[i].upper()[0:1] == "D":
	# 		downloadFiles = True
	# 	elif args[i].upper()[0:1] == "C":
	# 		convertPDFs = True
	# 	elif args[i].upper()[0:1] == "O":
	# 		getObjectives = True
	#
	# if not help:
	# 	if downloadFiles == True:
	# 		# download CORs from Butte Curriculum website
	# 		downloadCORs()
	#
	# 	if convertPDFs == True:
	# 		# convert PDFs to text
	# 		convertPDFToText()
	#
	# 	if getObjectives == True:
	# 		saveObjectives()

	courses = processCoursePDFs()
	writeCoursesToFile(courses, 'courses.csv')
	parse text CORs and output all to a text file
	a line of the output file would look like:
	    CSCI 4:Describe the software development life-cycle.
	parseCourse('./course_text/csci.txt')

if __name__ == "__main__":
	main()
