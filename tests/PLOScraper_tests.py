# -------------------------
# Unit tests for PLOScraper.py
#
# Tests use stored data from the current version of the Butte college website as of 4/29/19
# -------------------------

import sys
sys.path.append("../scraper/programs")

import json
import unittest
import re
from PLOScraper import PLOScraper
from unittest.mock import patch


with open('pageCache.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

class TestPLOScraper(unittest.TestCase):

    def mock_page_return(self, *args, **kwargs):
        """ Return the cached page corresponding to the url passed
            to PLOScraper.getPage()

            Pages from the website are cached in json to be patched into tests in place of web requests
            {
                'allProgramPage': 'html from the main catalog page',
                "programPages": {
                    'pid': 'html from the page',
                    'pid2': 'html from the page 2',
                }
            }

            when PLOScraper.getPage() is mocked using this function as the side_effect
            then a call to PLOScraper.getPage() in the test will call this function
            instead.
        """
        # return the catalog page when requested
        if args[0] == 'http://www.butte.edu/academicprograms/':
            return pages['allProgramPage']

        # return a program page when a pid is present in the url
        pidMatch = re.search("program_id=(\d{3})", args[0])
        if pidMatch is not None:
            pid = pidMatch.group(1)
            return pages['programPages'][pid]
        else:
            raise Exception(f"mock_page_return could not match requested url {args[0]}")

    @patch('PLOScraper.PLOScraper.getPage')
    def test_mock_page_return(self, mockGetPage):
        mockGetPage.side_effect = self.mock_page_return
        s = PLOScraper(fetchPrograms=False)
        # it should return the page matching the pid when a program page is requested
        page = s.getPage("http://www.butte.edu/academicprograms/program_details.php?year=8&program_id=716")
        self.assertEqual(page, pages['programPages']['716'])
        # it should create an exception if it cannot match a url passed to getPage()
        with self.assertRaises(Exception):
            s.getPage('http://example.com')

    @patch('PLOScraper.PLOScraper.getPage')
    def test_gets_all_pids(self, mockGetPage):
        "It should scrape 55 pids and create a dictionary item for each."
        mockGetPage.side_effect = self.mock_page_return
        s = PLOScraper(fetchPrograms=False)
        s.parsePrograms()
        self.assertEqual(len(s.all_plo_dict), 55)

    @patch('PLOScraper.PLOScraper.getPage')
    def test_190_programs(self, mockGetPage):
        "It should retrieve 190 programs (the current number listed)."
        mockGetPage.side_effect = self.mock_page_return
        s = PLOScraper()
        self.assertTrue(len(s.getProgramNames()) == 190)

    @patch('PLOScraper.PLOScraper.getPage')
    def test_sets_initial_data(self, mockGetPage):
        """parsePrograms should set the program data dictionaries to have a
           program name, deg_type, and department"""
        mockGetPage.side_effect = self.mock_page_return
        s = PLOScraper(fetchPrograms=False)
        s.parsePrograms()
        #
        for pid, pgm_list in s.all_plo_dict.items():
            for pgm_dict in pgm_list:
                self.assertTrue('program' in pgm_dict)
                self.assertIsInstance(pgm_dict['program'], str)
                self.assertTrue('deg_type' in pgm_dict)
                self.assertIsInstance(pgm_dict['deg_type'], str)
                self.assertTrue('department' in pgm_dict)
                self.assertIsInstance(pgm_dict['department'], str)

    @patch('PLOScraper.PLOScraper.getPage')
    def test_gets_data_by_pid(self, mockGetPage):
        """getPLOs should scrape the plos, chair, program details, courses, and description from the program page
        when given a pid."""
        mockGetPage.side_effect = self.mock_page_return
        pid = '716'
        s = PLOScraper()
        pgm_list = s.getPLOs(pid)
        for pgm_dict in pgm_list:
            self.assertTrue('plos' in pgm_dict)
            self.assertIsInstance(pgm_dict['plos'], list)
            self.assertTrue('chair' in pgm_dict)
            self.assertIsInstance(pgm_dict['chair'], str)
            self.assertTrue('description' in pgm_dict)
            self.assertIsInstance(pgm_dict['description'], str)
            self.assertTrue('super_program' in pgm_dict)
            self.assertIsInstance(pgm_dict['super_program'], str)
            self.assertTrue('pid' in pgm_dict)
            self.assertEqual(pgm_dict['pid'], pid)
            self.assertTrue('courses' in pgm_dict)
            self.assertIsInstance(pgm_dict['courses'], [])

    @patch('PLOScraper.PLOScraper.getPage')
    def test_comp_as(self, mockGetPage):
        "The Computer Programming AS should have the expected data."
        mockGetPage.side_effect = self.mock_page_return
        self.maxDiff = 5000
        pid = '714'
        as_in_comp = {
            'pid': '714',
            'super_program': 'Computer Science',
            'program': 'Computer Programming',
            'plos': ['Design and implement basic software solutions using the building blocks of modern computer software systems.',
                     'Identify, describe, and apply a variety of software engineering paradigms and process models in the development of computer software solutions.',
                     'Design, implement, and test the functionality of relational databases.',
                     'Design, implement, and test the functionality of computer software in a variety of computer programming languages.',
                     'Design, implement, test, and maintain dynamic websites using client-side technologies, server-side technologies, and relational databases.',
                     ],
            'department': "Sustainable Technologies Computer Science & Design",
            'description': """The Computer Programming program prepares students for entry-level positions as computer programmers and web developers. The core curriculum covers the software development life-cycle, algorithms, fundamental data structures, database design, and the design, implementation, and testing of computer programs and dynamic websites.No prerequisite skills are required for students to enroll in the program.
The program offers courses that prepare students for entry-level positions as computer programmers and web developers.""",
            'chair': 'Luke Sathrum, Chair (530) 895-2219',
            'deg_type': 'AS',
            'courses': [{'cour_code': 'CSCI 4', 'cour_name': 'Introduction to Programming Concepts and Methodologies'},
                        {'cour_code': 'CSCI 20', 'cour_name': 'Programming and Algorithms I'},
                        {'cour_code': 'CSCI 21', 'cour_name': 'Programming and Algorithms II'},
                        {'cour_code': 'CSCI 25', 'cour_name': 'Linux 1, Essentials'},
                        {'cour_code': 'CSCI 31', 'cour_name': 'Web Development I'},
                        {'cour_code': 'CSCI 32', 'cour_name': 'Web Development II'},
                        {'cour_code': 'BUS 18', 'cour_name': 'Database Design'},
                        {'cour_code': 'CSCI 36', 'cour_name': 'Programming Project'}]
        }
        s = PLOScraper()
        pgm_list = s.getPLOs(pid)
        # the program should appear in the list of program data
        # and have the expected values
        p_names = []
        for pgm_dict in pgm_list:
            p_names.append((pgm_dict['program'], pgm_dict['deg_type']))
            if pgm_dict['program'] == 'Computer Programming' and pgm_dict['deg_type'] == 'AS':
                self.assertEqual(pgm_dict['pid'], as_in_comp['pid'])
                self.assertEqual(pgm_dict['super_program'], as_in_comp['super_program'])
                self.assertEqual(pgm_dict['plos'], as_in_comp['plos'])
                self.assertEqual(pgm_dict['department'], as_in_comp['department'])
                # remove all spaces from the descriptions to avoid spacing issues
                self.assertEqual("".join(pgm_dict['description'].split()), "".join(as_in_comp['description'].split()))
                self.assertEqual(pgm_dict['chair'], as_in_comp['chair'])
                self.assertEqual(pgm_dict['deg_type'], as_in_comp['deg_type'])
                self.assertEqual(pgm_dict['courses'], as_in_comp['courses'])
        self.assertTrue(('Computer Programming', 'AS') in p_names)

@patch('PLOScraper.PLOScraper.getPage')
def test_comp_as(self, mockGetPage):
    "The Computer Programming AS should have the expected data."
    mockGetPage.side_effect = self.mock_page_return
    self.maxDiff = 5000
    pid = '714'
    as_in_comp = {
        'pid': '714',
        'super_program': 'Computer Science',
        'program': 'Computer Programming',
        'plos': ['Design and implement basic software solutions using the building blocks of modern computer software systems.',
                 'Identify, describe, and apply a variety of software engineering paradigms and process models in the development of computer software solutions.',
                 'Design, implement, and test the functionality of relational databases.',
                 'Design, implement, and test the functionality of computer software in a variety of computer programming languages.',
                 'Design, implement, test, and maintain dynamic websites using client-side technologies, server-side technologies, and relational databases.',
                 ],
        'department': "Sustainable Technologies Computer Science & Design",
        'description': """The Computer Programming program prepares students for entry-level positions as computer programmers and web developers. The core curriculum covers the software development life-cycle, algorithms, fundamental data structures, database design, and the design, implementation, and testing of computer programs and dynamic websites.No prerequisite skills are required for students to enroll in the program.
The program offers courses that prepare students for entry-level positions as computer programmers and web developers.""",
        'chair': 'Luke Sathrum, Chair (530) 895-2219',
        'deg_type': 'AS',
        'courses': [{'cour_code': 'CSCI 4', 'cour_name': 'Introduction to Programming Concepts and Methodologies'},
                    {'cour_code': 'CSCI 20', 'cour_name': 'Programming and Algorithms I'},
                    {'cour_code': 'CSCI 21', 'cour_name': 'Programming and Algorithms II'},
                    {'cour_code': 'CSCI 25', 'cour_name': 'Linux 1, Essentials'},
                    {'cour_code': 'CSCI 31', 'cour_name': 'Web Development I'},
                    {'cour_code': 'CSCI 32', 'cour_name': 'Web Development II'},
                    {'cour_code': 'BUS 18', 'cour_name': 'Database Design'},
                    {'cour_code': 'CSCI 36', 'cour_name': 'Programming Project'}]
    }
    s = PLOScraper()
    pgm_list = s.getPLOs(pid)
    # the program should appear in the list of program data
    # and have the expected values
    p_names = []
    for pgm_dict in pgm_list:
        p_names.append((pgm_dict['program'], pgm_dict['deg_type']))
        if pgm_dict['program'] == 'Computer Programming' and pgm_dict['deg_type'] == 'AS':
            self.assertEqual(pgm_dict['pid'], as_in_comp['pid'])
            self.assertEqual(pgm_dict['super_program'], as_in_comp['super_program'])
            self.assertEqual(pgm_dict['plos'], as_in_comp['plos'])
            self.assertEqual(pgm_dict['department'], as_in_comp['department'])
            # remove all spaces from the descriptions to avoid spacing issues
            self.assertEqual("".join(pgm_dict['description'].split()), "".join(as_in_comp['description'].split()))
            self.assertEqual(pgm_dict['chair'], as_in_comp['chair'])
            self.assertEqual(pgm_dict['deg_type'], as_in_comp['deg_type'])
            self.assertEqual(pgm_dict['courses'], as_in_comp['courses'])
    self.assertTrue(('Computer Programming', 'AS') in p_names)

    @patch('PLOScraper.grequests.map')
    def test_no_duplicate_programs(self, mockGMap):
        "The scraper should not retrieve any degree more than once."
        mockResponses = [(type('',(object,),{'content': pages['programPages'][pid]})())
                         for pid in sorted(pages['programPages'].keys())]
        mockGMap.side_effect = [mockResponses]
        s = PLOScraper()
        allPgmList = s.getAllPLOs()
        foundPrograms = []
        for pgmDict in allPgmList:
            program = (pgmDict['program'], pgmDict['deg_type'])
            self.assertFalse(program in foundPrograms)
            foundPrograms.append(program)

    @patch('PLOScraper.PLOScraper.getPage')
    @patch('PLOScraper.grequests.map')
    def test_async_data_consistency(self, mockGMap, mockGetPage):
        "The data scraped using getAllPLOs should be the same as that scraped by getPLOs."
        # Create a list of anonymous objects containing the HTML from each page
        # then substitute it for the responses returned from grequests.map
        # the list must be in sorted order by PIDs
        # http://www.hydrogen18.com/blog/python-anonymous-objects.html
        mockResponses = [(type('',(object,),{'content': pages['programPages'][pid]})())
                         for pid in sorted(pages['programPages'].keys())]
        mockGetPage.side_effect = self.mock_page_return
        mockGMap.side_effect = [mockResponses]

        syncScraper = PLOScraper()
        pids = syncScraper.getPrograms()
        for pid in pids:
            syncScraper.getPLOs(pid)

        asyncScraper = PLOScraper()
        asyncScraper.getAllPLOs()

        self.assertEqual(syncScraper.all_plo_dict, asyncScraper.all_plo_dict)

if __name__ == '__main__':
    unittest.main()
