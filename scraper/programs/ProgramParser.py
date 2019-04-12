#! /usr/bin/env python3
from bs4 import BeautifulSoup
import urllib2

class ProgramParser():
    def __init__(self, url):
        self.page = urllib2.urlopen(url)
        self.parser = BeautifulSoup(self.page, "html.parser")

    def processRow(self, row):
        # program title is second field
        pTitle = row.contents[1].get_text()
        pTitle = pTitle.encode('ascii')
        # program type is third field

        pType = row.contents[2].get_text()
        pType = pType.encode('ascii')

        return (pTitle, pType)

    def parseToList(self):
        tables = self.parser.find_all("table")
        # grab the second table from the page
        programTable = tables[1]

        programRows = programTable.find_all('tr')
        # skip the first row
        programList = []
        for i in range(1, len(programRows)):
            programList.append(self.processRow(programRows[i]))

        return programList
