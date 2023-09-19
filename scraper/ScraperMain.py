#! /usr/bin/env -S python3 -B -OO -q
DEBUG = False

#install pips
from os import system
system('pip install -r requirements.txt')
print("************PIPS INSTALLED**********")

# Add subdirectories

import sys
sys.path.append("./courses")
sys.path.append("./programs")

from PLOScraper import PLOScraper
from PLODB import PLODB

programsUrl = "http://www.butte.edu/academicprograms/"

def main():
	scraper = PLOScraper(); Socket = PLODB()
	scrapedPrograms = scraper.getPrograms()
	for prog in scrapedPrograms:
		[Socket.insert(plo) for plo in scraper.getPLOs(prog)]

if __name__ == "__main__":
	main()
