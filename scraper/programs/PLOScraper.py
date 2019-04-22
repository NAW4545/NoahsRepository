#! /usr/bin/env python3
import urllib.request
import re
from bs4 import BeautifulSoup

class PLOScraper():
    """Scrape PLO and program data from the butte college website"""

    def __init__(self,
                 allProgramsUrl="http://www.butte.edu/academicprograms/",
                 programUrl="http://www.butte.edu/academicprograms/program_details.php?year=8&program_id="):

        self.allProgramsUrl = allProgramsUrl
        self.programUrl = programUrl

    def getPage(self):
        "Return a BeautifulSoup Parser object created from the url."
        page = urllib.request.urlopen(self.allProgramsUrl).read()
        print("getting page " + self.allProgramsUrl)
        return BeautifulSoup(page, "html.parser")

    def getPrograms(self):
        """ Parse the program ids from the page located at self.allProgramsUrl 

            In the current URL structure
            the pid is set as program_id in the query string ex.
            http://www.butte.edu/academicprograms/program_details.php?year=8&program_id=[PID]
            This url will return the page containing all the programs listed in the
            department associated with the PID.

            ex.

            Computer science's id 714 so
            http://www.butte.edu/academicprograms/program_details.php?year=8&program_id=714
            is the page listing all programs in this department.

            @return: A list of strings representing the PIDs scraped from the page.
                ['PID1', '737', '716', '699']
        """
        programsPage = self.getPage()
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
        return programs

    def getPLOs(self, pid):
        """ Parse the PLOS from an individual program page.
            @pid: A string containing the program_id of the page to fetch.
            @return: A list of dictionaries containing the data for each program.
                The format of the dictionary should be the same as that accepted
                by PLODB.insert()
                [{
                    'pid': pid,
                    'program': program (ex. AA Degree in Wallpaper Design),
                    'plos': a list of PLOs (['plo 1', 'plo 2']),
                    'department': department name (Computer Science, Fasion),
                    'description': program description,
                    'chair': department chair,
                    'deg_type': degree code (AA, AS-T, CERT)
                }]
        """
        plos = {}
        page = urllib.request.urlopen("{}{}".format(self.programUrl, pid)).read()
        page = BeautifulSoup(page, "html.parser")

        # get the program name
        pname = ''
        pnameSection = page.find('h2', 'catalogDetails').parent.parent.next_sibling.find('td')
        if pnameSection != None:
            pname = pnameSection.string

        # chair is in a td formatted as <td>firstname lastname, Chair (123) 456-7890</td>
        chairTd = page.find('td', string=re.compile('(.*?), Chair \(\d{3}\) \d{3}-'))
        if chairTd != None:
            chair = chairTd.text.strip()
        else:
            chair = ''

        print("created bs4 object " + pname)
        # get the list of degree programs on this page
        # look for all lines starting with a degree type and add those lines to a list
        programs = [d.text.strip() for d in page.find_all('td', string=re.compile('^AS Degree'))]
        programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^AS-T Degree'))]
        programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^AA Degree'))]
        programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^AA-T Degree'))]
        programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^Certificate'))]
        programs += [d.text.strip() for d in page.find_all('td', string=re.compile('^Noncredit Certificate'))]

        # remove duplicate items
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

                    descSearchGroup = nextRow.find('td', string=re.compile('About the Program'))
                    if descSearchGroup != None:
                        descTd = descSearchGroup.parent.next_sibling.find('td')
                        desc = descTd.text.strip()

                    if searchGroup != None:
                        ploList = searchGroup.parent.next_sibling.next_sibling.find('ul')
                        pgmPLOs = []
                        for plo in ploList.find_all('li'):
                            pgmPLOs.append(plo.text.strip())
                            plos[pgm] = {'description': desc, 'plo_list': pgmPLOs}
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

                        descSearchGroup = nextRow.find('td', string=re.compile('About the Program'))
                        if descSearchGroup != None:
                            descTd = descSearchGroup.parent.next_sibling.find('td')
                            desc = descTd.text.strip()

                        if searchGroup != None:
                            ploList = searchGroup.parent.next_sibling.next_sibling.find('ul')
                            pgmPLOs = []
                            for plo in ploList.find_all('li'):
                                pgmPLOs.append(plo.text.strip())
                                plos[pgm] = {'description': desc, 'plo_list': pgmPLOs}
                            # stop on the first one
                            break

                except:
                    None

        # create a list containing a dictionary for each plo's data
        plo_data = []
        for program, program_data in plos.items():
            plo_data.append({
                    'pid': pid,
                    'program': program,
                    'plos': program_data['plo_list'],
                    'department': pname,
                    'description': program_data['description'],
                    'chair': chair,
                    'deg_type': self.findDegType(program)
            })
        return plo_data

    def findDegType(self, program_name):
        """ Determine the type of degree based on the program name.
            @program_name: A name of an academic program such as Certificate in *** or AS Degree in ***
            @return: The abbreviated degree type
        """

        if program_name.find('AA Degree in') >= 0:
            deg_type = 'AA'
        elif program_name.find('AA-T Degree') >= 0:
            deg_type = 'AA-T'
        elif program_name.find('AS-T Degree in') >= 0:
            deg_type = 'AS-T'
        elif program_name.find('AS Degree in') >= 0:
            deg_type = 'AS'
        elif program_name.find('Certificate of Achievement in') >= 0:
            deg_type = 'CA'
        elif program_name.find('Noncredit Certificate in') >= 0:
            deg_type = 'Noncredit Certificate'
        elif program_name.find('Certificate in') >= 0:
            deg_type = 'CERT'
        else:
            deg_type = None

        return deg_type

def main():
    s = PLOScraper()
    print(s.getPLOs('716'))

if __name__ == '__main__':
    main()
