#! /usr/bin/env python3
from bs4 import BeautifulSoup
import glob, os, sys
from subprocess import call
import urllib.request
import re
from fpdf import FPDF

allProgramsUrl = "http://www.butte.edu/academicprograms/"
programUrl = "http://www.butte.edu/academicprograms/program_details.php?year=8&program_id="
filters = [
	'ANTH', 'ART', 'AUTO', 'BCIS', 'CDF', 'CMST', 'DRAM', 'EH', 'ENGL', 'FN', 'GEOG',
	'HIST', 'KIN', 'MATH', 'NSG', 'OLS', 'PHIL', 'PHO', 'PSY', 'RTVF', 'SOC', 'SPAN'
]

def getPage(url):
	page = urllib.request.urlopen(url).read()
	print("getting page " + url)
	return BeautifulSoup(page, "html.parser")

def getPrograms(programsPage):
	""" Parse the program ids from the programs page. In the current URL structure
		the pid is set as program_id in the query string ex.
		http://www.butte.edu/academicprograms/program_details.php?year=8&program_id=[PID]
		This url will return the page containing all the programs listed in the
		department associated with the PID.

		ex.

		Computer science's id 714 so
		http://www.butte.edu/academicprograms/program_details.php?year=8&program_id=714
		is the page listing all programs in this department.

		@programsPage: The HTML Parser object created from the programs page
			like that returned from getPage().
		@return: A list of strings representing the PIDs scraped from the page.
			['PID1', '737', '716', '699']
	"""
	programs = []
	rows = programsPage.find_all("td")
	for row in rows:
		if row.find("a"):
			link = row.find("a")
			pname = link.string
			pdata = link['href'].split('=')
			if (len(pdata) == 3):
				pid = pdata[2]
				# index 2 is program id number
				programs.append(pid) if pid not in programs else None

	print("retrieved programs:")
	print(programs)
	return programs

def getPLOs(pid):
	""" Parse the PLOS from an individual program page.
		@pid: A string containing the program_id of the page to fetch.
		@return: A tuple of the program name eg. Drafting or Computer Science
			and a dictionary where the keys are programs and the values
			are a list of the outcomes for the program.
			(
				'Program Name',
				{'degree name': ['plo 1', 'plo 2'], 'degree name': ['plo 1', 'plo 2']}
			)

			ex.

			http://www.butte.edu/academicprograms/program_details.php?year=8&program_id=716
			is the program page for drafting so
			getPLOs(716) ->
				(
					'Drafting',
					{   'AS Degree in Drafting and CAD Technology':
						[
							'Describe the role of technical graphics in the engineering design process.',
							'Produce dimensioned technical drawings using various techniques including computer-aided drafting (CAD), 3D modeling, and freehand sketching.',
							'etc...'
						],
					   'Certificate of Achievement in Drafting and CAD Technology':
						[
							'Describe the role of technical graphics in the engineering design process and in the architectural design process.',
							'etc...'
						]
					}
				)
	"""
	plos = {}
	page = urllib.request.urlopen("{}{}".format(programUrl, pid)).read()
	page = BeautifulSoup(page, "html.parser")

	# get the program name
	pname = ''
	pnameSection = page.find('h2', 'catalogDetails').parent.parent.next_sibling.find('td')
	if pnameSection != None:
		pname = pnameSection.string

	print("created bs4 object " + pname)
	# get the list of degree programs on this page
	# look for all lines starting with a degree type and add those lines to a list
	programs = [d.text.strip() for d in page.find_all('td', string=re.compile('^AS Degree'))]
	programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^AS-T Degree'))]
	programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^AA Degree'))]
	programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^AA-T Degree'))]
	programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^Certificate'))]
	programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^Noncredit Certificate'))]
	programs = set(programs)
	# get the plos for each program
	print("programs:")
	print(programs)

	for pgm in programs:
		print("Processing {}".format(pgm))
		try:
			ploTable = page.find(
				'td',
				string=re.compile(pgm),
				attrs={'style': 'font-size:16px;font-weight:bold;'}).parent.parent.parent.parent

			for nextRow in ploTable.find_next_siblings('tr'):
				searchGroup = nextRow.find('td', string=re.compile('Student Learning Outcomes'))
				if searchGroup != None:
					ploList = searchGroup.parent.next_sibling.next_sibling.find('ul')
					pgmPLOs = []
					for plo in ploList.find_all('li'):
						pgmPLOs.append(plo.text.strip())
					plos[pgm] = pgmPLOs
					# stop on the first one
					break
		except:

			try:
				ploTable = page.find(
					'td',
					string=re.compile(pgm),
					attrs={'style': 'font-size:20px;font-weight:bold;'}).parent.parent.parent.parent

				for nextRow in ploTable.find_next_siblings('tr'):
					searchGroup = nextRow.find('td', string=re.compile('Student Learning Outcomes'))
					if searchGroup != None:
						ploList = searchGroup.parent.next_sibling.next_sibling.find('ul')
						pgmPLOs = []
						for plo in ploList.find_all('li'):
							pgmPLOs.append(plo.text.strip())
						plos[pgm] = pgmPLOs
						# stop on the first one
						break

			except:
				None

	return pname, plos

def found(name, list):
	for n in list:
		if re.search(n, name, re.IGNORECASE):
			return True
	return False

def makePDF(allPLOs, filter=False, filterBy=None):
	pdf = FPDF()
	for groupName, groupPLOs in sorted(allPLOs.items()):
		if not filter or found(groupName, filterBy):
			pdf.add_page()

			pdf.set_font('Arial', 'B', 20)
			pdf.set_fill_color(211, 211, 211)
			pdf.multi_cell(0, 12, groupName, 0, 'C', True)
			pdf.set_fill_color(255, 255, 255)
			pdf.cell(0, 8, '', 0, 1)

			for pname, ploList in groupPLOs.items():

				# 16 is height of program heading
				# multiply each PLO item by 3 (guess 2 lines per PLO printed) * 8mm
				#   per line + 4mm for empty space beneath each one
				next_section_height = 16 + (len(ploList) * 2 * 8) + 4
				space_left = 280 - pdf.get_y() - 2
				if next_section_height >= space_left:
					pdf.add_page()

				pdf.set_font('Arial', 'B', 16)
				pdf.multi_cell(0, 10, pname, 'TB', 'L')
				pdf.set_font('Arial', '', 12)
				pdf.cell(0, 6, '', 0, 1)
				num = 1
				for plo in ploList:
					pdf.multi_cell(0, 8, "{}. {}".format(num, plo), 0, 1)
					pdf.cell(0, 4, '', 0, 1)
					num += 1

	pdf.output('Butte-PLOs.pdf', 'F')

	#pdfstream = pdf.output(dest='S').encode('latin-1')
	#pdffile = open('Butte-PLOs.pdf', 'wb')
	#pdffile.write(pdfstream)
	#pdffile.flush()
	#pdffile.close()

def main():
	pids = getPrograms(getPage(allProgramsUrl))
	print(pids)
	programs = getPLOs(pids[0])
	print(programs)


	# makePDF(allPLOs, True, filters)

if __name__ == "__main__":
	main()
