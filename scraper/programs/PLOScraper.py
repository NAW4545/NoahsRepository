#! /usr/bin/env  -S python3 -B -OO -q
import urllib.request
import re
import grequests
import json
from bs4 import BeautifulSoup

titleCode = {
    "AA": "AA Degree",
    "AS": "AS Degree",
    "AA-T": "AA-T Degree",
    "AS-T": "AS-T Degree",
    "CERT": "Certificate",
    "CA": "Certificate of Achievement",
    "Noncredit Certificate": "Noncredit Certificate",
}

class PLOScraper():
    """ Scrape PLO and program data from the butte college website.

        PLO Data is spread accross separate pages, so an internal dictionary is
        used to collect data as it's scraped.

        self.all_plo_dict stores a dictionary using the program pids as keys,
        with each pid key storing a list of dictionaries, one dictionary for each degree
        within the program.

        self.parsePrograms() will create the dictionary structure
        and populate the names, degree types, and departments from the catalog page
        at allProgramsUrl.

        self.parsePrograms()->
        self.all_plo_dict = {
           'pid': [
                       {'program': 'name', 'deg_type': 'code', 'department': 'dep'},
                       {'program': 'Graphic Design for Print', 'deg_type': 'AS', 'department': 'Digital Arts and Design'}
                   ],
           '737': etc..
        }

        self.getPLOs() will then populate the remaining data from the individual program page
        based on pid.

        self.getPLOs('716')->
        self.all_plo_dict = {
           '716': [
                       {
                           'pid': pid,
                           'super_program': listed under 'Program Details' (Multimedia Studies Program, Computer Science),
                           'program': program (ex. Wallpaper Design),
                           'plos': a list of PLOs (['plo 1', 'plo 2']),
                           'department': department name (Business Education, Digital Arts and Design),
                           'description': program description,
                           'chair': department chair,
                           'deg_type': degree code (AA, AS-T, CERT),
                           'courses': a list of dictionaries containting course names and codes
                                      [{'cour_code': 'CSCI 20', 'cour_name': 'Programming and Algorithms I'}]
                       },
                       {'program': 'program name2', 'deg_type': 'AS', 'department': 'dep'},
                       etc..
                   ]
        }

        Initializing with fetchPrograms=True (the default) will fetch the programs on
        initialization. Then the pids can be obtained through getPrograms() to fetch the remaining data
        for each pid separately using getPLOs().

        scraper = PLOScraper()
        pids = scraper.getPrograms()
        plo_list = scraper.getPLOs(pids[0])

        or all PLOs can be fetched at once using getAllPLOs()

        scraper = PLOScraper()
        all_plo_list = scraper.getAllPLOs()
    """

    def __init__(self,
                 fetchPrograms=True,
                 cachePages=False,
                 allProgramsUrl="http://www.butte.edu/academicprograms/",
                 programUrl="http://www.butte.edu/academicprograms/program_details.php?year=8&program_id="):
        """
            @fetchPrograms: When set to true, populate self.all_plo_dict with data from
                allProgramsUrl on initialization.

            @cachePages: When set to true, create a file containing a json object to store
                         the html retrieved from each page. (Currently the only use is to create
                         a local cache for testing. Another possile use is to check for changes to any page
                         on the website since it was last accessed.)
                         {
                             'allProgramPage': 'html from the main catalog page',
                             "programPages": {
                                 'pid': 'html from the page',
                                 'pid2': 'html from the page 2',
                             }
                         }

            @allProgramsUrl: The url of the catalog listing page containing all the programs

            @programUrl: The url and partial query string used to access invidual program pages
                In the current URL structure each program's unique ID is set as program_id
                in the query string ex.
                http://www.butte.edu/academicprograms/program_details.php?year=8&program_id=[PID]
                This url will return the page containing all the programs listed in the
                department associated with the PID.
                ex.
                Computer science's id 714 so
                http://www.butte.edu/academicprograms/program_details.php?year=8&program_id=714
                is the page listing all programs in this department.
        """

        self.allProgramsUrl = allProgramsUrl
        self.programUrl = programUrl
        self.all_plo_dict = {}

        self.cachePages = cachePages
        if self.cachePages is True:
            self.pageCache = { 'allProgramPage': '',
                                'programPages': {}
                             }

        if fetchPrograms == True:
            self.parsePrograms()

    def __del__(self):
        # write any cached pages to a json file
        if self.cachePages is True:
            with open('pageCache.json', 'w', encoding='utf-8') as outfile:
                json.dump(self.pageCache, outfile)

    def getPage(self, url):
        return urllib.request.urlopen(url).read()

    def getPrograms(self):
        """ Return the program ids from the page located at self.allProgramsUrl
            self.all_plo_dict must be populated by using self.parsePrograms()

            @return: A list of strings representing the PIDs scraped from the page.
                ['PID1', '737', '716', '699']
        """
        # return a list of the dictionary keys
        return list(self.all_plo_dict)

    def getProgramNames(self):
        """ Return the program names from the page located at self.allProgramsUrl.
            self.all_plo_dict must be populated by using self.parsePrograms()

            @return: A list of program names.
                ['EMT - Paramedic',
                 'Emergency Medical Responder (EMR)',
                 'Law Enforcement Academy - Basic/Fish and Wildlife Emphasis'
                 etc...]
        """
        pgm_names = []
        for pid, pgm_list in self.all_plo_dict.items():
            for pgm in pgm_list:
                pgm_names.append(pgm['program'])
        return pgm_names

    def getPLOs(self, pid):
        """ Get the PLOs from an individual program page.
            @pid: The pid of the page to retrieve data from.
            @return: A list of dictionaries containing the data for each program on the page.
                The format of the dictionary should be the same as that accepted
                by PLODB.insert()
                [{
                    'pid': pid,
                    'super_program': listed under 'Program Details' (Multimedia Studies Program, Computer Science),
                    'program': program (ex. Wallpaper Design),
                    'plos': a list of PLOs (['plo 1', 'plo 2']),
                    'department': department name (Business Education, Digital Arts and Design),
                    'description': program description,
                    'chair': department chair,
                    'deg_type': degree code (AA, AS-T, CERT),
                    'courses': a list of dictionaries containting course names and codes within the degree program
                               [{'cour_code': 'CSCI 20', 'cour_name': 'Programming and Algorithms I'}]
                }]
        """
        page = self.getPage("{}{}".format(self.programUrl, pid))

        self.parseProgramPage(pid, page)

        return self.all_plo_dict[pid]

    def getAllPLOs(self):
        """ Fetch all program pages asyncronously using grequests and parse all
            program data from them to populate self.all_plo_dict
            @return: A list of all PLO data
        """

        # def showProgress(response, *args, **kwargs):
        #     print(response.url)

        # sort the list of pids
        # sorted pids ['699', '700', '701']
        pids = sorted(self.all_plo_dict.keys())

        # ensure the session is closed
        with grequests.Session() as sess:
            # create a list of url requests in the order of the sorted pids
            # sorted requests ['url?program_id=699', 'url?program_id=700', 'url?program_id=701']
            # create a list of requests to send asyncronously
            # the hook will print the url when a response is received
            request_list = [grequests.get(self.programUrl+pid,
                                          hooks={'response': lambda r, *args, **kw: print(r.url)},
                                          session=sess)
                            for pid in pids]
            # grequests.map will return responses in the same order as requests
            response_list = grequests.map(request_list)

        # scrape data from all responses
        for i in range(0, len(pids)):
            self.parseProgramPage(pids[i], response_list[i].content)

        return self.getPLOList()

    def parseProgramPage(self, pid, page):
        """ Parse the PLOS from an individual program page. The data is populated
            into self.all_plo_dict.
            @pid: The pid of the page.
            @page: The HTML of the page at program_id=@pid
        """
        if self.cachePages == True:
            self.pageCache['programPages'][pid] = page.decode('utf-8')

        page = BeautifulSoup(page, "html.parser")
        # get the chair from the page
        # chair is in a td formatted as <td>firstname lastname, Chair (123) 456-7890</td>
        chairTd = page.find('td', string=re.compile(r'(.*?), Chair \(\d{3}\) \d{3}-'))
        chair = ''
        if chairTd != None:
            chair = chairTd.text.strip()

        # get the super program name listed under Program Details for the page
        pname = ''
        pnameSection = page.find('h2', 'catalogDetails').parent.parent.next_sibling.find('td')
        if pnameSection != None:
            pname = pnameSection.string

        for plo_dict in self.all_plo_dict[pid]:

            # insert the values into the dictionary
            plo_dict['super_program'] = pname
            plo_dict['chair'] = chair
            plo_dict['pid'] = pid
            # set initial values for description and plos
            plo_dict['description'] = ''
            plo_dict['plos'] = []
            plo_dict['courses'] = []

            # set the regex pattern to match the heading contents
            # --
            # On the catalog listing page most programs are listed without a degree prefix
            # such as 'AA degree in', but Noncredit certificates are always
            # listed with the prefix 'Noncredit certificate of', so a different
            # pattern is needed to match the headings.
            # --

            if plo_dict['program'].startswith('Noncredit Certificate'):
                headingSearch = re.escape(plo_dict['program'])
            else:
                headingSearch = f"{titleCode[plo_dict['deg_type']]} in {re.escape(plo_dict['program'])}"

            # print(headingSearch)

            # all certs, ca, noncred are in tds styled with font-size:20px, all other
            # degrees use font-size:16px
            # look for degree headings with contents matching the headingSearch
            heading = page.find(
                'td',
                string=re.compile(headingSearch),
                attrs={'style': 'font-size:16px;font-weight:bold;'})
            # print("heading 16", heading)

            # look for cert headings with contents matching the headingSearch
            # if no degrees were found
            if heading == None:
                heading = page.find(
                    'td',
                    string=re.compile(headingSearch),
                    attrs={'style': 'font-size:20px;font-weight:bold;'})
                # print("heading 20", heading)

            if heading is not None:
                ploTable = heading.parent.parent.parent.parent

                for nextRow in ploTable.find_next_siblings('tr'):

                    # look for the description
                    descSearchGroup = nextRow.find('td', string=re.compile(r'About the Program'))
                    # print('descSearchGroup ', descSearchGroup)

                    if descSearchGroup != None:
                        descTd = descSearchGroup.parent.next_sibling.find('td')
                        desc = descTd.text.strip()
                        plo_dict['description'] = desc

                    # look for the slos
                    searchGroup = nextRow.find('td', string=re.compile(r'Student Learning Outcomes'))
                    # print('searchGroup ', searchGroup)
                    if searchGroup != None:
                        ploList = searchGroup.parent.next_sibling.next_sibling.find('ul')
                        for plo in ploList.find_all('li'):
                            plo_dict['plos'].append(plo.text.strip())

                    # look for courses in the degree program
                    courseDivs = nextRow.find_all('div', class_="heading")
                    if courseDivs is not None:
                        for courseDiv in courseDivs:
                            cour_code = courseDiv.find('td', attrs={'width': '15%'}).find('a').get_text().strip()
                            cour_code = cour_code[3:] if cour_code.startswith('or ') else cour_code
                            cour_name = courseDiv.find('td', attrs={'width': '50%'}).find('a').get_text().strip()
                            course = {'cour_code': cour_code, 'cour_name': cour_name}
                            plo_dict['courses'].append(course)

                    # stop when the 2px horizontal ref separator is found
                    hRef = nextRow.find('hr')
                    if hRef is not None:
                        # print(hRef, hRef.attrs)
                        s = re.search('height:2px', hRef.attrs['style'])
                        # print(s)
                        if s is not None:
                            break


    def getPLOList(self):
        """ Return a list of all programs in self.all_plo_dict
            @return: A list containing all current program data
                [{
                    'pid': pid,
                    'super_program': listed under 'Program Details' (Multimedia Studies Program, Computer Science),
                    'program': program (ex. Wallpaper Design),
                    'plos': a list of PLOs (['plo 1', 'plo 2']),
                    'courses': a list of course dictionaries ([{'cour_code': 'code', cour_name: 'name'}])
                    'department': department name (Business Education, Digital Arts and Design),
                    'description': program description,
                    'chair': department chair,
                    'deg_type': degree code (AA, AS-T, CERT)
                }]
        """
        pgms = []
        for pid, pgm_list in self.all_plo_dict.items():
            pgms += pgm_list
        return pgms

    def parsePrograms(self):
        """ Parse the pids program names, program types, and departments from the
            academic program page (self.allProgramsUrl) populate the data into self.all_plo_dict.

            Each pid key corresponds to a list of dictionaries containing the scraped program data.
            This dictionary is then populated with the remaining data by getPLOs().

            @return: self.all_plo_dict
                 {
                    'pid': [
                                {'program': 'name', 'deg_type': 'code', 'department': 'dep'},
                                {'program': 'Graphic Design for Print', 'deg_type': 'AS', 'department': 'Digital Arts and Design'}
                            ],
                    '737': etc..
                 }
        """
        page = self.getPage(self.allProgramsUrl)

        if self.cachePages is True:
            self.pageCache['allProgramPage'] = page.decode('utf-8')

        page = BeautifulSoup(page, "html.parser")
        tables = page.find_all("table")
        # grab the second table from the page
        programTable = tables[1]

        programRows = programTable.find_all('tr')
        # skip the first row

        for i in range(1, len(programRows)):
            self.processProgramRow(programRows[i])

        return self.all_plo_dict

    def processProgramRow(self, row):
        """ Create a key for new PIDs in self.all_plo_dict and populate it with
            initial PLO data.
            @row: A BeautifulSoup bs4.element.Tag object containing
                  a row from the table on the academic program page.
        """
        # get the pid from the link in the second cell
        if row.contents[1].find("a"):
            link = row.contents[1].find("a")
            pidata = link['href'].split('=')
            if (len(pidata) == 3):
                pid = pidata[2]
                # index 2 is program id number

        # program title is second field
        pTitle = row.contents[1].get_text()
        #pTitle = pTitle.encode('ascii')
        # program type is third field

        pType = row.contents[2].get_text()
        #pType = pType.encode('ascii')

        # department is fourth field
        department = row.contents[3].get_text()

        pData = {
            'program': pTitle,
            'deg_type': pType,
            'department': department,
        }
        # if the pid is in the dictionary add data from the new row to the list
        # else assign a new list
        if pid in self.all_plo_dict:
            self.all_plo_dict[pid].append(pData)
        else:
            self.all_plo_dict[pid] = [pData]

