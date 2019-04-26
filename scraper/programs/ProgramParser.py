#! /usr/bin/env python3
from bs4 import BeautifulSoup
import urllib.request

class ProgramParser():
    """ Fetch the program page and parse out the program names and
        types.
    """
    def __init__(self, url):
        """ Fetch the program page from @url and create the html parser
            object.
            @url: The full url of the program page.
        """
        self.page = urllib.request.urlopen(url)
        self.parser = BeautifulSoup(self.page, "html.parser")

    def processRow(self, row):
        """ Parse the program name and program type from the row.
            @row: A BeautifulSoup bs4.element.Tag object containing
                  a row from the tables on the academic program page.
            @return: A tuple containing the program and type EX.
                     (b'Art History', b'AA-T')
        """
        # program title is second field
        pTitle = row.contents[1].get_text()
        #pTitle = pTitle.encode('ascii')
        # program type is third field

        pType = row.contents[2].get_text()
        #pType = pType.encode('ascii')

        return (pTitle, pType)

    def parseToList(self):
        """ Extract the program names and program types from the
            academic program page.
            @return: A list of tuples containing the program and type EX.
                     [(b'Program Name', b'TYPE'),(b'Art History', b'AA-T')]
        """
        tables = self.parser.find_all("table")
        # grab the second table from the page
        programTable = tables[1]

        programRows = programTable.find_all('tr')
        # skip the first row
        programList = []
        for i in range(1, len(programRows)):
            programList.append(self.processRow(programRows[i]))

        return programList