def main():
    import pprint
    pp = pprint.PrettyPrinter(indent=2)


    scraper = PLOScraper()
    # pp.pprint(scraper.getPLOs('714'))


    with open('pageCache.json', 'r', encoding='utf-8') as f:
        pages = json.load(f)
    page = BeautifulSoup(pages['programPages']['714'], "html.parser")
    heading = page.find(
        'td',
        string=re.compile("Certificate in Microsoft Server Administration"),
        attrs={'style': 'font-size:20px;font-weight:bold;'})
    # print(heading)

    # t = heading.parent.parent.parent.parent
    # # print(t)
    #
    # courseList = []
    # for nextRow in t.find_next_siblings('tr'):
    #     courseDivs = nextRow.find_all('div', class_="heading")
    #     if courseDivs is not []:
    #         for courseDiv in courseDivs:
    #             # print(nextRow)
    #             cour_code = courseDiv.find('td', attrs={'width': '15%'}).find('a').get_text().strip()
    #             # remove 'or ' from alternate courses
    #             cour_name = courseDiv.find('td', attrs={'width': '50%'}).find('a').get_text().strip()
    #             course = {'cour_code': cour_code, 'cour_name': cour_name}
    #             print(course)
    #             courseList.append(course)
    #
    #     # stop when the horizontal ref separator is found.
    #     # there is no separator after the last tr in the table, currently this is not an issue.
    #     hRef = nextRow.find('hr')
    #     if hRef is not None:
    #         # print(hRef, hRef.attrs)
    #         s = re.search('height:2px', hRef.attrs['style'])
    #         # print("href match ", s)
    #         if s is not None:
    #             break


    # pp.pprint(courseList)


    # tables = page.find("table", attrs={'bordercolor': 'red'})
    # print(tables)
    # trs = tables.find('td', attrs={'width': '15%'})
    # get table border red
    # get sibling div heading



if __name__ == '__main__':
    main()
